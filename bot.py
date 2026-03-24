import os
import time
import requests
import asyncio
import re
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait
from PIL import Image

# Config - Use environment variables for security
class Config:
    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "8519451434:AAFQPiKXYjdiHzTyIIVwi9zxwzmupEevOcw")
    APP_ID = int(os.environ.get("APP_ID", 25976192))
    API_HASH = os.environ.get("API_HASH", "8ba23141980539b4896e5adbc4ffd2e2")
    AUTH_USERS = {int(x) for x in os.environ.get("AUTH_USERS", "8350605421,6621572366").split(",")}
    DOWNLOAD_LOCATION = "./DOWNLOADS"
    MAX_FILE_SIZE = 2000000000

# Create temp download directory
if not os.path.isdir(Config.DOWNLOAD_LOCATION):
    os.makedirs(Config.DOWNLOAD_LOCATION)

app = Client(
    "URL_Uploader_Bot",
    bot_token=Config.TG_BOT_TOKEN,
    api_id=Config.APP_ID,
    api_hash=Config.API_HASH,
    sleep_threshold=30
)

# Store user data
user_thumb = {}
user_rename_pattern = {}
user_episode_counter = {}
user_batch_urls = {}

# Progress bar function
def progress_bar(current, total, filename="", status="UPLOADING", episode=""):
    if total == 0:
        return f"{episode}\n**{status}**\n┌─────────────────────┐\n│████████████████████│\n└─────────────────────┘\n**Processing...**"
    
    percentage = min(100, current / total * 100)
    filled = int(20 * current / total)
    bar = "█" * filled + "░" * (20 - filled)
    
    current_mb = current / (1024 * 1024)
    total_mb = total / (1024 * 1024)
    
    return f"""{episode}
**{status}**
┌─────────────────────┐
│{bar}│
└─────────────────────┘
**{percentage:.1f}%** | **{current_mb:.2f} MB** / **{total_mb:.2f} MB**"""

# Get file info from URL
def get_file_info(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=10)
        content_length = int(response.headers.get('content-length', 0))
        
        filename = url.split('/')[-1]
        if '?' in filename:
            filename = filename.split('?')[0]
        filename = re.sub(r'%[0-9A-Fa-f]{2}', '_', filename)
        
        if not filename or filename == '':
            filename = f"video_{int(time.time())}.mp4"
        
        if not filename.lower().endswith(('.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm')):
            filename = f"{filename}.mp4"
        
        return {
            'filename': filename,
            'size': content_length
        }
    except:
        return None

# Generate episode name
def generate_episode_name(pattern, episode_num):
    return pattern.replace("{episode}", str(episode_num))

# Process single video with full parallel capability
async def process_video_parallel(client, user_id, url, filename, thumb_path, episode_num, total_count):
    download_path = None
    episode_text = f"**🎬 Episode {episode_num}/{total_count}**"
    
    try:
        download_path = f"{Config.DOWNLOAD_LOCATION}/{user_id}_{int(time.time())}_{episode_num}.mp4"
        
        # Create status message for this video
        status_msg = await client.send_message(user_id, f"{episode_text}\n📥 **DOWNLOADING**\n┌─────────────────────┐\n│░░░░░░░░░░░░░░░░░░░░│\n└─────────────────────┘\n**0%** | **0.00 MB** / **0.00 MB**")
        
        # Download with progress
        response = requests.get(url, stream=True, timeout=30)
        total_size = int(response.headers.get('content-length', 0))
        
        downloaded = 0
        last_update = time.time()
        
        with open(download_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    
                    if time.time() - last_update >= 1:
                        percentage = (downloaded / total_size) * 100
                        filled = int(20 * downloaded / total_size)
                        bar = "█" * filled + "░" * (20 - filled)
                        current_mb = downloaded / (1024 * 1024)
                        total_mb = total_size / (1024 * 1024)
                        
                        progress_text = f"""{episode_text}
📥 **DOWNLOADING**
┌─────────────────────┐
│{bar}│
└─────────────────────┘
**{percentage:.1f}%** | **{current_mb:.2f} MB** / **{total_mb:.2f} MB**"""
                        try:
                            await status_msg.edit_text(progress_text)
                        except:
                            pass
                        last_update = time.time()
        
        # Download complete, start upload immediately
        await status_msg.edit_text(f"{episode_text}\n📤 **UPLOADING**\n┌─────────────────────┐\n│░░░░░░░░░░░░░░░░░░░░│\n└─────────────────────┘\n**0%** | **0.00 MB** / **0.00 MB**")
        
        last_progress_update = time.time()
        
        async def progress_callback(current, total):
            nonlocal last_progress_update
            now = time.time()
            if now - last_progress_update >= 1 or current == total:
                progress_text = progress_bar(current, total, filename, "📤 UPLOADING", episode_text)
                try:
                    await status_msg.edit_text(progress_text)
                except:
                    pass
                last_progress_update = now
        
        # Upload as video
        await client.send_video(
            chat_id=user_id,
            video=download_path,
            caption=f"**{filename}**",
            thumb=thumb_path,
            supports_streaming=True,
            progress=progress_callback
        )
        
        # Delete status message
        await status_msg.delete()
        return True, filename
        
    except Exception as e:
        try:
            await client.send_message(user_id, f"{episode_text}\n❌ **Error:** `{str(e)}`")
        except:
            pass
        return False, filename
        
    finally:
        if download_path and os.path.exists(download_path):
            try:
                os.remove(download_path)
            except:
                pass

# Start Command
@app.on_message(filters.command("start"))
async def start_command(client, message: Message):
    user_id = message.from_user.id
    user_batch_urls[user_id] = []
    user_episode_counter[user_id] = 1
    
    await message.reply_text(
        "**✨ PARALLEL VIDEO UPLOADER BOT**\n\n"
        "**🔗 HOW TO USE:**\n\n"
        "**Single Mode:**\n"
        "• Send multiple URLs at once (one per line)\n"
        "• Bot will process ALL videos simultaneously!\n\n"
        "**Batch Mode:**\n"
        "• Add URLs one by one\n"
        "• Type `/finish` to process all together\n\n"
        "**✏️ Episode Rename:**\n"
        "`/rename The Rising of the Shield Hero Episode {episode}`\n\n"
        "**📝 COMMANDS:**\n"
        "/start - Show this\n"
        "/rename - Set episode pattern\n"
        "/thumb - Set thumbnail\n"
        "/showthumb - View thumbnail\n"
        "/delthumb - Delete thumbnail\n"
        "/reset - Reset episode counter\n"
        "/finish - Process batch\n"
        "/cancel - Clear queue"
    )

# Rename Command
@app.on_message(filters.command("rename"))
async def set_rename_pattern(client, message: Message):
    user_id = message.from_user.id
    
    if len(message.command) > 1:
        pattern = " ".join(message.command[1:])
        if "{episode}" in pattern:
            user_rename_pattern[user_id] = pattern
            await message.reply_text(f"✅ **Pattern set!**\n\n`{pattern}`")
        else:
            await message.reply_text("❌ Must include `{episode}`")
    else:
        await message.reply_text(
            "**✏️ SET PATTERN**\n\n"
            "Use `{episode}` for episode number\n\n"
            "**Example:**\n"
            "`/rename The Rising of the Shield Hero Episode {episode}`"
        )

# Reset counter
@app.on_message(filters.command("reset"))
async def reset_episode_counter(client, message: Message):
    user_id = message.from_user.id
    user_episode_counter[user_id] = 1
    await message.reply_text("✅ **Reset to Episode 1!**")

# Cancel batch
@app.on_message(filters.command("cancel"))
async def cancel_batch(client, message: Message):
    user_id = message.from_user.id
    user_batch_urls[user_id] = []
    await message.reply_text("✅ **Queue cleared!**")

# Thumbnail Commands
@app.on_message(filters.command("thumb"))
async def set_thumbnail(client, message: Message):
    reply = message.reply_to_message
    if reply and reply.photo:
        user_id = message.from_user.id
        thumb_path = f"{Config.DOWNLOAD_LOCATION}/{user_id}_thumb.jpg"
        
        await reply.download(thumb_path)
        
        try:
            img = Image.open(thumb_path)
            img.thumbnail((320, 320))
            img.save(thumb_path, "JPEG")
        except:
            pass
        
        if user_id in user_thumb and os.path.exists(user_thumb[user_id]):
            try:
                os.remove(user_thumb[user_id])
            except:
                pass
        
        user_thumb[user_id] = thumb_path
        await message.reply_text("✅ Thumbnail saved!")
    else:
        await message.reply_text("❌ Reply to a photo with /thumb")

@app.on_message(filters.command("showthumb"))
async def show_thumbnail(client, message: Message):
    user_id = message.from_user.id
    if user_id in user_thumb and os.path.exists(user_thumb[user_id]):
        await message.reply_photo(user_thumb[user_id], caption="📸 Your thumbnail")
    else:
        await message.reply_text("❌ No thumbnail set")

@app.on_message(filters.command("delthumb"))
async def delete_thumbnail(client, message: Message):
    user_id = message.from_user.id
    if user_id in user_thumb and os.path.exists(user_thumb[user_id]):
        try:
            os.remove(user_thumb[user_id])
            del user_thumb[user_id]
            await message.reply_text("✅ Thumbnail deleted!")
        except:
            await message.reply_text("❌ Failed to delete")
    else:
        await message.reply_text("❌ No thumbnail found")

# Handle URLs - Single mode (process immediately in parallel)
@app.on_message(filters.text & filters.private)
async def handle_urls(client, message: Message):
    text = message.text.strip()
    user_id = message.from_user.id
    
    # Skip commands
    if text.startswith('/'):
        # Check for finish command
        if text == "/finish" and user_id in user_batch_urls and user_batch_urls[user_id]:
            await process_batch(client, message)
        return
    
    # Check if it's multiple URLs (one per line)
    urls = [u.strip() for u in text.split('\n') if u.strip().startswith(('http://', 'https://'))]
    
    if len(urls) > 1:
        # Multiple URLs in one message - process all in parallel
        await message.reply_text(f"✅ **Processing {len(urls)} videos in parallel!**\n\nAll videos will download and upload simultaneously.")
        
        # Get thumbnail
        thumb_path = user_thumb.get(user_id) if user_id in user_thumb and os.path.exists(user_thumb[user_id]) else None
        
        # Get pattern
        pattern = user_rename_pattern.get(user_id)
        start_episode = user_episode_counter.get(user_id, 1)
        
        # Create tasks for all videos
        tasks = []
        for idx, url in enumerate(urls):
            episode_num = start_episode + idx
            file_info = get_file_info(url)
            
            if file_info:
                if pattern:
                    episode_name = generate_episode_name(pattern, episode_num)
                    ext = file_info['filename'].split('.')[-1] if '.' in file_info['filename'] else 'mp4'
                    filename = f"{episode_name}.{ext}"
                else:
                    filename = file_info['filename']
                
                task = process_video_parallel(client, user_id, url, filename, thumb_path, episode_num, len(urls))
                tasks.append(task)
        
        # Run ALL tasks in parallel (simultaneously)
        await asyncio.gather(*tasks)
        
        # Update episode counter
        if pattern:
            user_episode_counter[user_id] = start_episode + len(urls)
        
    elif len(urls) == 1:
        # Single URL - also process with parallel capability
        file_info = get_file_info(urls[0])
        if file_info:
            thumb_path = user_thumb.get(user_id) if user_id in user_thumb and os.path.exists(user_thumb[user_id]) else None
            pattern = user_rename_pattern.get(user_id)
            episode_num = user_episode_counter.get(user_id, 1)
            
            if pattern:
                episode_name = generate_episode_name(pattern, episode_num)
                ext = file_info['filename'].split('.')[-1] if '.' in file_info['filename'] else 'mp4'
                filename = f"{episode_name}.{ext}"
                user_episode_counter[user_id] = episode_num + 1
            else:
                filename = file_info['filename']
            
            await process_video_parallel(client, user_id, urls[0], filename, thumb_path, 1, 1)
    else:
        # Not a URL, add to batch if in batch mode
        if user_id not in user_batch_urls:
            user_batch_urls[user_id] = []
        
        if text.startswith(('http://', 'https://')):
            user_batch_urls[user_id].append(text)
            total = len(user_batch_urls[user_id])
            file_info = get_file_info(text)
            if file_info:
                size_mb = file_info['size'] / (1024 * 1024)
                await message.reply_text(
                    f"✅ **Added to queue!**\n\n"
                    f"📹 **Video #{total}**\n"
                    f"📁 `{file_info['filename']}`\n"
                    f"📊 `{size_mb:.2f} MB`\n\n"
                    f"📦 **Total:** {total}\n"
                    f"Type `/finish` to start parallel processing"
                )
            else:
                await message.reply_text(f"✅ **Added URL #{total} to queue!**")

# Process batch
async def process_batch(client, message):
    user_id = message.from_user.id
    
    if user_id not in user_batch_urls or not user_batch_urls[user_id]:
        await message.reply_text("❌ **No URLs in queue!**")
        return
    
    urls = user_batch_urls[user_id]
    total = len(urls)
    
    await message.reply_text(f"✅ **Processing {total} videos in parallel!**\n\nAll videos will download and upload simultaneously.")
    
    # Get thumbnail
    thumb_path = user_thumb.get(user_id) if user_id in user_thumb and os.path.exists(user_thumb[user_id]) else None
    
    # Get pattern
    pattern = user_rename_pattern.get(user_id)
    start_episode = user_episode_counter.get(user_id, 1)
    
    # Create tasks for all videos
    tasks = []
    for idx, url in enumerate(urls):
        episode_num = start_episode + idx
        file_info = get_file_info(url)
        
        if file_info:
            if pattern:
                episode_name = generate_episode_name(pattern, episode_num)
                ext = file_info['filename'].split('.')[-1] if '.' in file_info['filename'] else 'mp4'
                filename = f"{episode_name}.{ext}"
            else:
                filename = file_info['filename']
            
            task = process_video_parallel(client, user_id, url, filename, thumb_path, episode_num, total)
            tasks.append(task)
    
    # Run ALL tasks in parallel (simultaneously)
    await asyncio.gather(*tasks)
    
    # Update episode counter
    if pattern:
        user_episode_counter[user_id] = start_episode + total
    
    # Clear queue
    user_batch_urls[user_id] = []
    
    await message.reply_text(f"✅ **All {total} videos processed!**")

# Run bot
if __name__ == "__main__":
    print("🚀 TRUE PARALLEL VIDEO UPLOADER BOT Started!")
    print("📝 ALL videos download AND upload simultaneously!")
    app.run()
