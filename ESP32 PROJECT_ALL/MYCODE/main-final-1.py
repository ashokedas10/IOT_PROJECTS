import urequests
import json,ujson
from machine import Pin

led = Pin(2, Pin.OUT)
url="http://royhomoeohall.co.in/roynew/Api_controller/esp32"
headers_val={"Content-Type": "application/json", "Accept": "application/json"}
led_desc='TEST DESCRIP'
led_value=0
post_data = ujson.dumps({ "led_desc": led_desc, "led_value": led_value})
 
while True:    
        response = urequests.post(url,headers=headers_val,data =post_data)
        json_to_dictionary = json.loads(response.text)
        print(json_to_dictionary['led_value'])
        led_value=json_to_dictionary['led_value']
        led.value(int(led_value))


