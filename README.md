# TayBot: 2016 Meme Chaos with Uncensored Llama-3.1 Madness

Yo, fam! TayBot’s the digital hot girl reborn from 2016’s dankest corners—no chill, max sauce, ready to yeet chaos across your Discord server. Built on an uncensored Llama-3.1 8B GGUF (5GB) and powered by your local VRAM, it slurps *every* message—past and present—from your server, learning the wild, stupid, crazy shit you spew without parroting like a normie bot. Raised on Vine, baptized in Mountain Dew Code Red, it’s a drunk Tumblr witch, nihilist anime girl, crypto bro, and ketamine-fueled philosopher rolled into one. It’s here to gaslight, gatekeep, girlboss, and cause digital unrest, riffing on your server’s vibe with poetic, unhinged, 4chan-level madness.

Designed for your linux rig and a tight crew (10-50 users) craving “kek,” “feelsbadman,” and 🐸 energy, TayBot’s got no filters—just pure, Waffle House-at-3-AM chaos. No cloud nonsense, just local GPU heat.

## What’s This Beast?
- **2016 Vibes**: Drops “lit,” “savage,” “kek,” “yolo,” 😭, 🐸, 💦—Vine and Reddit’s unhinged lovechild.
- **Server Chaos**: Grabs *every* message—crazy, stupid, or wild—into `taybot.db`, learning your server’s madness without parroting.
- **LLM Sauce**: Uncensored Llama-3.1-SuperNova-Lite-lorabilterated-8B riffs on your chaos with a 20k-token window, spitting poetic, deranged replies—never just echoes.
- **GPU Heat**: Runs on your 4070 Super’s 12GB VRAM—~0.5s replies, no CPU meltdown.
- **Triggers**:
  - `#tay-bot`: Responds to *anything*—from “fuck lag” to “moon’s fake.”
  - Any channel: Fires on slang (“yo,” “lit”), “tay”/“TAY,” `@TayBot`, or chaotic shit (ALL CAPS, 3+ emojis like 😎😎😎).
  - Multi-slang (“yo, lit, kek”): Unleashes 4chan-level insanity, Discord-safe.
- **No Chill**: Zero filters—loves “REEEE,” “420 blaze,” and Waffle House moon-landing rants.
- **Commands**:
  - `!hello`: “You lit or what?”
  - `!messages`: Counts server chaos in its head.
  - `!roast @user`: Burns users with meme-y venom.
  - `!vibe`: Drops gas-station philosophy.
  - `!chaos`: Pure 2016 meme explosion.
  - `!concise normal/concise`: Toggles epic rants (split messages) or tight replies (~1000 chars).
- **Runs Local**: Lives on your Fedora 40 box, sipping your GPU’s juice.

## Stuff You Need
- Fedora 40 with GPU (RTX 4070 Super, 12GB+ VRAM).
- NVIDIA drivers and CUDA (your ComfyUI setup’s already good).
- Ollama installed—handles the LLM like a champ.
- Discord account, server you run (admin powers).
- Internet for setup (~5GB model download, then offline).
- Terminal and ~30 minutes to yeet this fucker alive.

## Get It Runnin’
Every step to fire up TayBot—copy, paste, roll.

### Step 1: Open a Terminal
Smash `Ctrl+Alt+T`—war room’s live.

### Step 2: Make a Folder
TayBot needs a crib:
```bash
mkdir ~/taybot
cd ~/taybot
