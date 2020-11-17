#!/usr/bin/python3

from sense_hat import SenseHat
import paho.mqtt.client as mqtt
import os, sys, json, time

cfg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
if(not(os.path.exists(cfg_path))):
	sys.stderr.write("Configuration file " + cfg_path + " not found.\n")
	sys.exit(1)
fp = open(cfg_path, "r")
cfg = json.load(fp)
fp.close()

if not('id' in cfg):
	sys.stderr.write("No 'id' field in configuration.\n")
	sys.exit(1)
if not('broker' in cfg):
	sys.stderr.write("No 'broker' field in configuration.\n")
	sys.exit(1)
if not('topics' in cfg):
	sys.stderr.write("No 'topics' field in configuration.\n")
	sys.exit(1)

sense = SenseHat()
client = mqtt.Client(cfg['id'])

# Credit to yaab-arduino.blogspot.com for this formula, which measures temperature from the
# sensehat but also takes CPU temperature into account for a slightly more accurate reading.
temp_sense = (sense.get_temperature_from_pressure() + sense.get_temperature_from_humidity()) / 2
temp_cpu = float(os.popen("vcgencmd measure_temp").readline().replace("temp=", "").replace("'C\n", ""))
temp = temp_sense - ((temp_cpu - temp_sense) / 1.5)

client.connect(cfg['broker']['host'], port=cfg['broker']['port'])
client.publish(cfg['topics']['temperature'], round(temp, 1))
time.sleep(0.5)
client.publish(cfg['topics']['humidity'], round(sense.get_humidity(), 1))
client.disconnect()
