def lights_on():
    print("Turning lights on!")

def lights_off():
    print("Turning lights off!")

trigger_functions = [lights_on, lights_off]
def handleTrigger(prediction, confidence_threshold):
    if float(prediction["probability"]) > confidence_threshold:
        for function in trigger_functions:
            if function.__name__ == prediction["intent"]:
                function()