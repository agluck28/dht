import time, json, sys
import board
sys.path.append('/home/pi/Documents/GIT/modules')
import adafruit_dht
from Flux.Flux import Writer
from PointWriter.PointWriter import PointWriter


#read constants from configuration file
with open('./.configuration/db_settings.local.json') as jsondata:
    config = json.load(jsondata)

#open up a writer connection
db_writer = Writer(config['token'], config['org'], config['url'], config['bucket'])

#initialize data dict
data = {
        'temperature': -1,
        'humidity': -1
}

#Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT11(board.D17)

#setup base point
base_point = PointWriter(config['roomId'],('deviceId', config['deviceId']))

while True:
    try:
        # Print the values to the serial port
        data['temperature'] = dhtDevice.temperature * (9 / 5) + 32
        data['humidity'] = dhtDevice.humidity
        temp_point = base_point.add_fields(data, time.time_ns())
        db_writer.write_data(temp_point)
        time.sleep(60)
    except RuntimeError as error:     # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
    