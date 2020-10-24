import urequests
import json,ujson
from machine import Pin
import mfrc522
from os import uname

#DATA COMMUNICATION WITH SERVER --WORKING PERFECTLY

led = Pin(2, Pin.OUT)
url="http://royhomoeohall.co.in/roynew/Api_controller/esp32"
headers_val={"Content-Type": "application/json", "Accept": "application/json"}
# led_desc='TEST DESCRIP'
led_value=0
# post_data = ujson.dumps({ "led_desc": led_desc, "led_value": led_value})
#  
# while True:    
#         #response = urequests.post(url,headers={"Content-Type": "application/json", "Accept": "application/json"},data = "test")
#         response = urequests.post(url,headers=headers_val,data =post_data)
#         json_to_dictionary = json.loads(response.text)
#         print(json_to_dictionary['led_value'])
#         led_value=json_to_dictionary['led_value']
#         led.value(int(led_value))

#DATA COMMUNICATION WITH SERVER --WORKING PERFECTLY


#COMMUNICATE WITH RFID CARD


if uname()[0] == 'WiPy':
    rdr = mfrc522.MFRC522("GP14", "GP16", "GP15", "GP22", "GP17")
elif uname()[0] == 'esp8266':
   # rdr = mfrc522.MFRC522(0, 2, 4, 5, 14)
   #sck, mosi, miso, rst, cs
    rdr = mfrc522.MFRC522(14, 13, 12, 5, 15)
    print(uname()[0])
    print(rdr.request(rdr.REQIDL))
# elif uname()[0] == 'esp32':
#     rdr = mfrc522.MFRC522(0, 18, 23, 19, 14)
else:
    raise RuntimeError("Unsupported platform")

    print("")
    print("Place card before reader to read from address 0x08")
    print("")

try:
    while True:
        (stat, tag_type) = rdr.request(rdr.REQIDL)

        if stat == rdr.OK:
            (stat, raw_uid) = rdr.anticoll()
            if stat == rdr.OK:
                print("New card detected")
                print("  - tag type: 0x%02x" % tag_type)
                #UID=(raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
                UID="0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
                print(UID)
                
                post_data = ujson.dumps({ "led_desc": UID, "led_value": led_value})
                response = urequests.post(url,headers=headers_val,data =post_data)
                json_to_dictionary = json.loads(response.text)
                print(json_to_dictionary['led_value'])
                led_value=json_to_dictionary['led_value']
                led.value(int(led_value))
                                
                print(UID)
                if UID=="0xa0faf473":
                    led.value(1)
                    
                if UID=="0x909e1883":
                    led.value(0)
                    
                print("  - uid   : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                print("")

                if rdr.select_tag(raw_uid) == rdr.OK:

                    key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

                    if rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid) == rdr.OK:
                        print("Address 8 data: %s" % rdr.read(8))
                        rdr.stop_crypto1()
                    else:
                        print("Authentication error")
                else:
                    print("Failed to select tag")

except KeyboardInterrupt:
    print("Bye")

#COMMUNICATE WITH RFID END
