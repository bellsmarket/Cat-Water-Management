#! /usr/bin/python2
# -*- coding: utf-8 -*-
import time
import sys
from datetime import datetime, timedelta
import csv
import os
import sys
from time import sleep
import Adafruit_DHT
from datetime import datetime
# from mymodule import mail_alert

d = datetime.today()
record_time = d.strftime("%y/%m/%d %H:%M")

HOMEPATH = os.environ['HOME']
# print(HOMEPATH)
os.chdir(os.getcwd())
# print(os.getcwd())
CSVPATH = os.getcwd()

CSV = '/home/rasbell/Program/cat-management/observation_record.csv'

# print(CSVPATH)
# print(CSV)
# exit()
# ---------------------------------------------------------------------------
sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }

nowtime =  datetime.now().strftime("%Y/%m/%d %H:%M")

sensor = Adafruit_DHT.AM2302

pin = 4
 #   print('Usage: sudo ./Adafruit_DHT.py [11|22|2302] <GPIO pin number>')
  #  print('Example: sudo ./Adafruit_DHT.py 2302 4 - Read from an AM2302 connected to GPIO pin #4')
   # sys.exit(1)

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

data = {
    'date': '',
    'temp': '',
    'humi': ''
}

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
# if humidity is not None and temperature is not None:
#     print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
# else:
#     print('Failed to get reading. Try again!')
context = 'Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity)


data['date'] = nowtime
data['temp'] = round(float('{}'.format(temperature)), 1)
data['humi'] = round(float('{}'.format(humidity)), 1)
# cols = data.keys()
row = []

# -------------------------------------------------------
EMULATE_HX711=False

referenceUnit = 1

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

def cleanAndExit():
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()
    print("Bye!")
    sys.exit()

hx = HX711(5, 6)


# -------------------------------------------------------------------------
hx.set_reading_format("MSB", "MSB")


#基準単位を1に設定するには、センサーまたはお持ちの物に1kgを乗せ、重量を正確に把握します。
#この場合、92は1グラムです。これは、参照単位として1を使用すると、重みなしで0に近い数値が得られるためです。
#
#2kgを追加したときに184000前後の数字が出ました。 だから、三分の一のルールに従って：
#2000グラムが184000の場合、1000グラムは184000/2000 = 92です。


#+_ 1-2g程度の誤差まで追い込んでいる
#ベルの水の器の重さ    218g
bowl = 218


#キャリブレーション用に正確な重さのオブジェクト(iPhone 7使用)
#iPhone 7 Plus  188g    117000

iPhoneWeight = 188
# iPhoneCar = 124400
# iPhoneCar = 800000
# iPhoneCar = 1417694
iPhoneCar = -143487

# iPhoneCar = 19000

caribration = iPhoneCar / iPhoneWeight

hx.set_reference_unit(caribration)
# hx.set_reference_unit(-750)
# hx.set_reference_unit(referenceUnit)
# hx.set_reference_unit(1)

# hx.set_reference_unit(11087)
# -------------------------------------------------------------------------
hx.reset()

# hx.tare()
print("デバッグ用プログラム・重さは容器の量を含めて計測します。")
data = [record_time, str(data['temp']), str(data['humi'])]  
tmp = 0
array = []
correction_value = 2536 - 90 

while True:
    try:

        water = hx.get_weight(1) - correction_value - bowl -30
        standard_point  = hx.get_weight(1)
        errorrange = hx.get_weight(1) - correction_value
        if tmp != water:
            print("全体の重量:" + str(abs(water + 188))  + "g\t"+ "水の重量：" + str(abs(water)) + "g")
        array.append(water)
        hx.power_down()
        hx.power_up()
        time.sleep(0.3)
        tmp = water
    except (KeyboardInterrupt, SystemExit):
        # result = numpy.array(array)
        ave = sum(array) / len(array)
        with open('measurement.csv', "a")as f:
            w = csv.writer(f, lineterminator='\n')
            w.writerow(record_time)
            w.writerow(array)
            w.write(data['temp'])

        print(ave)
        cleanAndExit()


