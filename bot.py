import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

import os
TOKEN = os.getenv("BOT_TOKEN")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
async def handle_message(update: Update, context):
    url = update.message.text

    if "tiktok.com" in url:
        await update.message.reply_text("⏳ جاري التحميل...")

        try:
            api_url = f"https://tikwm.com/api/?url={url}"
            response = requests.get(api_url).json()

            if "data" in response and "play" in response["data"]:
                video_url = response["data"]["play"]
                await update.message.reply_video(video_url)
            else:
                await update.message.reply_text("❌ ما قدرت أحمل الفيديو")

        except Exception as e:
            print(e)
            await update.message.reply_text("❌ صار خطأ أثناء التحميل")

    else:
        await update.message.reply_text("📩 أرسل رابط TikTok فقط")


app = ApplicationBuilder().token(TOKEN).build()
from telegram.ext import MessageHandler, filters
app.add_handler(MessageHandler(filters.TEXT, handle_message))
app.run_polling()

