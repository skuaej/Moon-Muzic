# Copyright (c) 2025 Nand Yaduwanshi <NoxxOP>
# Universal Downloader Module for Music Bots
# Framework: Pyrogram

import requests
import json
import os
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from MoonXMusic import app # Tera main app instance

# --- CONFIG ---
API_URL = "https://instaaaa-pi.vercel.app/download"

def get_media_data(data):
    """
    Backend logic to find the best link (Hidden from user).
    """
    results = data.get("all_results") or data.get("results", {})
    metadata = {
        "link": data.get("clean_download_url"),
        "title": "Universal Media",
        "desc": "Downloaded via Universal Bot",
        "platform": data.get("platform", "Media").capitalize(),
        "type": "video"
    }

    # Search in all_results
    for provider, content in results.items():
        if isinstance(content, dict) and content.get("status") != "failed":
            if content.get("title"): metadata["title"] = content["title"]
            if content.get("author"): metadata["desc"] = f"By: {content['author']}"
            
            keys = ["no_watermark", "no_watermark_hd", "video_url", "download_url", "url", "mp3"]
            for key in keys:
                link = content.get(key)
                if link and isinstance(link, str) and link.startswith("http"):
                    if "token=" in link and len(link) < 60: continue
                    if any(x in link.lower() for x in [".jpg", ".png", ".webp"]): continue
                    
                    metadata["link"] = link
                    if key == "mp3" or "spotify" in data.get("platform", "").lower():
                        metadata["type"] = "audio"
                    return metadata
    return metadata if metadata["link"] else None

# --- AUTO DOWNLOAD HANDLER ---
# Jab bhi koi user link bhejega, ye auto-detect karega
@app.on_message(filters.regex(r"http(s)?://(www\.)?(facebook|fb|instagram|insta|tiktok|vt|youtube|youtu|spotify)\.com|be|link/"))
async def universal_downloader(client, message: Message):
    url = message.text
    status = await message.reply_text("🔎 **Searching for your media...**")

    try:
        response = requests.get(f"{API_URL}?url={url}", timeout=25)
        data = response.json()
        media = get_media_data(data)

        if media and media["link"]:
            title = media['title'][:100]
            description = media['desc']
            platform = media['platform']
            
            caption = f"🎬 **{title}**\n👤 {description}\n\n✨ _Powered by @{client.me.username}_"
            
            try:
                # Direct Video/Audio Send
                if media["type"] == "audio":
                    await message.reply_audio(audio=media["link"], caption=caption)
                else:
                    await message.reply_video(video=media["link"], caption=caption)
                await status.delete()
            except Exception:
                # Backend Hidden: Button mode for large files
                keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("📥 Download File", url=media['link'])]])
                await status.edit_text(
                    f"📦 **File Found on {platform}**\n\n🎬 **Title:** {title}\n👤 **Info:** {description}\n\n"
                    "⚠️ _The file is too high quality or large for direct upload. Use the button below._",
                    reply_markup=keyboard
                )
        else:
            await status.edit_text("❌ **Sorry, I couldn't find any media for this link.**")
    except Exception as e:
        await status.edit_text(f"⚠️ **API Error:** Contact @NoxxOP")

__MODULE__ = "Dᴏᴡɴʟᴏᴀᴅᴇʀ"
__HELP__ = """
**ᴜɴɪᴠᴇʀsᴀʟ ᴅᴏᴡɴʟᴏᴀᴅᴇʀ:**

• Jᴜsᴛ sᴇɴᴅ ᴀɴʏ sᴏᴄɪᴀʟ ᴍᴇᴅɪᴀ ʟɪɴᴋ (YT, FB, Iɴsᴛᴀ, TɪᴋTᴏᴋ, Sᴘᴏᴛɪғʏ).
• Tʜᴇ ʙᴏᴛ ᴡɪʟʟ ᴀᴜᴛᴏ-ᴅᴇᴛᴇᴄᴛ ᴀɴᴅ ᴅᴏᴡɴʟᴏᴀᴅ ᴛʜᴇ ᴍᴇᴅɪᴀ ꜰᴏʀ ʏᴏᴜ.
"""

# ©️ Copyright Reserved - @NoxxOP 

