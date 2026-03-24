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
| 🎬 **Episode Rename** | Auto rename with episode numbers using `{episode}` variable |
| 🖼️ **Custom Thumbnail** | Set custom thumbnail for all videos |
| 📊 **Live Progress Bar** | Real-time progress for each video |
| 🔄 **Batch Mode** | Add URLs one by one, process all together |
| ⚡ **Single Mode** | Send multiple URLs at once, process simultaneously |
| 🧹 **Auto Cleanup** | Temp files deleted automatically |

---

## 🔧 Commands

| Command | Description |
|---------|-------------|
| `/start` | Show bot information and help |
| `/rename <pattern>` | Set episode rename pattern (must include `{episode}`) |
| `/thumb` | Set custom thumbnail (reply to a photo) |
| `/showthumb` | Show current thumbnail |
| `/delthumb` | Delete thumbnail |
| `/reset` | Reset episode counter to 1 |
| `/finish` | Process all queued URLs |
| `/cancel` | Clear queue |

---

## 📝 How to Use

### 🎬 Episode Rename

Set your rename pattern using `/rename` command with `{episode}` variable. Then send your video URLs - each will get the next episode number automatically.

### 🚀 Single Mode

Send multiple video URLs in one message (one per line). All videos will download and upload simultaneously.

### 📦 Batch Mode

Send URLs one by one, then type `/finish` to process all videos together.

### 🖼️ Thumbnail

Send a photo and reply with `/thumb` to set custom thumbnail for all videos.

---

## 🛠️ Deployment

### Deploy on Render

1. **Fork this repository**

2. **Create a new Web Service on Render**

3. **Environment Variables:**
```

TG_BOT_TOKEN = your_bot_token
APP_ID = your_app_id
API_HASH = your_api_hash
AUTH_USERS = user_id1,user_id2

```

4. **Build Command:**
   ```bash
   pip install -r requirements.txt
   apt-get update && apt-get install -y ffmpeg
```

1. Start Command:
   ```bash
   python bot.py
   ```

Deploy Locally

```bash
git clone https://github.com/yourusername/video-uploader-bot.git
cd video-uploader-bot
pip install -r requirements.txt
sudo apt-get install ffmpeg -y  # For Linux
python bot.py
```

---

📦 Requirements

```txt
pyrogram==2.0.106
requests==2.31.0
Pillow==10.1.0
ffmpeg (system dependency)
```

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

All videos are processed in parallel, reducing total upload time significantly compared to sequential processing.

---

⚙️ Configuration

Configure via environment variables or edit bot.py:

```python
class Config:
    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
    APP_ID = int(os.environ.get("APP_ID"))
    API_HASH = os.environ.get("API_HASH")
    AUTH_USERS = {int(x) for x in os.environ.get("AUTH_USERS", "").split(",")}
    DOWNLOAD_LOCATION = "./DOWNLOADS"
    MAX_FILE_SIZE = 2000000000
```

---

🐛 Troubleshooting

Issue Solution
Video upload as document Install ffmpeg on your server
Progress bar not showing Check your internet connection
"Not authorized" error Add your user ID to AUTH_USERS
Slow upload speed Render free tier has bandwidth limitations

---

📄 License

MIT License - Feel free to use and modify!

---

🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

<div align="center">

⭐ Star this repository if you find it useful!

Made with ❤️ for the Telegram Community

</div>
