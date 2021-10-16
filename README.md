# arrismonitor
Monitor Arris Cable Modem Channel Status over HNAP

Connect to local Arris Surfboard Cable Modem (Tested with SB33, but any modern surfboard should work) over HNAP and push upstream and downstream channel status into influxdb 2.x

# Usage

Config is handled by environment settings:

| Environment Setting Name| use | default |
|--|--|--|
|ARRIS_HOST| modem ip | 192.168.100.1 |
|ARRIS_USER| modem username | admin |
|ARRIS_PASSWORD| modem password | password |
|INFLUX_URL| influxdb url | http://localhost/8086 |
|INFLUX_TOKEN| influxdb access token (needs write on the bucket) | no default |
|INFLUX_BUCKET| influxdb bucket | modem_status |
|INFLUX_ORG| influxdb org | logs |

## Running locally:
Install requirements with `pip install -r requirements.txt` and then run the program with `python ./src/main.py`

## Running with docker:

`docker pull nickdepinet/arrismonitor`
`docker run nickdepinet/arrismonitor`

# Thanks
Special Thanks to:
* https://github.com/mitchelhaan/moto-client for the motorola hnap client which i've updated to work with arris modems
