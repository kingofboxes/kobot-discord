from datetime import datetime, timedelta
import pytz

# Returns a timestamped string for specified timezone from .
def timestamp():
    timezone = pytz.timezone("Australia/NSW")
    return datetime.now(timezone).strftime("%d/%m/%Y, %H:%M:%S")

def log(message):
    print(message)
    f = open("log.txt", "a+")
    f.write(message + "\n")
    f.close()

