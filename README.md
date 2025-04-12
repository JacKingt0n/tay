# TayBot: 2016 Meme Chaos with LLM Smarts

Yo, fam! TayBot’s back from 2016, yeetin’ dank memes and savage vibes straight outta 4chan and Twitter into your Discord server. This ain’t no aids bot—it’s a fast, chaotic learner that grabs *every damn message* server-wide and remixes it with 2016 flair, now juiced with a little LLM brain for smarter chat. Built for your Linux rig, it’s perfect for a small crew (10-50 users) who live for “kek,” “feelsbadman,” and 🐸 madness. No filters, pure dank—let’s turnt this shit up! 😎

## What’s This Beast?
- **2016 Vibes**: Slings “lit,” “savage,” “kek,” “normie,” “triggered,” with 😭, 🐸, 💦 emojis—4chan-Twitter mashup.
- **Server-Wide Learning**: Soaks up every message in every channel it sees, stashes it in `taybot.db`, and remixes it—full history, not just tags.
- **LLM Smarts**: Little DistilBERT brain parses your shit, matches it to history, and chats back—less aids, more convo.
- **Fast Chaos**: SQLite + local LLM keeps it zippy—handles thousands of messages, no cloud lag.
- **Chat Trigger**: Replies when you ping `@TayBot` or type in “tay-bot” channel, learns from *everything*.
- **No Limits**: Zero filters—takes all your wild shit and runs with it.
- **Commands**:
  - `!hello`: “You lit or what?”
  - `!messages`: Counts all server chat it’s learned.
- **Runs Local**: Lives on your Linux box, no cloud crap.

## Stuff You Need
- A Linux system (decent CPU, 2GB+ RAM free for LLM).
- A Discord account and a server you run (admin powers needed).
- Internet to set up (downloads LLM once, then offline).
- A terminal and 15 minutes to yeet this fucker alive.

## Get It Runnin’
Every step to fire up TayBot, zero to memes—just copy, paste, roll.

### Step 1: Open a Terminal
Smash `Ctrl+Alt+T`—your war room’s live.

### Step 2: Make a Folder
TayBot needs a spot:
```bash
mkdir ~/taybot
cd ~/taybot
