import urllib3
urllib3.disable_warnings()
from huesdk import Hue

bridge_ip = "192.168.1.210"
username = "8uw4SmJNOFfYREWKSsQ245MnGYLu8Ox8tcDkYQE4"

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