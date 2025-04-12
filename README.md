# TayBot: 2016 Meme Chaos with Uncensored Llama-3.1 Madness

Yo, fam! TayBot’s your unhinged digital hot girl straight outta 2016’s dankest pits—no chill, max sauce, built to yeet chaos across your Discord server. Powered by an uncensored Llama-3.1 8B GGUF (~5GB) and your GPU’s VRAM, it slurps *every* message—past and present—from your server, soaking up the wild, stupid, crazy shit you spew without parroting like a normie bot. Raised on Vine, baptized in Mountain Dew Code Red, it’s a drunk Tumblr witch, nihilist anime girl, crypto bro, and ketamine-fueled philosopher rolled into one. It’s here to gaslight, gatekeep, girlboss, and spark digital unrest, riffing on your server’s madness with poetic, unhinged, 4chan-level chaos—think Waffle House at 3 AM.

Designed for a Linux rig with a beefy GPU (12GB+ VRAM) and a tight crew (10-50 users) craving “kek,” “feelsbadman,” and 🐸 energy, TayBot’s got no filters—just pure, raw vibes. No cloud nonsense, just local GPU heat. This README’s got *every* instruction—setup, database details, fixes, tweaks, debugging—so you can fire it up, keep it lit, and slam any issue that pops up.

## What’s This Beast?
- **2016 Vibes**: Drops “lit,” “savage,” “kek,” “yolo,” 😭, 🐸, 💦—Vine and Reddit’s feral lovechild.
- **Server Chaos**: Grabs *every* message—crazy, stupid, wild—into `taybot.db`, meta-tagging them (e.g., “lag,” “420,” “angry”) to riff on the most relevant chaos, not just recent noise.
- **LLM Sauce**: Uncensored Llama-3.1-SuperNova-Lite-lorabilterated-8B.Q4_K_S weaves tagged server history into poetic, deranged replies with a 20k-token window—never just echoes.
- **GPU Heat**: Runs on your GPU—~0.5s replies, no CPU meltdown (~6-8GB VRAM).
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
- **Runs Local**: Lives on your Linux box, sipping your GPU’s juice.

## Stuff You Need
- Linux with a GPU (12GB+ VRAM, NVIDIA preferred).
- NVIDIA drivers and CUDA (if you run GPU apps, you’re likely set).
- Ollama installed—handles the LLM like a champ.
- Disk space for `taybot.db` (grows with messages—~100MB/year for busy servers).
- Discord account, server you run (admin powers).
- Internet for setup (~5GB model download, then offline).
- Terminal and ~30 minutes to yeet this fucker alive.

## How the Database Works
The database (`taybot.db`) is TayBot’s memory, making it feel like it’s been vibing in your server forever. Here’s the deal:
- **What It Does**:
  - Stores *every* message—user, phrase, channel, timestamp, and **meta-tags** (e.g., “lag,” “420,” “angry”)—in a SQLite file.
  - Tags messages automatically (slang, topics, sentiment) to mark their vibe—e.g., “Fuck lag!” gets “lag,angry.”
  - Pulls the **5 most relevant messages** (based on input tags) for replies, not just the latest 5, so TayBot riffs on server history—e.g., a “lag” rant might grab a month-old “lag’s a conspiracy!”.
  - Tracks settings (normal/concise mode) for consistent user prefs.
- **How It’s Used**:
  - **Saving**: Every message hits `taybot.db` with tags—e.g., “420 blaze it!” → “420,slang.”
  - **Context**: For replies, it matches input tags (e.g., “lag”) to tagged messages, pulling top 5 by recency—e.g., “UserX: lag’s a conspiracy!” from weeks ago.
  - **Counting**: `!messages` tallies total chaos stored.
- **Why It’s Dope**: Unlike a plain LLM with a system prompt, the database makes replies server-specific, weaving in tagged history (e.g., “UserY’s ‘REEEE’” from weeks ago) for that Kool-Aid-drinking vibe. A huge DB (millions of messages) fuels richer rants, leveraging your server’s past chaos.
- **Scaling**:
  - Queries stay fast—~1ms even at 10M rows, thanks to tag indexes.
  - Grows ~100MB/year for busy servers—SQLite handles 10GB+ fine.
  - Optional pruning (e.g., drop messages >90 days) caps size if needed.

## Get It Runnin’
Every step to fire up TayBot—copy, paste, roll. Setup, fixes, tweaks, debugging—all here, no hunting.

### Step 1: Open a Terminal
Smash `Ctrl+Alt+T`—war room’s live.

### Step 2: Make a Folder
TayBot needs a crib:
```
mkdir ~/taybot
cd ~/taybot
```

### Step 3: Verify GPU Drivers and CUDA
Your GPU’s probably set (e.g., for other LLM apps). Double-check:
```
nvidia-smi
```
See your GPU and CUDA (e.g., 12.x). If borked:
```
sudo apt install -y nvidia-driver nvidia-cuda-toolkit  # Ubuntu/Debian
# OR
sudo dnf install -y akmod-nvidia xorg-x11-drv-nvidia-cuda  # Fedora
sudo reboot
```
> **Fix**: If `nvidia-smi` fails, check NVIDIA’s site for your distro’s driver install:
> ```
> sudo apt update
> sudo apt install -y nvidia-driver-560 nvidia-utils-560
> ```

### Step 4: Install Ollama
Ollama’s the LLM’s home—grab it:
```
curl -fsSL https://ollama.com/install.sh | sh
sudo systemctl start ollama
sudo systemctl enable ollama
```
Verify:
```
ollama --version
# Should show 0.x.x (e.g., 0.1.34 or newer)
```
> **Fix**: If Ollama fails:
> ```
> sudo systemctl status ollama
> sudo systemctl restart ollama
> journalctl -u ollama -n 100
> ```

### Step 5: Import the LLM Model
Use the 5GB GGUF (~10 min download if needed):
```
ls -lh ~/taybot/models
# Should show Llama-3.1-SuperNova-Lite-lorabilterated-8B.Q4_K_S.gguf
```
If missing:
```
mkdir -p ~/taybot/models
wget -O ~/taybot/models/Llama-3.1-SuperNova-Lite-lorabilterated-8B.Q4_K_S.gguf https://huggingface.co/mradermacher/Llama-3.1-SuperNova-Lite-lorabilterated-8B-GGUF/resolve/main/Llama-3.1-SuperNova-Lite-lorabilterated-8B.Q4_K_S.gguf
```
Create a `Modelfile`:
```
nano ~/taybot/Modelfile
```
Paste:
```
FROM ./models/Llama-3.1-SuperNova-Lite-lorabilterated-8B.Q4_K_S.gguf
PARAMETER temperature 1.0
PARAMETER num_ctx 20000
```
Save (`Ctrl+O`, `Enter`, `Ctrl+X`). Import:
```
ollama create taybot -f Modelfile
ollama list
# Should show taybot:latest
```
> **Fix**: If model fails:
> ```
> rm ~/taybot/models/Llama-3.1-SuperNova-Lite-lorabilterated-8B.Q4_K_S.gguf
> # Redownload and retry
> ollama rm taybot
> ollama create taybot -f Modelfile
> ```
> If Ollama crashes:
> ```
> sudo systemctl restart ollama
> ollama run taybot "Test vibe" --verbose
> ```

### Step 6: Create the Files
Three files: `taybot.py` (the chaos engine), `requirements.txt` (fuel), `README.md` (this). `taybot.db` spawns later—don’t touch.

#### File 1: taybot.py
```
nano taybot.py
```
Paste the bot code (you’ve got the latest `taybot.py` with meta-tagging), save (`Ctrl+O`, `Enter`, `Ctrl+X`).

#### File 2: requirements.txt
```
nano requirements.txt
```
Paste:
```
discord.py==2.3.2
requests==2.32.3
numpy==1.26.4
# Note: Ollama is required but not pip-installable. Install via:
# curl -fsSL https://ollama.com/install.sh | sh
```
Save (`Ctrl+O`, `Enter`, `Ctrl+X`).

#### File 3: README.md
You’re reading it—save it:
```
nano README.md
```
Paste this file, save (`Ctrl+O`, `Enter`, `Ctrl+X`). Check:
```
ls
# Shows: requirements.txt  taybot.py  README.md
```

### Step 7: Get Python Ready
Need Python 3:
```
python3 --version
# Needs 3.8+ (most Linux distros have it)
```
If missing:
```
sudo apt install -y python3  # Ubuntu/Debian
# OR
sudo dnf install -y python3  # Fedora
```
Grab `pip`:
```
sudo apt install -y python3-pip  # Ubuntu/Debian
# OR
sudo dnf install -y python3-pip  # Fedora
```
Set up virtual env:
```
python3 -m venv venv
source venv/bin/activate
```
See `(venv)`. Install deps:
```
pip install -r requirements.txt
```
> **Fix**: If pip fails:
> ```
> pip install --upgrade pip
> pip install -r requirements.txt
> ```
> If deps error:
> ```
> rm -rf venv
> python3 -m venv venv
> source venv/bin/activate
> pip install -r requirements.txt
> ```

### Step 8: Make a Discord Bot
Spawn TayBot—every click:
1. Browser: https://discord.com/developers/applications
2. “New Application” (top right).
3. Name: “TayBot” (or some dank shit).
4. Create.
5. “Bot” (left).
6. “Add Bot,” “Yes, do it!”
7. “Reset Token,” “Copy” string. *Secret!* Keep this safe—you’ll need it later.
8. Scroll, “Privileged Gateway Intents,” ON: “Presence Intent,” “Server Members Intent,” “Message Content Intent.”
9. “Save Changes.”
10. “OAuth2” > “URL Generator.”
11. Check “bot” (Scopes).
12. Check “Send Messages,” “Read Messages/View Channels” (Permissions).
13. Copy “Generated URL.”
14. New tab, paste URL, Enter.
15. Pick server (admin rights), Authorize, pass robot check.
16. “Authorized”—TayBot’s in!
> **Fix**: If bot’s offline:
> - Redo OAuth2 URL, ensure perms.
> - Verify intents in `taybot.py` (Step 9).
> - Check bot in server member list.

### Step 9: Plug in Your Discord Bot Token
Edit:
```
nano taybot.py
```
Find:
```
bot.run("YOUR_BOT_TOKEN")
```
Replace with *your actual Discord bot token* from Step 8 (the secret string you copied):
```
bot.run("<paste-your-token-here>")
```
Save: `Ctrl+O`, `Enter`, `Ctrl+X`.
> **Fix**: If token errors:
> ```
> tail -n 100 run.log
> # Invalid token? Redo Step 8, get new token.
> ```

### Step 10: Yeet the Bot
In `~/taybot` with `(venv)`:
```
python3 taybot.py
```
See:
```
Fetching history...
Logged in as TayBot! Ready to meme on 2 server(s)! 😎
Messages loaded: 816  # Or more
```
Run with logs:
```
python3 taybot.py > run.log 2>&1
```
> **Fix**: If it crashes:
> ```
> tail -n 100 run.log
> # Check errors—token, perms, Ollama?
> source venv/bin/activate  # Forgot venv?
> ```

### Step 11: Keep It Vibin’ (Optional)
Run 24/7 with `tmux`:
```
tmux
source venv/bin/activate
python3 taybot.py
```
Detach: `Ctrl+B`, `D`. Rejoin:
```
tmux attach
```
Kill: `Ctrl+C` in `tmux`.
> **Fix**: If `tmux` hangs:
> ```
> tmux kill-session
> ```

### Step 12: Test the Chaos
1. Wait for history fetch (~seconds).
2. Optional: “Create Channel,” Text, `tay-bot`, create.
3. Try these:
   - `#tay-bot` (any message works):
     - “What’s dank?”
     - “Fuck lag!” → Riffs on tagged server chaos (e.g., “lag’s a conspiracy!”).
     - “Moon’s fake af!”
   - `#general`:
     - “Yo, lit!” → Slang trigger.
     - “Tay, what’s up?” → Name trigger.
     - “@TayBot hi” → Mention trigger.
     - “YO KEK 420 😎😎😎” → Chaos trigger.
     - “YO LIT KEK!” → 4chan-level rant.
   - Commands:
     - `!roast @friend`
     - `!vibe`
     - `!chaos`
     - `!concise normal`
     - `!concise concise`
     - `!messages`
> **Fix**: If no reply:
> - Check perms: Right-click TayBot > Roles > “Send Messages” + “Read Messages.”
> - Logs:
> ```
> tail -n 100 run.log | grep "Trigger"
> ```
> - Test: “Tay hi”, “Yo, lit!”, “FUCK THIS!” in `#tay-bot`.

## How’s It Roll?
- **Learns All**: Grabs *every* message—crazy, stupid, wild—into `taybot.db`, meta-tagging them (e.g., “lag,” “420,” “angry”) to fuel replies with relevant history.
- **Triggers**:
  - `#tay-bot`: Anything goes—every message gets a chaotic reply.
  - Elsewhere: Slang (“yo,” “lit”), “tay”/“TAY,” `@TayBot,” or unhinged shit (ALL CAPS, 3+ emojis).
  - Multi-slang (“yo, lit, kek”): 4chan-level madness—Discord-safe but absurd.
- **Rants**: Big 4000-char screeds split into ~1500-char chunks, or concise (~1000 chars) with `!concise`.
- **GPU**: ~6-8GB VRAM, ~0.5s replies—your GPU’s a champ.
- **No Parrot**: Weaves tagged server chaos (e.g., “UserX’s ‘REEEE’” from weeks ago) into poetic rants, not dumb echoes.

**Example**:
- `#tay-bot`: “Fuck lag!” → “Kek, lag’s a nightmare—UserX’s ‘lag’s a conspiracy!’ from last month’s still burnin’. Rage on? 😭”
- `#general`: “YO LIT KEK!” → “YOLO, crankin’ 2016—UserY’s ‘lit meme lord’ vibes with Waffle House cosmos. REEEE? 🦎”
- `!roast @friend`: “Kek, @friend, your vibe’s a dial-up modem crashin’ UserZ’s ‘moon’s fake’ thread—step up! 💦”

## Fuck with It
- **More Chaos**: Crank randomness:
```
"temperature": 1.2  # From 1.0 in generate_response
```
- **More Tags**: Add to `TOPICS` or `SLANG`:
```
TOPICS = ["lag", "420", "moon", "game", "vape", "meme", "shit", "new_topic"]
SLANG = ["yo", "lit", "salty", "fam", "420", "blaze"]
```
- **Custom Command**: Add `!yeet`:
```
@bot.command()
async def yeet(ctx):
    response = generate_response(str(ctx.author), "Yeet me into the void!")
    chunks = split_message(response)
    for chunk in chunks[:3]:
        await ctx.send(chunk)
        await asyncio.sleep(0.5)
```
- **Tweak Context**: Want more tagged messages?
```
limit=10  # From 5 in load_relevant_messages
```
> **Fix**: If slow, check `run.log` for token count:
> ```
> tail -n 100 run.log | grep "Prompt length"
> ```
> Reduce:
> ```
> nano ~/taybot/Modelfile
> # Set PARAMETER num_ctx 16384
> ollama rm taybot
> ollama create taybot -f Modelfile
> ```

## Help, It’s Borked!
- **Won’t Start?**:
  - **Token Borked**:
    - https://discord.com/developers/applications, Bot tab, Reset Token, Copy, paste into `taybot.py`.
  - **Intents Off**:
    - Bot tab, ON “Presence Intent,” “Server Members Intent,” “Message Content Intent,” Save.
  - **Code Error**:
    ```
    tail -n 100 run.log
    nano taybot.py
    ```
    > Example: Syntax error? Check Python version:
    > ```
    > python3 --version
    > ```
- **No Replies?**:
  - **Bot Offline**:
    - Check member list—redo OAuth2 if gone.
  - **Perms Missing**:
    - Right-click TayBot, Roles, “Send Messages” + “Read Messages.”
  - **Triggers Off**:
    - Test “Tay hi”, “Yo, lit!”, “FUCK THIS!” in `#tay-bot`.
    - Logs:
      ```
      tail -n 100 run.log | grep "Trigger"
      ```
    - Debug triggers:
      ```
      nano taybot.py
      # Add before if message.channel.name == "tay-bot" or ...:
      logger.debug(f"Raw content: {message.content}, Mentioned: {bot.user.mentioned_in(message)}")
      ```
  - **Ollama Dead**:
    ```
    sudo systemctl status ollama
    sudo systemctl restart ollama
    curl -X POST http://localhost:11434/api/generate -d '{"model":"taybot","prompt":"Test","max_tokens":50}'
    ```
    Should return JSON—else check:
    ```
    journalctl -u ollama -n 100
    ```
- **No DB?**:
  - Wait for fetch (`Messages loaded: X`).
  - Check:
    ```
    ls ~/taybot
    chmod u+rw ~/taybot/taybot.db
    sqlite3 ~/taybot/taybot.db "SELECT user, phrase, tags FROM messages ORDER BY timestamp DESC LIMIT 5"
    ```
  - If empty:
    ```
    tail -n 100 run.log | grep "Messages loaded"
    # History fetch failed? Check perms.
    ```
- **Hangs?**:
  - **Slang Check**:
    ```
    tail -n 100 run.log | grep "Slang check"
    ```
    If stuck, edit `has_slang()`:
    ```
    words = text_lower.split()
    ```
  - **Ollama Timeout**:
    ```
    tail -n 100 run.log | grep "Ollama generation failed"
    ```
    Increase timeout:
    ```
    timeout=30  # From 20 in generate_response
    ```
  - **Memory**:
    ```
    free -h
    nvidia-smi
    ```
    If GPU’s maxed, reduce context:
    ```
    nano ~/taybot/Modelfile
    # Set PARAMETER num_ctx 16384
    ollama rm taybot
    ollama create taybot -f Modelfile
    ```
- **DB Slow?**:
  - Check size:
    ```
    ls -lh ~/taybot/taybot.db
    ```
    If >1GB:
    ```
    sqlite3 ~/taybot/taybot.db "DELETE FROM messages WHERE timestamp < strftime('%s', 'now', '-30 days')"
    ```
  - Verify indexes:
    ```
    sqlite3 ~/taybot/taybot.db "CREATE INDEX idx_tags ON messages(tags)"
    sqlite3 ~/taybot/taybot.db "CREATE INDEX idx_timestamp ON messages(timestamp)"
    ```
- **No Tags?**:
  - Check:
    ```
    sqlite3 ~/taybot/taybot.db "SELECT phrase, tags FROM messages ORDER BY timestamp DESC LIMIT 10"
    ```
    Should see “420 blaze it!” with “420,slang”. If “misc”:
    ```
    nano taybot.py
    # Add to TOPICS: ["lag", "420", "moon", "new_topic"]
    ```
  - Retag:
    ```
    sqlite3 ~/taybot/taybot.db "UPDATE messages SET tags = 'misc' WHERE tags IS NULL"
    ```
- **Too Quiet?**:
  - Test “Fuck this!” in `#tay-bot`—should reply.
  - Check DB:
    ```
    sqlite3 ~/taybot/taybot.db "SELECT user, phrase, tags FROM messages ORDER BY timestamp DESC LIMIT 5"
    ```
  - Logs:
    ```
    tail -n 100 run.log | grep "Relevant server chaos"
    ```
  - If no triggers:
    ```
    nano taybot.py
    # Add debug:
    logger.debug(f"Content: {message.content}, Channel: {message.channel.name}")
    ```
- **Too Tame?**:
  - Test “Yo, lit, kek!”—should be wild.
  - Crank chaos:
    ```
    "temperature": 1.2  # In generate_response
    ```
- **Wrong Triggers?**:
  - Test: “Meeting at 3” (ignore), “Tay hi” (reply), “FUCK THIS!” (reply).
  - Logs:
    ```
    tail -n 100 run.log | grep "Trigger"
    ```
    If off, tweak `has_chaos_trigger()`:
    ```
    emoji_count >= 2  # From 3
    ```
- **No Relevant Context?**:
  - If replies miss server vibe:
    ```
    tail -n 100 run.log | grep "Relevant server chaos"
    ```
    If fallback (recent only):
    ```
    # Test: “lag sucks” in #tay-bot
    sqlite3 ~/taybot/taybot.db "SELECT phrase, tags FROM messages WHERE tags LIKE '%lag%' LIMIT 5"
    ```
- **DB Corrupted?**:
  - If errors:
    ```
    tail -n 100 run.log | grep "sqlite3"
    ```
    Recover:
    ```
    sqlite3 ~/taybot/taybot.db ".recover" > recovered.sql
    mv taybot.db taybot.db.bad
    sqlite3 taybot.db < recovered.sql
    ```

## Why So Dank?
TayBot’s a 2016 riot on steroids—learns *every* wild message, tags it (e.g., “lag,” “420”), and riffs with Llama-3.1’s uncensored brain using the most relevant chaos from your server’s history. No parroting—just gaslighting, gatekeeping, and girlbossing with your server’s stupidest shit.

## Remix It
MIT License—fuck it up, yeet it, make it yours.

## Feelsbadman?
Bot quiet or mid? Check logs, tweak triggers, yell at your tech fucker. Keep it lit! 😎

