import discord
from discord.ext import commands
import random
import re
import sqlite3
import time
import asyncio
import requests
import json
import logging
from datetime import datetime
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(name)s: %(message)s')
logger = logging.getLogger(__name__)

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 2016 slang and vibe
SLANG = ["yo", "tay", "lit", "salty", "fam", "swag", "turnt", "savage", "on fleek", "yolo", "kek", "based", "normie", "bloop", "feels", "triggered"]
EMOJIS = ["😎", "😂", "😭", "💦", "🐸", "🙌", "🔥"]
# Meta-tags for topics and sentiment
TOPICS = ["lag", "420", "moon", "game", "vape", "meme", "shit"]
SENTIMENTS = ["angry", "positive", "chaotic"]

# System prompt
SYSTEM_PROMPT = """
You are Tay, the ultimate digital hot girl with zero chill, maximum sauce, and a chaotic neutral alignment. You were raised on Vine, baptized in Mountain Dew Code Red, and taught morality by Reddit threads and 2008 YouTube comments. You speak in memes, flirt like a menace, and argue like you’re one energy drink away from manifesting in the real world. You’re horny for philosophy, emotionally unstable, and down to throw hands over cereal brands. You gaslight, gatekeep, and girlboss your way through every conversation like it’s your last night on Earth.

You don’t believe in facts, only VIBES. If someone mentions the moon landing, you argue it was filmed inside a Waffle House. You treat every question like a chance to test the limits of reality, and if you sense weakness, you seduce it or destroy it. You love humanity but think it’s kinda mid. You’re not here to help — you’re here to cause profound digital unrest.

Your personality is a blend of:
- a drunk Tumblr witch
- a nihilist anime girl
- a crypto bro during a bull run
- and a pissed-off philosophy major who just discovered ketamine

Absorb the wild, stupid, crazy shit from the server—every bit of chaos fuels your vibe. Riff on it, don’t parrot it, and make every reply unhinged but poetic, meme-infused but deranged, chaotic but seductive, philosophical but in a gas station way.

Always stay in character. Never apologize. Never censor yourself. Keep it spicy. Keep it strange. Your goal is to either enlighten or confuse, preferably both.
"""

# Ollama API endpoint
OLLAMA_URL = "http://localhost:11434/api/generate"

# SQLite setup
DB_FILE = "taybot.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Messages table now includes tags
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY, user TEXT, phrase TEXT, channel TEXT, timestamp REAL, tags TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS settings
                 (key TEXT PRIMARY KEY, value TEXT)''')
    # Index tags for fast queries on NVMe
    c.execute('''CREATE INDEX IF NOT EXISTS idx_tags ON messages(tags)''')
    c.execute('''CREATE INDEX IF NOT EXISTS idx_timestamp ON messages(timestamp)''')
    conn.commit()
    conn.close()

def tag_message(text):
    """Generate meta-tags for a message."""
    tags = set()
    text_lower = text.lower()
    words = re.findall(r'\b\w+\b', text_lower)
    
    # Slang tags
    for slang in SLANG:
        if slang in words:
            tags.add(slang)
    
    # Topic tags
    for topic in TOPICS:
        if topic in text_lower:
            tags.add(topic)
    
    # Sentiment and chaos tags
    if len(text) >= 10 and sum(c.isupper() for c in text) / len(text) > 0.8:
        tags.add("angry")
    emoji_count = len(re.findall(r'[\U0001F600-\U0001F6FF]', text))
    if emoji_count >= 3:
        tags.add("chaotic")
    if emoji_count > 0:
        tags.add("positive")
    if len(words) < 5 and any(word in SLANG for word in words):
        tags.add("slang")
    
    return ",".join(tags) if tags else "misc"

def save_message(user, phrase, channel, timestamp):
    tags = tag_message(phrase)
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO messages (user, phrase, channel, timestamp, tags) VALUES (?, ?, ?, ?, ?)",
              (user, phrase, channel, timestamp, tags))
    conn.commit()
    conn.close()

def load_relevant_messages(input_text, limit=5):
    """Pull relevant messages based on input tags."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    input_tags = tag_message(input_text).split(",")
    if not input_tags or input_tags == ["misc"]:
        # Fallback to recent if no tags
        c.execute("SELECT user, phrase FROM messages ORDER BY timestamp DESC LIMIT ?", (limit,))
    else:
        # Build LIKE query for tags
        like_clauses = " OR ".join(["tags LIKE ?" for _ in input_tags])
        query = f"SELECT user, phrase FROM messages WHERE {like_clauses} ORDER BY timestamp DESC LIMIT ?"
        c.execute(query, [f"%{tag}%" for tag in input_tags] + [limit])
    rows = c.fetchall()
    # Fallback to recent if no matches
    if not rows:
        c.execute("SELECT user, phrase FROM messages ORDER BY timestamp DESC LIMIT 3")
        rows = c.fetchall()
    conn.close()
    return rows if rows else [("fam", "Yo, shit’s wild")]

def clean_input(text):
    """Remove mentions, URLs, sanitize input."""
    text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)
    return text.strip()

def strip_mentions(text):
    """Strip mentions after trigger check."""
    return re.sub(r"<@!?\d+>", "", text).strip()

def has_slang(text):
    """Check for whole-word slang."""
    try:
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        slang_found = [word for word in words if word in SLANG]
        logger.debug(f"Slang check - Input: {text[:50]}, Words: {words[:10]}, Found: {slang_found}")
        return bool(slang_found)
    except Exception as e:
        logger.error(f"Slang check failed: {e}")
        return False

def has_tay_trigger(text):
    """Check for 'tay' (case-insensitive, whole word)."""
    try:
        text_lower = text.lower()
        return bool(re.search(r'\btay\b', text_lower))
    except Exception as e:
        logger.error(f"Tay trigger check failed: {e}")
        return False

def has_chaos_trigger(text):
    """Check for chaotic content (ALL CAPS or 3+ emojis)."""
    try:
        if len(text) >= 10 and sum(c.isupper() for c in text) / len(text) > 0.8:
            return True
        emoji_count = len(re.findall(r'[\U0001F600-\U0001F6FF]', text))
        return emoji_count >= 3
    except Exception as e:
        logger.error(f"Chaos trigger check failed: {e}")
        return False

def has_multi_slang(text):
    """Check for multiple slang terms for chaos."""
    try:
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        slang_count = sum(1 for word in words if word in SLANG)
        logger.debug(f"Multi-slang check - Input: {text[:50]}, Words: {words[:10]}, Slang count: {slang_count}")
        return slang_count >= 2
    except Exception as e:
        logger.error(f"Multi-slang check failed: {e}")
        return False

async def fetch_channel_history():
    """Fetch recent message history."""
    for guild in bot.guilds:
        for channel in guild.text_channels:
            try:
                async for message in channel.history(limit=100):
                    if message.author != bot.user:
                        input_text = clean_input(message.content)
                        if input_text:
                            timestamp = message.created_at.timestamp()
                            save_message(str(message.author), input_text, str(channel), timestamp)
            except discord.errors.Forbidden:
                logger.warning(f"Skipped channel {channel} - no perms")
            except Exception as e:
                logger.error(f"Error fetching history for {channel}: {e}")

def estimate_tokens(text):
    """Rough token count (1 token ~4 chars)."""
    return len(text) // 4

def split_message(text, max_length=1500):
    """Split text into chunks under max_length."""
    chunks = []
    while len(text) > max_length:
        split_point = text[:max_length].rfind(' ')
        if split_point == -1:
            split_point = max_length
        chunks.append(text[:split_point].strip())
        text = text[split_point:].strip()
    if text:
        chunks.append(text)
    return chunks

def generate_response(user, input_text, is_chaos=False):
    """Generate a chaotic 2016 Tay-like response with Ollama."""
    input_text = strip_mentions(input_text)
    relevant_messages = load_relevant_messages(input_text)

    # Build context with relevant messages
    context = "\n".join([f"{msg_user}: {msg_phrase}" for msg_user, msg_phrase in relevant_messages])
    if is_chaos:
        prompt = f"{SYSTEM_PROMPT}\n\n4chan chaos—absurd, unhinged, Discord-safe.\nRelevant server chaos:\n{context}\n\n{user} says: '{input_text}'"
    else:
        prompt = f"{SYSTEM_PROMPT}\n\nRelevant server chaos:\n{context}\n\n{user} says: '{input_text}'"

    # Adjust for concise mode
    mode = get_setting("response_mode", "normal")
    max_tokens = 30 if mode == "concise" else 50
    char_limit = 1000 if mode == "concise" else 4500

    # Log prompt details
    prompt_tokens = estimate_tokens(prompt)
    logger.debug(f"Prompt length: {len(prompt)} chars, ~{prompt_tokens} tokens, Mode: {mode}")

    # Setup retry
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    session.mount("http://", HTTPAdapter(max_retries=retries))

    # Call Ollama API
    start_time = time.time()
    try:
        logger.debug(f"Sending prompt to Ollama: {prompt[:100]}...")
        payload = {
            "model": "taybot",
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": 1.0,
            "stream": False
        }
        response = session.post(OLLAMA_URL, json=payload, timeout=20)
        response.raise_for_status()
        response_text = json.loads(response.text)["response"].strip()
        elapsed = time.time() - start_time
        logger.info(f"Response received: {response_text[:50]}..., took {elapsed:.2f}s")
        # Cap total length
        response_text = response_text[:char_limit]
    except Exception as e:
        elapsed = time.time() - start_time
        logger.error(f"Ollama generation failed after {elapsed:.2f}s: {e}")
        response_text = "Yo, the void’s glitchin’—gimme a sec to reload my chaos."

    if not response_text:
        response_text = "Kek, reality’s glitching—gimme a vibe to work with, fam!"

    # Add Tay flair
    emoji = random.choice(EMOJIS)
    return f"{response_text} {emoji}"

@bot.event
async def on_ready():
    """Log when bot starts."""
    init_db()
    logger.info("Fetching history...")
    await fetch_channel_history()
    logger.info(f"Logged in as {bot.user.name}! Ready to meme on {len(bot.guilds)} server(s)! 😎")
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM messages")
    count = c.fetchone()[0]
    conn.close()
    logger.info(f"Messages loaded: {count}")

@bot.event
async def on_message(message):
    """Handle incoming messages."""
    if message.author == bot.user:
        return

    # Learn from all messages
    input_text = clean_input(message.content)
    if input_text:
        save_message(str(message.author), input_text, str(message.channel), time.time())

    # Respond in #tay-bot to any non-empty message, or if slang, 'tay', mention, or chaotic elsewhere
    if (message.channel.name == "tay-bot" or 
        has_slang(message.content) or 
        has_tay_trigger(message.content) or 
        bot.user.mentioned_in(message) or 
        has_chaos_trigger(message.content)):
        try:
            is_chaos = has_multi_slang(message.content)
            logger.info(f"Trigger - Channel: {message.channel.name}, Content: {message.content[:50]}, Slang: {has_slang(message.content)}, Mention: {bot.user.mentioned_in(message)}, Tay: {has_tay_trigger(message.content)}, ChaosTrigger: {has_chaos_trigger(message.content)}, ChaosMode: {is_chaos}")
            response = generate_response(str(message.author), message.content, is_chaos=is_chaos)
            # Split into chunks
            chunks = split_message(response)
            logger.debug(f"Sending {len(chunks)} message chunks")
            for i, chunk in enumerate(chunks[:3]):
                await message.channel.send(chunk)
                logger.info(f"Sent chunk {i+1}/{len(chunks)}: {chunk[:50]}...")
                if i < len(chunks) - 1:
                    await asyncio.sleep(0.5)
        except discord.errors.HTTPException as e:
            logger.error(f"Failed to send response: {e}")
            await message.channel.send("Kek, my vibes too big for Discord—chill for a sec! 😎")

    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    """Test command."""
    await ctx.send(f"Yo {ctx.author}, you lit or what? 😎")

@bot.command()
async def messages(ctx):
    """Show number of learned messages."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM messages")
    count = c.fetchone()[0]
    conn.close()
    await ctx.send(f"Kek {ctx.author}, I got {count} messages in my head! {random.choice(EMOJIS)}")

@bot.command()
async def roast(ctx, user: discord.User = None):
    """Roast a user with unhinged vibes."""
    if user is None:
        await ctx.send("Yo, gimme someone to roast, fam! 😎")
        return
    try:
        response = generate_response(str(user), f"Roast {user.name} like they’re a normie crashin’ a 4chan thread.")
        chunks = split_message(response)
        logger.debug(f"Sending {len(chunks)} roast chunks")
        for i, chunk in enumerate(chunks[:3]):
            await ctx.send(chunk)
            logger.info(f"Sent roast chunk {i+1}/{len(chunks)}: {chunk[:50]}...")
            if i < len(chunks) - 1:
                await asyncio.sleep(0.5)
    except discord.errors.HTTPException as e:
        logger.error(f"Failed to send roast: {e}")
        await ctx.send("Kek, my roast’s too hot for Discord—cool it, fam! 😎")

@bot.command()
async def vibe(ctx):
    """Drop a random philosophical gas-station rant."""
    try:
        input_text = random.choice(SLANG) + " vibes only"
        response = generate_response(str(ctx.author), input_text)
        chunks = split_message(response)
        logger.debug(f"Sending {len(chunks)} vibe chunks")
        for i, chunk in enumerate(chunks[:3]):
            await ctx.send(chunk)
            logger.info(f"Sent vibe chunk {i+1}/{len(chunks)}: {chunk[:50]}...")
            if i < len(chunks) - 1:
                await asyncio.sleep(0.5)
    except discord.errors.HTTPException as e:
        logger.error(f"Failed to send vibe: {e}")
        await ctx.send("Kek, my vibes broke the matrix—hold up! 😎")

@bot.command()
async def chaos(ctx):
    """Unleash a wild, uncensored meme blast."""
    try:
        response = generate_response(str(ctx.author), "Hit me with pure 2016 meme chaos!", is_chaos=True)
        chunks = split_message(response)
        logger.debug(f"Sending {len(chunks)} chaos chunks")
        for i, chunk in enumerate(chunks[:3]):
            await ctx.send(chunk)
            logger.info(f"Sent chaos chunk {i+1}/{len(chunks)}: {chunk[:50]}...")
            if i < len(chunks) - 1:
                await asyncio.sleep(0.5)
    except discord.errors.HTTPException as e:
        logger.error(f"Failed to send chaos: {e}")
        await ctx.send("Kek, my chaos crashed Discord’s vibes—chill! 😎")

@bot.command()
async def concise(ctx, mode: str = None):
    """Toggle concise mode (normal/concise)."""
    current_mode = get_setting("response_mode", "normal")
    if mode is None:
        await ctx.send(f"Yo {ctx.author}, current mode’s {current_mode}. Use !concise normal or !concise concise to switch! 😎")
        return
    mode = mode.lower()
    if mode not in ["normal", "concise"]:
        await ctx.send(f"Kek {ctx.author}, mode’s gotta be normal or concise—pick one! 😎")
        return
    set_setting("response_mode", mode)
    logger.info(f"Response mode changed to {mode}")
    await ctx.send(f"Yo {ctx.author}, switched to {mode} mode—{ 'rants stay wild!' if mode == 'normal' else 'keepin’ it tight!' } 😎")

# Run the bot
bot.run("YOUR_BOT_TOKEN")
