# Copyright (c) 2025 Nand Yaduwanshi <NoxxOP>
# Framework: Pyrogram (MoonXMusic)

import requests
import json
import logging
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from MoonXMusic import app 

# --- CONFIG ---
API_URL = "https://instaaaa-pi.vercel.app/download"
logger = logging.getLogger(__name__)

def get_media_data(data):
    results = data.get("all_results") or data.get("results", {})
    # Root level check (TikTok/YT aggressive link)
    root_link = data.get("clean_download_url")
    
    metadata = {
        "link": root_link if root_link and "token=" not in root_link else None,
        "title": "Universal Media",
        "desc": "Downloaded via Universal Bot",
        "platform": data.get("platform", "Media").capitalize(),
        "type": "video"
    }

    # Deep scan providers
    for provider, content in results.items():
        if isinstance(content, dict) and content.get("status") != "failed":
            if content.get("title"): metadata["title"] = content["title"]
            if content.get("author"): metadata["desc"] = f"By: {content['author']}"
            
            keys = ["no_watermark", "no_watermark_hd", "video_url", "download_url", "url", "mp3"]
            for key in keys:
                link = content.get(key)
                if link and isinstance(link, str) and link.startswith("http"):
                    if "token=" in link and len(link) < 60: continue
                    metadata["link"] = link
                    if key == "mp3" or "spotify" in data.get("platform", "").lower():
                        metadata["type"] = "audio"
                    return metadata
    return metadata if metadata["link"] else None

# --- DOWNLOADER HANDLER ---
# Ye regex ab vt.tiktok.com ko pakka pakdega
@app.on_message(filters.regex(r"(https?://(?:www\.)?(?:tiktok\.com|vt\.tiktok\.com|instagram\.com|fb\.watch|facebook\.com|spotify\.com|youtube\.com|youtu\.be)/?\S+)") | filters.command(["dl", "download"]))
async def universal_downloader(client, message: Message):
    # Agar command use ki hai toh link text se nikal lo
    if message.command:
        if len(message.command) < 2:
            return await message.reply_text("❌ **Link toh bhej lodu!**\nUsage: `/dl [link]`")
        url = message.command[1]
    else:
        url = message.text

    status = await message.reply_text("🔎 **Scanning link...**")
    print(f"[DEBUG] Hitting API for: {url}") # Terminal mein check karne ke liye

    try:
        response = requests.get(f"{API_URL}?url={url}", timeout=30)
        data = response.json()
        media = get_media_data(data)

        if media and media["link"]:
            title = media['title'][:100]
            caption = f"🎬 **{title}**\n👤 {media['desc']}\n\n✨ _Powered by @{client.me.username}_"
            
            try:
                if media["type"] == "audio":
                    await message.reply_audio(audio=media["link"], caption=caption)
                else:
                    await message.reply_video(video=media["link"], caption=caption, supports_streaming=True)
                await status.delete()
            except Exception as e:
                # Backend Hidden: Button mode
                keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("📥 Download File", url=media['link'])]])
                await status.edit_text(
                    f"📦 **File Found on {media['platform']}**\n\n🎬 **Title:** {title}\n\n"
                    "⚠️ _The file is too large for Telegram upload. Use the button below._",
                    reply_markup=keyboard
                )
        else:
            await status.edit_text("❌ **No working link found for this media.**")
    except Exception as e:
        print(f"[ERROR] API Call Fail: {e}")
        await status.edit_text("⚠️ **API Error or Timeout.**")

__MODULE__ = "Dᴏᴡɴʟᴏᴀᴅᴇʀ"
__HELP__ = """
**ᴜɴɪᴠᴇʀsᴀʟ ᴅᴏᴡɴʟᴏᴀᴅᴇʀ:**

• Jᴜsᴛ sᴇɴᴅ ᴀɴʏ sᴏᴄɪᴀʟ ᴍᴇᴅɪᴀ ʟɪɴᴋ (YT, FB, Iɴsᴛᴀ, TɪᴋTᴏᴋ, Sᴘᴏᴛɪғʏ).
• Oʀ ᴜsᴇ `/dl [ʟɪɴᴋ]` ɪғ ᴀᴜᴛᴏ-ᴅᴇᴛᴇᴄᴛ ꜰᴀɪʟs.
"""
