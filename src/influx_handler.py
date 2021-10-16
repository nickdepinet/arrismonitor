import datetime
import typing
from influxdb_client import InfluxDBClient, Point, WriteOptions

def initialize_influx(url: str, token: str):
    """
    Initializes InfluxDB to receive modem data metrics.
    """
    influx_client = InfluxDBClient(
        url=url,
        token=token
    )

    return influx_client


def send_data_to_influx(influx_client, bucket_name, org_name, record_array, direction, timestamp):
    """
    Uses the InfluxDB 2.0 Python API to send data.
    """
    with influx_client.write_api(write_options=WriteOptions(batch_size=500,
                                                      flush_interval=10_000,
                                                      jitter_interval=2_000,
                                                      retry_interval=5_000,
                                                      max_retries=5,
                                                      max_retry_delay=30_000,
                                                      exponential_base=2)) as write_client:
        write_client.write(bucket_name, org_name, record_array)
        print(f'Writing {direction} for {timestamp}')

def create_point_array(channels_list: typing.List, direction: str, modem_host: str) -> typing.List:
    """
    Create an array of influx_db points
    :param table_data:
    :return:
    """
    points_array = []  # array of InfluxDBPoints
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    for channel in channels_list:
        data_point = Point('channel_status')
        data_point.tag('host', modem_host)
        data_point.tag('channel_direction', direction)
        data_point.tag('channel_id', channel['ID'])
        data_point.time(timestamp)

        for value_title, value_to_report in channel.items():
            if (value_title in ['Channel', 'Modulation', 'ID', 'Type']):
                # Don't log the non-numerics, don't log id (its a tag instead)
                continue
            elif (value_title == 'Status'):
                value_to_report = True if value_to_report == 'Locked' else False
                data_point.field('Channel_Locked', value_to_report)
            elif (value_title == "Symbol Rate"):
                value_title = 'Width'

            # For some reason, Grafana doesn't play nice with using spaces in measurement keys?
            data_point.field(value_title.replace(" ", "_"), float(value_to_report))

        points_array.append(data_point)

    return points_array, timestamp