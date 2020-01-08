#! /usr/bin/python2
# -*- coding: utf-8 -*-
import time
import sys
from datetime import datetime, timedelta
import csv
import numpy as np

d = datetime.today()
exetime = d.strftime("%y/%m/%d %H:%M")

# exit()

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
# iPhoneCar = -1560977

# iPhoneCar = 19000

# caribration = iPhoneCar / iPhoneWeight

# hx.set_reference_unit(caribration)
hx.set_reference_unit(-750)
# hx.set_reference_unit(referenceUnit)
# hx.set_reference_unit(1)
# hx.set_reference_unit(11087)
# -------------------------------------------------------------------------
hx.reset()

# hx.tare()

print("Tare done! Add weight now...")

# to use both channels, you'll need to tare them both
#hx.tare_A()
#hx.tare_B()
array = []
tmp = 0
while True:
    try:
        water = hx.get_weight(1) - 2596 - bowl

        # if tmp != water:
        #     print("水の量は" + str(abs(water + 188)) + "gです。")
        #else:
        #    print("Same Weight!!!")
        #print("tmp" + str(tmp))
        print("重さは" + str(water))

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
            w.writerow(exetime)
            w.writerow(array)
        print(ave)
        cleanAndExit()
