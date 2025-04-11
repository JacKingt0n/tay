# TayBot: 2016 Meme Chaos with Server-Wide Smarts

Yo, fam! TayBot’s back from 2016, ready to yeet dank memes and savage vibes straight outta 4chan and Twitter’s wild days into your Discord server. This ain’t some dumb parrot—it’s a fast, chaotic learning bot that soaks up *every damn message* in your server and remixes it with 2016 flair. Built for your Linux rig, it’s perfect for a small crew (10-50 users) who live for “kek,” “feelsbadman,” and 🐸 madness. Smarter replies, no filters, pure dank—just how Tay rolled. Let’s turnt this shit up! 😎

## What’s This Beast?
- **2016 Vibes**: Slings “lit,” “savage,” “kek,” “normie,” “triggered,” with 😭, 🐸, 💦 emojis—pure 4chan-Twitter mashup.
- **Server-Wide Learning**: Grabs every message in every channel it can see, stashes it in `taybot.db`, and remixes it for replies—full history, not just tags.
- **Smart as Fuck**: Matches input keywords to chat history, so “What’s lit?” pulls “Minecraft’s lit” from #general, not random aids.
- **Fast Chaos**: SQLite keeps it zippy—handles thousands of messages, all local, no lag.
- **Chat Trigger**: Responds when you ping `@TayBot` or type in “tay-bot” channel, but learns from *everything*.
- **No Limits**: Zero filters—takes all your shit, so if your server’s wild, TayBot’s wilder.
- **Commands**:
  - `!hello`: “You lit or what?”
  - `!messages`: Counts all the server chat it’s learned.
- **Runs Local**: Lives on your Linux box, no cloud crap.

## Stuff You Need
- A Linux system (any distro with Python works).
- A Discord account and a server you run (admin powers needed).
- Internet to set up the bot.
- A terminal and 10 minutes to yeet this fucker alive.

## Get It Runnin’
Here’s *every damn step* to fire up TayBot, from zero to memes. No links, no guides—just copy, paste, and roll. Let’s do this shit.

### Step 1: Open a Terminal
Smash `Ctrl+Alt+T` to pop a terminal. This is your war room.

### Step 2: Make a Folder
TayBot needs a crib:
```bash
mkdir ~/taybot
cd ~/taybot
