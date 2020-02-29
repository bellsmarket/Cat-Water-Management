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
import mymodule.mail_alert

d = datetime.today()
record_time = d.strftime("%y/%m/%d %H:%M")

HOMEPATH = os.environ['HOME']
os.chdir(os.getcwd())
CSVPATH = os.getcwd()

CSV = '/home/rasbell/Program/cat-management/observation_record.csv'

# exit()
# ---------------------------------------------------------------------------
sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }

nowtime =  datetime.now().strftime("%Y/%m/%d %H:%M")
sensor = Adafruit_DHT.AM2302

pin = 4
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

data = {
    'date': '',
    'temp': '',
    'humi': ''
}

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
context = 'Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity)

data['date'] = nowtime
data['temp'] = round(float('{}'.format(temperature)), 1)
data['humi'] = round(float('{}'.format(humidity)), 1)

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
#ベルの水の器の重さ    230g
bowl = 230


#キャリブレーション用に正確な重さのオブジェクト(iPhone7 Plusで計測)
#iPhone 7 Plus  188g    Average 181300

iPhone_weight = 188
iPhone_raw_value = -181300

calibration_value = iPhone_raw_value / iPhone_weight

# hx.set_reference_unit(referenceUnit)
hx.set_reference_unit(calibration_value)

correction_value = 1869


# -------------------------------------------------------------------------
hx.reset()
# hx.tare() //計測時に0gに合わせる場合にはこのメソッドを使用する

print("日時・室温・湿度・水の量を測量しています。")

# 各種パラメーター
water = hx.get_weight(1) - correction_value - bowl
standard_point  = hx.get_weight(1)
total_weight = hx.get_weight(1) - correction_value

print("水の量は" + str(water) + "gです")

data = [record_time, str(data['temp']), str(data['humi']), str(water), str(standard_point), str(total_weight)]

# ループしたい場合には下記に追記する
# for v in data:

alert = "ベルの水が少なくなってきました。水の量は" + str(water) + "gです"
subject = "Cat Manegement Alert!!"

while True:
    if  -10 < water < 10:
        print(alert)
        mymodule.mail_alert.send_mail(alert,subject)
    else:
        print("まだまだ十分お水はあります。")

    if -100 < water < 500:
      with open(CSV, "a") as f:
          w = csv.writer(f, lineterminator='\n')
          w.writerow(data)




    cleanAndExit()
