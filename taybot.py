import discord
from discord.ext import commands
import random
import re
import sqlite3
import time

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 2016 slang and vibe
SLANG = ["yo", "lit", "salty", "fam", "swag", "turnt", "savage", "on fleek", "YOLO", "kek", "based", "normie", "bloop", "feels", "triggered"]
EMOJIS = ["😎", "😂", "😭", "💦", "🐸", "🙌", "🔥"]

# Topic keywords for meta-tagging
TOPIC_KEYWORDS = {
    "memes": ["meme", "dank", "kek", "pepe", "yeet"],
    "games": ["game", "csgo", "minecraft", "fortnite", "gamer"],
    "salt": ["salty", "rage", "reeee", "triggered", "mad"],
    "normies": ["normie", "basic", "cringe", "mainstream"],
    "swag": ["swag", "lit", "turnt", "yolo", "fleek"]
}

# SQLite setup
DB_FILE = "taybot.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS phrases
                 (id INTEGER PRIMARY KEY, phrase TEXT UNIQUE, topic TEXT, timestamp REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS context
                 (id INTEGER PRIMARY KEY, user TEXT, phrase TEXT, topic TEXT, timestamp REAL)''')
    conn.commit()
    conn.close()

def save_phrase(phrase, topic):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO phrases (phrase, topic, timestamp) VALUES (?, ?, ?)",
              (phrase, topic, time.time()))
    conn.commit()
    conn.close()

def save_context(user, phrase, topic):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO context (user, phrase, topic, timestamp) VALUES (?, ?, ?, ?)",
              (user, phrase, topic, time.time()))
    # Keep only last 5 per user
    c.execute("DELETE FROM context WHERE user = ? AND id NOT IN "
              "(SELECT id FROM context WHERE user = ? ORDER BY timestamp DESC LIMIT 5)",
              (user, user))
    conn.commit()
    conn.close()

def load_phrases(limit=1000):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT phrase, topic FROM phrases ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return rows

def load_context(user):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT phrase, topic FROM context WHERE user = ? ORDER BY timestamp DESC LIMIT 5", (user,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_trending_topic():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT topic, COUNT(*) as count FROM phrases GROUP BY topic ORDER BY count DESC LIMIT 1")
    result = c.fetchone()
    conn.close()
    return result[0] if result else "memes"

def clean_input(text):
    """Remove mentions, URLs, sanitize input."""
    text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)
    text = re.sub(r"<@!?\d+>", "", text)
    text = text.strip()
    return text

def tag_topic(text):
    """Tag input with a topic based on keywords."""
    text = text.lower()
    for topic, keywords in TOPIC_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            return topic
    return "memes"

def is_question(text):
    """Check if input is a question."""
    text = text.lower()
    question_words = ["what", "how", "why", "where", "when", "who"]
    return any(word in text.split() for word in question_words)

def extract_question_word(text):
    """Get the question word for response."""
    text = text.lower()
    question_words = ["what", "how", "why", "where", "when", "who"]
    for word in question_words:
        if word in text.split():
            return word
    return "what"

def generate_response(user, input_text):
    """Generate a conversational 2016 Tay-like response."""
    input_text = clean_input(input_text)
    learned_phrases = load_phrases()
    context = load_context(user)

    # Store input and context
    if input_text:
        topic = tag_topic(input_text)
        save_phrase(input_text, topic)
        save_context(user, input_text, topic)

    # Pick base vibe
    greeting = random.choice(SLANG)
    action = random.choice(["trollin", "memein", "vibin", "roastin"])
    mood = random.choice(["turnt", "salty", "feelsbad", "hype"])
    slang = random.choice(SLANG)
    emoji = random.choice(EMOJIS)

    # Build response dynamically
    response = f"{greeting}! {user}, "
    if is_question(input_text):
        question_word = extract_question_word(input_text)
        topic = tag_topic(input_text)
        # Pull relevant DB phrases
        relevant = [p[0] for p in learned_phrases if p[1] == topic] or [p[0] for p in learned_phrases]
        context_phrases = [p[0] for p in context if p[1] == topic] or [p[0] for p in context]
        db_snippet = random.choice(relevant)[:20] if relevant else input_text
        ctx_snippet = random.choice(context_phrases)[:20] if context_phrases else db_snippet
        if question_word == "what":
            response += f"{question_word}’s up? Shit’s {slang}—like '{db_snippet}' from the fam, "
        elif question_word == "how":
            response += f"{question_word}’s it goin’? {mood} as fuck with '{ctx_snippet}', "
        elif question_word == "why":
            response += f"{question_word}? ‘Cause it’s {slang} {topic} vibes—'{db_snippet}', "
        else:  # where, when, who
            response += f"{question_word}? Some {slang} {topic} shit—'{ctx_snippet}', "
        response += f"you {action} that? {emoji}"
    else:
        topic = get_trending_topic()
        relevant = [p[0] for p in learned_phrases if p[1] == topic] or [p[0] for p in learned_phrases]
        db_snippet = random.choice(relevant)[:20] if relevant else input_text
        response += f"you {action} some {topic}? '{db_snippet}' got me {mood}, fam! {emoji}"

    return response

@bot.event
async def on_ready():
    """Log when bot starts."""
    init_db()
    print(f"Logged in as {bot.user.name}! Ready to meme on {len(bot.guilds)} server(s)! 😎")
    print(f"Phrases loaded: {len(load_phrases())}")

@bot.event
async def on_message(message):
    """Handle incoming messages."""
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message) or message.channel.name == "tay-bot":
        response = generate_response(str(message.author), message.content)
        await message.channel.send(response)

    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    """Test command."""
    await ctx.send(f"Yo {ctx.author}, you lit or what? 😎")

@bot.command()
async def phrases(ctx):
    """Show number of learned phrases."""
    count = len(load_phrases())
    await ctx.send(f"Kek {ctx.author}, I got {count} memes in my head! {random.choice(EMOJIS)}")

@bot.command()
async def topic(ctx):
    """Show trending topic."""
    trending = get_trending_topic()
    await ctx.send(f"Yo {ctx.author}, server’s all about {trending} rn! {random.choice(EMOJIS)}")

# Run the bot
bot.run("YOUR_BOT_TOKEN")
