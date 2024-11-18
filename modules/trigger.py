import modules.phillipshue as ph
import requests

def lights_on(args):
    ph.light(on=True)

def lights_off(args):
    ph.light(on=False)

def fan_on(args):
    ph.fan(on=True)

def fan_off(args):
    ph.fan(on=False)

def weather(args):
    city = "Silkeborg"
    res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=f4e80e2071fcae0bd7c122d2f82fd284").json()
    return f"Temp: {res['main']['temp']} celcius, Description: {res['weather'][0]['description']}, City: {res['name']}"

trigger_functions = [lights_on, lights_off, fan_on, fan_off, weather]