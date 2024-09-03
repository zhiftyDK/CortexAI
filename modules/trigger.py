import modules.phillipshue as ph

def lights_on():
    ph.light(on=True)

def lights_off():
    ph.light(on=False)

def fan_on():
    ph.fan(on=True)

def fan_off():
    ph.fan(on=False)

trigger_functions = [lights_on, lights_off, fan_on, fan_off]