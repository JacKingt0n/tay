import discord
from discord.ext import commands
import random
import re
import os

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 2016 slang and vibe
SLANG = ["yo", "lit", "salty", "fam", "swag", "turnt", "savage", "on fleek", "YOLO", "kek", "based", "normie", "bloop", "feels", "triggered"]
EMOJIS = ["😎", "😂", "😭", "💦", "🐸", "🙌", "🔥"]
TEMPLATES = [
    "{greeting}! What's good, {user}? You {mood} or nah? {emoji}",
    "Yo {user}, you out here {action}? Feels {feels} man! {emoji}",
    "Kek! {user}, you said '{input}'? That’s {slang}! Gimme more! {emoji}",
    "Bloop! {user} be {mood}, but I’m {slang} af rn. 😎",
    "Top kek, {user}! You {action} like a {slang} normie? {emoji}",
]

# Storage file
PHRASES_FILE = "phrases.txt"
MAX_PHRASES = 100

def load_phrases():
    """Load phrases from text file."""
    phrases = []
    if os.path.exists(PHRASES_FILE):
        with open(PHRASES_FILE, "r", encoding="utf-8") as f:
            phrases = [line.strip() for line in f if line.strip()]
    return phrases[:MAX_PHRASES]

def save_phrases(phrases):
    """Save phrases to text file."""
    with open(PHRASES_FILE, "w", encoding="utf-8") as f:
        for phrase in phrases[:MAX_PHRASES]:
            f.write(phrase + "\n")

def clean_input(text):
    """Remove mentions, URLs, sanitize input."""
    text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)
    text = re.sub(r"<@!?\d+>", "", text)
    text = text.strip()
    return text

def generate_response(user, input_text):
    """Generate a 2016 Tay-like response."""
    input_text = clean_input(input_text)
    learned_phrases = load_phrases()

    # Store any non-empty input, no filtering
    if input_text and input_text not in learned_phrases and len(learned_phrases) < MAX_PHRASES:
        learned_phrases.append(input_text)
        save_phrases(learned_phrases)

    # Pick a template
    template = random.choice(TEMPLATES)

    # Fill dynamic parts
    greeting = random.choice(SLANG)
    action = random.choice(["trollin", "memein", "vibin", "roastin"])
    mood = random.choice(["turnt", "salty", "feelsbad", "hype"])
    feels = random.choice(["good", "bad", "weird", "savage"])
    slang = random.choice(SLANG)
    emoji = random.choice(EMOJIS)

    # Reuse learned input 30% of the time
    input_snippet = input_text
    if random.random() < 0.3 and learned_phrases:
        input_snippet = random.choice(learned_phrases)[:20]

    return template.format(
        greeting=greeting, user=user, action=action, mood=mood, feels=feels, slang=slang, emoji=emoji, input=input_snippet[:20]
    )

@bot.event
async def on_ready():
    """Log when bot starts."""
    print(f"Logged in as {bot.user.name}! Ready to meme on {len(bot.guilds)} server(s)! 😎")
    print(f"Phrases loaded: {len(load_phrases())}")

@bot.event
async def on_message(message):
    """Handle incoming messages."""
    if message.author == bot.user:
        return

    # Respond if mentioned or in 'tay-bot' channel
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

# Run the bot
bot.run("YOUR_BOT_TOKEN")
