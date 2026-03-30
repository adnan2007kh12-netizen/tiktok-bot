import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = "8258990351:AAGHcuQ8TQcACw51V1Ve6hANotJCn5KhFbA"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    if "tiktok.com" in url:
        await update.message.reply_text("⏳ جاري التحميل...")

        try:
            api_url = f"https://tikwm.com/api/?url={url}"
            response = requests.get(api_url).json()
            video_url = response['data']['play']

            await update.message.reply_video(video_url)

        except:
            await update.message.reply_text("❌ صار خطأ")

    else:
        await update.message.reply_text("📩 ارسل رابط تيك توك")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, handle_message))
app.run_polling()
