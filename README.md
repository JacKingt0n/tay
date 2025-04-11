# TayBot: 2016 Meme Machine for Discord

![Pepe Vibes](https://i.imgur.com/undefined.jpg) *Kek! Ready to yeet some 2016 vibes?* 🐸

TayBot is a Discord chatbot that channels the chaotic, meme-heavy spirit of Microsoft's 2016 Twitter bot, Tay. Built for a small server (10-50 users), it runs locally on Linux, bringing back the "lit," "savage," and "feelsbadman" slang of 2016's internet culture—think 4chan, Twitter, and peak meme era. TayBot learns by storing user phrases in a text file and reusing them in quirky replies, no big-ass LLM needed. It’s nostalgic, fun, and safe for your crew.

## Features
- **2016 Slang & Vibes**: Drops "kek," "YOLO," "normie," and 😭 emojis like it’s 2016 all over again.
- **Tay-Style Learning**: Saves up to 100 user phrases in `phrases.txt` and reuses them randomly (30% chance) for that parroting, adaptive feel.
- **Discord Integration**: Responds to `@TayBot` mentions or messages in a "tay-bot" channel.
- **Safety First**: Filters out toxic words to keep your server chill, unlike OG Tay’s meltdown.
- **Commands**:
  - `!hello`: Get a lit greeting.
  - `!phrases`: Check how many memes TayBot’s learned.
- **Local & Lightweight**: Runs on your   machine with just Python and `discord.py`.

## Prerequisites
-   Linux (with Python 3.12).
- A Discord account and a server where you have admin rights.
- A Discord bot token (see Setup).
- Basic terminal skills to yeet this bot into action.

## Setup
Follow these steps to get TayBot memein’ on your server.

1. **Clone or Create Project Folder**  
   ```bash
   mkdir ~/taybot
   cd ~/taybot

