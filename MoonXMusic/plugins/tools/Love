# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

from pyrogram import Client, filters
import random
from MoonXMusic import app
from config import BOT_USERNAME
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_random_message(love_percentage):
    if love_percentage <= 30:
        return random.choice([
            "💔 Love is in the air, but it needs a little spark.",
            "🌱 A good beginning, but there's room to grow.",
            "✨ Just the start of something meaningful."
        ])
    elif love_percentage <= 70:
        return random.choice([
            "💞 A strong bond is building. Keep nurturing it.",
            "🌼 You’ve got potential. Keep working on it.",
            "🌸 Love is blooming. Stay consistent."
        ])
    else:
        return random.choice([
            "💖 A match made in heaven!",
            "🌟 A perfect pair! Cherish the bond.",
            "💍 Destined to be together. Congratulations!"
        ])


@app.on_message(filters.command("love", prefixes="/"))
async def love_command(client, message):
    command, *args = message.text.split(" ")
    if len(args) >= 2:
        name1 = args[0].strip()
        name2 = args[1].strip()

        love_percentage = random.randint(10, 100)
        love_message = get_random_message(love_percentage)

        response = (
            f"❤️ Here is your love percentage:\n\n"
            f"🔹 {name1} ❤️ + {name2} ❤️ = {love_percentage}%\n\n"
            f"💬 {love_message}"
        )
    else:
        response = "❗ Please enter two names after the `/love` command."

    add_me_button = [
        [
            InlineKeyboardButton(
                text="➕ Add Me to Group",
                url=f"https://t.me/{BOT_USERNAME}?startgroup=true"
            ),
        ]
    ]

    await client.send_message(
        message.chat.id,
        response,
        reply_markup=InlineKeyboardMarkup(add_me_button),
    )
