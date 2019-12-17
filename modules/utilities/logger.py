from datetime import datetime, timedelta

# Returns a timestamp in a string format.
def timestamp():
    return datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

# Outputs a message to the server logs.
def log(message):
    print(message)
    f = open("data/log.txt", "a+")
    f.write(message + "\n")
    f.close()

