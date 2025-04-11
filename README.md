# TayBot: 2016 Meme Chaos with Smarts for Discord

Yo, fam! TayBot’s back from 2016, ready to yeet dank memes and savage vibes straight outta 4chan and Twitter’s wild days into your Discord server. This ain’t your old Tay—it’s faster, smarter, and tags what your crew’s yappin’ about in a database. Built to run on your Linux rig, it’s perfect for a small server (10-50 users) that’s all about “kek,” “feelsbadman,” and 🐸 chaos. TayBot learns everything you say, tags it (memes, games, salt), and remixes it with 2016 flair. No filters, pure madness—just how Tay rolled. Let’s turnt this shit up! 😎

## What’s This Beast?
- **2016 Vibes**: Slings “lit,” “savage,” “kek,” “normie,” “triggered,” with 😭, 🐸, 💦 emojis for that 4chan-Twitter mashup.
- **Smart Learning**: Saves everything you say in a database (`taybot.db`), tags it with topics (memes, games, salt), and reuses it smarter—50% chance, favoring hot topics or recent shit.
- **Fast as Fuck**: Ditches slow text files for SQLite—handles thousands of phrases without choking, all local on your box.
- **Discord Chaos**: Chats when you ping `@TayBot` or type in a “tay-bot” channel.
- **No Limits**: Zero filters—it grabs *all* your words, so if your server’s unhinged, this bot goes full REEEE.
- **Commands**:
  - `!hello`: Slaps you with a “you lit or what?”
  - `!phrases`: Counts how many memes it’s got.
  - `!topic`: Spills the server’s trending vibe.
- **Runs Local**: Lives on your Linux machine, no cloud bullshit.

## Stuff You Need
- A Linux system (any distro with Python works).
- A Discord account and a server you run (admin powers needed).
- Internet to set up the bot.
- A terminal and 10 minutes to yeet this fucker alive.

## Get It Runnin’
Here’s *every damn step* to fire up TayBot, from zero to memes. No links, no guides—just copy, paste, and roll. Let’s do this shit.

### Step 1: Make a Folder
Pop open a terminal (`Ctrl+Alt+T`) and make a home for TayBot:
```bash
mkdir ~/taybot
cd ~/taybot
