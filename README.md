# kobot-private

**Installation:**
1. Clone the repository.
2. Create a new .env file.
3. Add the following two lines in the file:
```
DISCORD_TOKEN = <BOT_TOKEN> 
DISCORD_GUILD_ID = <GUILD_ID_TO_CONNECT_TO>
```
4. Install requirements from "requirements.txt" using pip.

**Execution:**

Program can be run with:
```
python3 main.py
```
Written for Python3.6+.

**Current Features:**
1. Parroting. !mirror <message> will send the message back to you in your PMs.
2. Quoting. Reacting to a message with :asterisk: will quote the message and mention the original sender. Works with images.

**To-do List:**
* Add in a remind me command.
* Debug mirror.
