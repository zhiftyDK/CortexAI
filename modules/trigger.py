import modules.phillipshue as ph

def lights_on(args):
    ph.light(on=True)

def lights_off(args):
    ph.light(on=False)

def fan_on(args):
    ph.fan(on=True)

def fan_off(args):
    ph.fan(on=False)

trigger_functions = [lights_on, lights_off, fan_on, fan_off]