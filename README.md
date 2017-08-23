# smart_toy

Final project for CS-457 Wireless and Mobile Security

* Example Bot

How the example bot works, first install nodejs and use npm install

** Motor.js
This is a wrapper to talk to the raspberry pi GPIO and talk to a motor driver.
This allows someone to control the speed of a motor attached to a rapsberry pi

** robot.js
This makes an open socket communication layer, so you can control motors and turn on and off leds thourgh a web socket

** server.js
This is the web server that feeds the web UI to the user, and relays commands given by the user to the robot.js though websockets.

** public/*, robots/* and index.html
index.html splits into two views, one to control the command bot, and the other to control the car both of the views are in the robots folder. In the public folder all files are accessable from the web, so clientside librarys are in here.
