# 🚀 Parallel Video Uploader Bot

<div align="center">

### ⚡ True Parallel Processing Video Uploader Bot

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Pyrogram](https://img.shields.io/badge/Pyrogram-2.0.106-green.svg)](https://docs.pyrogram.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Render](https://img.shields.io/badge/Deploy-Render-purple.svg)](https://render.com)

**Upload Multiple Videos Simultaneously with Episode Rename Support!**

</div>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🚀 **True Parallel Processing** | All videos download AND upload at the same time |
| 🎬 **Episode Rename** | Auto rename with episode numbers: `Name Episode {episode}` |
| 🖼️ **Custom Thumbnail** | Set custom thumbnail for all videos |
| 📊 **Live Progress Bar** | Real-time progress for each video |
| 🔄 **Batch Mode** | Add URLs one by one, process all together |
| ⚡ **Single Mode** | Send multiple URLs at once, process simultaneously |
| 🧹 **Auto Cleanup** | Temp files deleted automatically |

---

## 📸 Screenshots

<div align="center">
  <img src="https://i.ibb.co.com/mCx78DTg/Screenshot-20260324-195945-org-telegram-messenger.jpg" alt="Demo Screenshot" width="300">
  <br>
  <em>All videos processing simultaneously!</em>
</div>

---

## 🔧 Commands

```
start - Show bot information and help
rename - Set episode rename pattern
thumb - Set custom thumbnail (reply to photo)
showthumb - Show current thumbnail
delthumb - Delete thumbnail
reset - Reset episode counter to 1
finish - Process all queued URLs
cancel - Clear questartstartue
```
---

## 📝 How to Use

### 🎬 Episode Rename Pattern

```

/rename The Rising of the Shield Hero Episode {episode}

```

Then send URLs:
```

https://example.com/video1.mp4  → Episode 1
https://example.com/video2.mp4  → Episode 2
https://example.com/video3.mp4  → Episode 3

```

### 🚀 Single Mode (Multiple URLs)

Send multiple URLs in one message:
```

https://example.com/video1.mp4
https://example.com/video2.mp4
https://example.com/video3.mp4
https://example.com/video4.mp4

```
✅ **All 4 videos download AND upload simultaneously!**

### 📦 Batch Mode (One by One)

```

https://example.com/video1.mp4
https://example.com/video2.mp4
https://example.com/video3.mp4
/finish

```
✅ **All 3 videos process together!**

---

## 🖼️ Thumbnail Setup

1. Send a photo
2. Reply with `/thumb`
3. ✅ Thumbnail saved!

---

🛠️ Deployment

Deploy on Render

1. Fork this repository
2. Create a new Web Service on Render
3. Environment Variables:
   ```
   TG_BOT_TOKEN = your_bot_token
   APP_ID = your_app_id
   API_HASH = your_api_hash
   AUTH_USERS = 8350605421,6621572366
   ```
4. Build Command:
   ```bash
   pip install -r requirements.txt && apt-get update && apt-get install -y ffmpeg
   ```
5. Start Command:
   ```bash
   python bot.py
   ```

Deploy Locally

```bash
# Clone repository
git clone https://github.com/RAHAT11790/URL-UPLOAD-BOT
cd URL-UPLOAD-BOT

# Install dependencies
pip install -r requirements.txt

# Install ffmpeg
# Ubuntu/Debian:
sudo apt-get install ffmpeg -y

# Windows: Download from https://ffmpeg.org/download.html
# Add ffmpeg to system PATH after installation

# Run bot
python bot.py
```

---

📦 Requirements

```txt
pyrogram==2.0.106
requests==2.31.0
Pillow==10.1.0
```

⚠️ ffmpeg is a system dependency, not a Python package. Install it separately using the commands above.

---
🌟 How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                     USER SENDS URLs                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              TRUE PARALLEL PROCESSING                       │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │Video 1  │  │Video 2  │  │Video 3  │  │Video 4  │        │
│  │DOWNLOAD │  │DOWNLOAD │  │DOWNLOAD │  │DOWNLOAD │        │
│  │   ↓     │  │   ↓     │  │   ↓     │  │   ↓     │        │
│  │UPLOAD   │  │UPLOAD   │  │UPLOAD   │  │UPLOAD   │        │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘        │
│              ALL AT THE SAME TIME!                          │
└─────────────────────────────────────────────────────────────┘
```

---

📊 Performance

Videos Sequential Time Parallel Time Speedup
5 x 200MB ~10 minutes ~2 minutes 5x faster
10 x 200MB ~20 minutes ~2 minutes 10x faster

---

⚙️ Configuration

Edit bot.py or use environment variables:

```python
class Config:
    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "your_token")
    APP_ID = int(os.environ.get("APP_ID", 12345))
    API_HASH = os.environ.get("API_HASH", "your_hash")
    AUTH_USERS = {int(x) for x in os.environ.get("AUTH_USERS", "").split(",")}
    DOWNLOAD_LOCATION = "./DOWNLOADS"
    MAX_FILE_SIZE = 2000000000  # 2GB
```

---

🐛 Troubleshooting

Issue Solution
Video upload as document Install ffmpeg
Progress bar not showing Check internet connection
"Not authorized" Add user ID to AUTH_USERS
Slow upload Render free tier has limited bandwidth

---

📄 License

MIT License - Feel free to use and modify!

---

🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

📞 Support

· Create an issue in this repository
· Contact: @RS_WONER

---

<div align="center">

⭐ Star this repository if you find it useful!

Made with ❤️ for the Telegram Community

</div>
