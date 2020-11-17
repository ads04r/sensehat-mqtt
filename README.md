sensehat-mqtt
=============

A very simple script to put in the cron of a Raspberry Pi with a sensehat
fitted.

It simply publishes temperature and humidity readings to an MQTT topic
whenever called.

The config.json is pretty straightforward, put the hostname and port of the
broker in the 'broker' section and change the topics for notifying temperature
and humidity in the 'topics' section. Then add to the crontab to run every
five minutes or so. Cheap and nasty thermostat!

Tested on a Raspberry Pi 1. Anything more powerful is, frankly, overkill.
