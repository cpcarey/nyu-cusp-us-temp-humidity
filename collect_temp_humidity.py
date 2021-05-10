import sys
import time
import adafruit_dht
import board
import csv
import datetime

dht_device = adafruit_dht.DHT11(board.D18)

while True:
    filename = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    i = 0
    run = True

    # Create a new CSV file with a timestamp filename.
    with open('/home/pi/data/csv/{}.csv'.format(filename),
              'w+', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar="'")
        writer.writerow(['datetime', 'temperature', 'humidity'])
        while run:
            try:
                dt_string = (datetime.datetime.now().strftime(
                             '%Y-%m-%d %H:%M:%S.%f')[:-3])
                temperature = dht_device.temperature
                humidity = dht_device.humidity
                writer.writerow([
                    dt_string,
                    '{:0.1f}'.format(temperature),
                    '{:0.1f}'.format(humidity),
                ])
            except RuntimeError as error:
                print(error.args[0])
                time.sleep(2.0)
                continue
            except Exception as error:
                dht_device.exit()
                raise error

            time.sleep(2.0)
            i += 1

            # Save and close the file after 60 iterations.
            if i > 60:
                csvfile.close()
                run = False
