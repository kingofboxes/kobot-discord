from datetime import datetime, timedelta

# Returns a timestamped string (UTC+11 for Sydney).
def timestamp():
    return (datetime.now() + timedelta(hours=11)).strftime("%d/%m/%Y, %H:%M:%S")

def log(message):
    f = open("log.txt", "a+")
    f.write(message + "\n")
    f.close()

