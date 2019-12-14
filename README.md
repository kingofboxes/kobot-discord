# kobot-discord

**Installation:**
1. Clone the repository.
2. Create a new .env file.
3. Add the following line to the file:
```
DISCORD_TOKEN = <BOT_TOKEN> 
```
4. Install requirements from "requirements.txt" using pip3.

**Execution:**

Program can be run with:
```
python3 main.py
```
Written for Python 3.6+ (for compatibility with f-strings).

**Current Features:**
1. Parroting. !mirror <message> will send the message back to you in your PMs.
2. Quoting. Reacting to a message with ✳️ will quote the message and mention the original sender. Works with images.
3. Reminders. !remindme will set a reminder. Usage: !remindme [time] [description] 
4. Uwulate. !uwulate <message> will uwulate the message. Reacting to a message with ♿ will uwulate the message and notify the original sender.
5. Dictionary. !define <word> will attempt to find the word in the dictionary. Note that it takes some time (since dictionary is local and not web scraped).
