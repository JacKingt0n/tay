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
TEMPLATES = [
    "{greeting}! What’s good, {user}? You {mood} over {input}? {emoji}",
    "Yo {user}, you {action} some {topic} shit like '{input}'? Feels {feels}! {emoji}",
    "Kek! {user}, you vibin’ with '{input}'? That’s {slang} af, fam! {emoji}",
    "Bloop! {user} be {mood}, mixin’ {topic} with '{input}'—{slang} as hell! {emoji}",
    "Top kek, {user}! You {action} like a {slang} {topic} normie with '{input}'? {emoji}",
]
QUESTION_TEMPLATES = [
    "Yo {user}, {question_word}? It’s {slang} as fuck—check '{input}' from the fam! {emoji}",
    "Kek, {user}! {question_word}’s up? Server’s all about {topic}—like '{input}'! {emoji}",
    "Bloop! {user}, {question_word}? Easy—{slang} chaos with '{input}'! {emoji}",
    "Yo {user}, {question_word}’s the deal? Shit’s {mood} on {topic}, think '{input}'! {emoji}",
    "Top kek, {user}! {question_word}? Just some {slang} {topic} vibes—'{input}'! {emoji}",
]

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
    conn.commit()
    conn.close()

def save_phrase(phrase, topic):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO phrases (phrase, topic, timestamp) VALUES (?, ?, ?)",
              (phrase, topic, time.time()))
    conn.commit()
    conn.close()

def load_phrases(limit=1000):  # Upped to 1000 for more pool
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT phrase, topic FROM phrases ORDER BY timestamp DESC LIMIT ?", (limit,))
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
    """Generate a 2016 Tay-like response."""
    input_text = clean_input(input_text)
    learned_phrases = load_phrases()

    # Store any non-empty input with topic
    if input_text:
        topic = tag_topic(input_text)
        save_phrase(input_text, topic)

    # Pick template based on question or not
    if is_question(input_text):
        template = random.choice(QUESTION_TEMPLATES)
        question_word = extract_question_word(input_text)
        topic = tag_topic(input_text)  # Use input topic for questions
    else:
        template = random.choice(TEMPLATES)
        question_word = "what"
        topic = get_trending_topic()

    # Fill dynamic parts
    greeting = random.choice(SLANG)
    action = random.choice(["trollin", "memein", "vibin", "roastin"])
    mood = random.choice(["turnt", "salty", "feelsbad", "hype"])
    feels = random.choice(["good", "bad", "weird", "savage"])
    slang = random.choice(SLANG)
    emoji = random.choice(EMOJIS)

    # Force DB reuse if possible
    input_snippet = input_text
    if learned_phrases and random.random() < 0.75:  # 75% chance to pull from DB
        relevant = [p[0] for p in learned_phrases if p[1] == topic]
        input_snippet = random.choice(relevant or [p[0] for p in learned_phrases])[:20]

    return template.format(
        greeting=greeting, user=user, action=action, mood=mood, feels=feels, slang=slang, emoji=emoji, topic=topic, input=input_snippet[:20], question_word=question_word
    )

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
        response = generate_response(message.author.display_name, message.content)
        await message.channel.send(response)

    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    """Test command."""
    await ctx.send(f"Yo {ctx.author.display_name}, you lit or what? 😎")

@bot.command()
async def phrases(ctx):
    """Show number of learned phrases."""
    count = len(load_phrases())
    await ctx.send(f"Kek {ctx.author.display_name}, I got {count} memes in my head! {random.choice(EMOJIS)}")

@bot.command()
async def topic(ctx):
    """Show trending topic."""
    trending = get_trending_topic()
    await ctx.send(f"Yo {ctx.author.display_name}, server’s all about {trending} rn! {random.choice(EMOJIS)}")

# Run the bot
bot.run("YOUR_BOT_TOKEN")
