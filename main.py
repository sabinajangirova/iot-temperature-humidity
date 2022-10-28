import pycom
import time
from machine import Pin
from dth import DTH
from network import LoRa
import socket
import ubinascii
import struct

pycom.heartbeat(False)
pycom.rgbled(0x000008) # blue
th = DTH(Pin('P23', mode=Pin.OPEN_DRAIN),0)
time.sleep(2)

lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

app_eui = ubinascii.unhexlify('0000000000000000')
app_key = ubinascii.unhexlify('1500E1BFA9365C2AB79BBFC9B4C896C6')
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

while not lora.has_joined():
    print('Not yet joined...')
    time.sleep(3)

print('Joined network')

s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
s.setblocking(True)
s.bind(2)

result = th.read()

if result.is_valid():
    pycom.rgbled(0x001000) # green
    temp = result.temperature
    hum = result.humidity
    print(bytes([temp, hum]))
    s.send(bytes([temp, hum]))
    machine.deepsleep(900000)
