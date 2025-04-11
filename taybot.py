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
    "{greeting}! What's good, {user}? You {mood} or nah? {emoji}",
    "Yo {user}, you out here {action} some {topic}? Feels {feels} man! {emoji}",
    "Kek! {user}, you said '{input}'? That’s {slang} af! {emoji}",
    "Bloop! {user} be {mood} about {topic}, but I’m {slang} rn. 😎",
    "Top kek, {user}! You {action} like a {slang} {topic} normie? {emoji}",
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

def load_phrases(limit=100):
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
    return result[0] if result else "memes"  # Default to "memes" if empty
