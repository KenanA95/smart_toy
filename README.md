# smart_toy

Final project for CS-457 Wireless and Mobile Security. This project aims
to create a secure smart toy with common and cheap hardware to prove
that internet connected smart toys can be secure. It will be a RC car
that will be to be controlled using any wifi enabled device with a
browser that supports HTML5 and ecmascript 5.1 standards. The program
will include features such as a live video feed and route memorization.
</br>

## Directory Guide
`server.py`
Receive requests from the front-end UI and forward to the toy car
***
`record_route.py`
Insert the route commands sent by the user into a database to be
replayed
***
`robot.py`
Controls the car hardware through raspberry pi
***
`test_robot.py`
Class for testing purposes because actual robot.py can only be run on
the raspberry PI

<br/>

## Example Bot

Example code for similar project completed by Tim Loftis.

<br/>

`Motor.js`
This is a wrapper to talk to the raspberry pi GPIO and talk to a motor driver.
This allows someone to control the speed of a motor attached to a rapsberry pi
***

`robot.js`
This makes an open socket communication layer, so you can control motors and turn on and off leds thourgh a web socket
***

`server.js`
This is the web server that feeds the web UI to the user, and relays commands given by the user to the robot.js though websockets.
***

`public/*, robots/* and index.html`
index.html splits into two views, one to control the command bot, and the other to control the car both of the views are in the robots folder. In the public folder all files are accessable from the web, so clientside librarys are in here.
***
