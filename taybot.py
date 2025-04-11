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

# SQLite setup
DB_FILE = "taybot.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY, user TEXT, phrase TEXT, channel TEXT, timestamp REAL)''')
    conn.commit()
    conn.close()

def save_message(user, phrase, channel):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO messages (user, phrase, channel, timestamp) VALUES (?, ?, ?, ?)",
              (user, phrase, channel, time.time()))
    conn.commit()
    conn.close()

def load_relevant_messages(input_text, limit=100):
    """Pull messages relevant to input keywords."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    keywords = re.findall(r'\w+', input_text.lower())
    if not keywords:
        c.execute("SELECT user, phrase FROM messages ORDER BY timestamp DESC LIMIT ?", (limit,))
    else:
        like_clauses = " OR ".join(["phrase LIKE ?" for _ in keywords])
        query = f"SELECT user, phrase FROM messages WHERE {like_clauses} ORDER BY timestamp DESC LIMIT ?"
        c.execute(query, [f"%{kw}%" for kw in keywords] + [limit])
    rows = c.fetchall()
    conn.close()
    return rows if rows else [("fam", "Yo, shit’s wild")]  # Fallback

def clean_input(text):
    """Remove mentions, URLs, sanitize input."""
    text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)
    text = re.sub(r"<@!?\d+>", "", text)
    text = text.strip()
    return text

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
    """Generate a conversational 2016 Tay-like response from full history."""
    input_text = clean_input(input_text)
    relevant_messages = load_relevant_messages(input_text)

    # Base vibe
    greeting = random.choice(SLANG)
    slang = random.choice(SLANG)
    emoji = random.choice(EMOJIS)
    mood = random.choice(["turnt", "salty", "feelsbad", "hype"])

    # Build response
    response = f"{greeting}! {user}, "
    if is_question(input_text):
        question_word = extract_question_word(input_text)
        # Pick a relevant message
        msg_user, msg_phrase = random.choice(relevant_messages)
        if question_word == "what":
            response += f"{question_word}’s good? Shit’s {slang}—{msg_user} said '{msg_phrase}', "
        elif question_word == "how":
            response += f"{question_word}’s it rollin’? {mood} vibes—{msg_user} dropped '{msg_phrase}', "
        elif question_word == "why":
            response += f"{question_word}? ‘Cause {msg_user} hit us with '{msg_phrase}', {slang} as fuck, "
        elif question_word == "where":
            response += f"{question_word}? Somewhere {slang}—{msg_user} mentioned '{msg_phrase}', "
        elif question_word == "when":
            response += f"{question_word}? Whenever it’s {mood}—{msg_user} said '{msg_phrase}', "
        else:  # who
            response += f"{question_word}? Some {slang} fam—{msg_user} threw '{msg_phrase}', "
        response += f"you feelin’ that? {emoji}"
    else:
        msg_user, msg_phrase = random.choice(relevant_messages)
        response += f"you {mood} or what? {msg_user} said '{msg_phrase}', that’s {slang} af, fam! {emoji}"

    return response

@bot.event
async def on_ready():
    """Log when bot starts."""
    init_db()
    print(f"Logged in as {bot.user.name}! Ready to meme on {len(bot.guilds)} server(s)! 😎")
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM messages")
    count = c.fetchone()[0]
    conn.close()
    print(f"Messages loaded: {count}")

@bot.event
async def on_message(message):
    """Handle incoming messages."""
    if message.author == bot.user:
        return

    # Learn from all messages
    input_text = clean_input(message.content)
    if input_text:
        save_message(str(message.author), input_text, str(message.channel))

    # Respond when tagged or in tay-bot
    if bot.user.mentioned_in(message) or message.channel.name == "tay-bot":
        response = generate_response(str(message.author), message.content)
        await message.channel.send(response)

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

# Run the bot
bot.run("YOUR_BOT_TOKEN")
