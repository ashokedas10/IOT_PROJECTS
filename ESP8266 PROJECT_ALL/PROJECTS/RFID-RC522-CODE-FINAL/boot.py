# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

import network

wlan = network.WLAN(network.STA_IF) # create station interface
wlan.active(True)       # activate the interface
wlan.scan()

if not wlan.isconnected():
    print('connecting to network...')
    wlan.active(True)
    wlan.connect('12345678', '12345678')
    wlan.config('mac')
    
    while  not wlan.isconnected():
        pass
print('network config seting:', wlan.ifconfig())
