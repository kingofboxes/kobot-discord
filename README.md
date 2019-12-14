# kobot-discord

Fun side project for a Discord bot with features and utilities that I needed.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Only prerequisites required is Python 3.6+, with pip3 installed.

### Installing

Below is a step-by-step guide on setting up the program to get a development environment running.

1. Clone this repo.

```
git clone git@github.com:kingofboxes/kobot-discord.git
```

2. Change directory to of the cloned repo and create a new virtual environment.

```
cd kobot-discord
python3 -m virtualenv <folder>
```

3. Activate the virtual environment.

```
. <folder>/bin/activate
```

4. Install the requirements using pip3.

```
pip3 install -r requirements.txt
```

5. Create a new file called '.env' as follows.

```
echo DISCORD_TOKEN="YOUR_BOT_TOKEN" > .env
```

6. Run the program.

```
python3 main.py
```

7. If done correctly, it should say that your bot has connected.

## Current Features

### Features List
1. Parroting. !mirror <message> will send the message back to you in your PMs.
2. Quoting. Reacting to a message with ✳️ will quote the message and mention the original sender. Works with images.
3. Reminders. !remindme will set a reminder. Usage: !remindme [time] [description] 
4. Uwulate. !uwulate <message> will uwulate the message. Reacting to a message with ♿ will uwulate the message and notify the original sender.
5. Dictionary. !define <word> will attempt to find the word in the dictionary. Note that it takes some time.

### Motivation
1. Parroting was an introduction to using the discord.py and learning how to send messages.
2. Quoting was the first major feature which involved learning and using the discord.py API to do a simple task with many steps.
3. Reminders was the second major feature which was slightly more complex with use cases and learning how to run background tasks.
4. Uwulate was the third feature that was extremely simple and minor. Idea taken from Reddit.
5. Dictionary was the fourth major feature that involved learning how to use a different API and combining it with my bot.

This whole project is a learning experience aimed to develop my skills by extending functionality to the bot while being practical about the features added.

## Acknowledgments

* [PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2) - For the README.md template.
* [Cimera42](https://github.com/Cimera42/DiscordBot) - For the idea of QuoteBot.
* [nltk](https://github.com/nltk/wordnet) - For the standalone wordnet API.
