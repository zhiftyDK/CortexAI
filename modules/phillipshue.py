import os
from dotenv import load_dotenv
import urllib3
urllib3.disable_warnings()
from huesdk import Hue

load_dotenv()

bridge_ip = "192.168.1.210"
username = os.getenv("HUE_USERNAME")

hue = Hue(bridge_ip=bridge_ip, username=username)

def light(on):
    group = hue.get_group(name="Lys Værelse")
    if on:
        group.on()
        group.set_brightness(254)
    else:
        group.off()

def fan(on):
    group = hue.get_light(name="Blæser")
    if on:
        group.on()
    else:
        group.off()