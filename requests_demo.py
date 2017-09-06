import requests
import time

# Simple demo for the record and replay route function

url = "http://localhost:8000/"


command = 'start'
r = requests.post(url, command)
time.sleep(3)

command = "fb=19"
r = requests.post(url, command)
time.sleep(3)


command = "lr=108"
r = requests.post(url, command)
time.sleep(3)

command = "stop"
r = requests.post(url, command)
time.sleep(1)

command = "play"
r = requests.post(url, command)

