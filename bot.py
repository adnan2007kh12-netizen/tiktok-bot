import requests
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = -1003734774744

async def check_join(update: Update, context):
    user_id = update.effective_user.id
    try:
        member = await context.bot.get_chat_member(-1003734774744, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    joined = await check_join(update, context)
    if not joined:
        await update.message.reply_text(
            "🚫 لازم تشترك بالقناة أولاً 👇\n"
            "https://t.me/media_bots5\n\n"
            "بعد الاشتراك ابعت الرابط مرة ثانية ✅"
        )
        return

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
        await update.message.reply_text("📩 ابعت رابط TikTok فقط")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, handle_message))
app.run_polling()
