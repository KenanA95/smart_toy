import requests
import time

# Simple demo for the record and replay route function

url = "http://localhost:8000/"


r = requests.post(url+'start', '0')
time.sleep(3)

r = requests.post(url+'forwardBack', '50')
time.sleep(3)

r = requests.post(url+'leftRight', '122')
time.sleep(3)

r = requests.post(url+'stop', '0')
time.sleep(1)

r = requests.post(url+'play', '0')

