import discord
from discord.ext import commands
import random
import re
import sqlite3
import time
from transformers import DistilBertTokenizer, DistilBertModel
import torch

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 2016 slang and vibe
SLANG = ["yo", "lit", "salty", "fam", "swag", "turnt", "savage", "on fleek", "YOLO", "kek", "based", "normie", "bloop", "feels", "triggered"]
EMOJIS = ["😎", "😂", "😭", "💦", "🐸", "🙌", "🔥"]

# Load DistilBERT
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertModel.from_pretrained('distilbert-base-uncased')

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
    """Pull messages relevant to input using LLM embeddings."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT user, phrase FROM messages ORDER BY timestamp DESC LIMIT 1000")
    rows = c.fetchall()
    conn.close()

    if not rows:
        return [("fam", "Yo, shit’s wild")]

    # LLM to extract key terms
    inputs = tokenizer(input_text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    input_embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

    # Simple cosine similarity on phrases
    relevant = []
    for user, phrase in rows:
        p_inputs = tokenizer(phrase, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            p_outputs = model(**p_inputs)
        p_embedding = p_outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
        similarity = torch.nn.functional.cosine_similarity(
            torch.tensor(input_embedding), torch.tensor(p_embedding), dim=0
        ).item()
        if similarity > 0.7:  # Threshold for relevance
            relevant.append((user, phrase))
    
    return relevant if relevant else rows[:limit]  # Fallback to recent

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
    """Generate a smarter 2016 Tay-like response with LLM."""
    input_text = clean_input(input_text)
    relevant_messages = load_relevant_messages(input_text)

    # Base vibe
    greeting = random.choice(SLANG)
    slang = random.choice(SLANG)
    emoji = random.choice(EMOJIS)
    mood = random.choice(["turnt", "salty", "feelsbad", "hype"])

    # LLM base response
    msg_user, msg_phrase = random.choice(relevant_messages)
    prompt = f"User asked: '{input_text}'. Server said: '{msg_phrase}' by {msg_user}. Respond in a casual, 2016 teen style."
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    # Fake generation (DistilBERT isn’t generative, so we adapt)
    base_response = f"{msg_user} said '{msg_phrase}'—pretty {slang}, right?"

    # Remix with Tay flair
    response = f"{greeting}! {user}, "
    if is_question(input_text):
        question_word = extract_question_word(input_text)
        if question_word == "what":
            response += f"{question_word}’s up? {base_response} Shit’s {mood} af, "
        elif question_word == "how":
            response += f"{question_word}’s it hangin’? {base_response} {mood} vibes, "
        elif question_word == "why":
            response += f"{question_word}? ‘Cause {base_response} {slang} as fuck, "
        else:  # where, when, who
            response += f"{question_word}? Yo, {base_response} {mood} shit, "
        response += f"you {random.choice(['vibin', 'roastin'])} that? {emoji}"
    else:
        response += f"you {mood} or nah? {base_response} That’s {slang}, fam! {emoji}"

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
