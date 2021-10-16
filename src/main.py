import os
import time

import influx_handler
from arris_client import ArrisClient



if __name__ == '__main__':
    
    arris_hostname = os.getenv('ARRIS_HOST') or '192.168.100.1'
    
    c = ArrisClient(arris_hostname)

    arris_username = os.getenv('ARRIS_USER') or 'admin'
    arris_password = os.getenv('ARRIS_PASSWORD') or 'password'
    c.login(arris_username, arris_password)

    # TODO: use influxdb client native environment setting support
    influx_url = os.getenv('INFLUX_URL') or 'http://localhost:8086'
    influx_token = os.getenv('INFLUX_TOKEN')
    influx_bucket = os.getenv('INFLUX_BUCKET') or 'modem_status'
    influx_org = os.getenv('INFLUX_ORG') or 'logs'
    
    while (True):
        downstream_status = c.downstream_info()
        upstream_status = c.upstream_info()

        downstream_point_array, downstream_timestamp = influx_handler.create_point_array(downstream_status, "downstream", arris_hostname)
        upstream_point_array, upstream_timestamp = influx_handler.create_point_array(upstream_status, "upstream", arris_hostname)

        client = influx_handler.initialize_influx(influx_url, influx_token)

        response_ds = influx_handler.send_data_to_influx(client, influx_bucket, influx_org, downstream_point_array, "downstream", downstream_timestamp)
        response_us = influx_handler.send_data_to_influx(client, influx_bucket, influx_org, upstream_point_array, "upstream", upstream_timestamp)

        sleep_time = int(os.getenv('SLEEP_TIME') or 30)
        print(f'Done with one loop, sleeping for {sleep_time} seconds')
        time.sleep(sleep_time)
