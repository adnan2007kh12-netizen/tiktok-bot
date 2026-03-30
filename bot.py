import requests
import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler, CallbackQueryHandler

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "@media_bots5"

async def check_join(user_id, context):
    try:
        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 اشترك بالقناة", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")],
        [InlineKeyboardButton("✅ تحققت من الاشتراك", callback_data="check")]
    ]
    await update.message.reply_text(
        "🔥 أهلاً!\n\nلاستخدام البوت لازم تشترك بالقناة أولاً 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def check_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    if await check_join(user_id, context):
        await query.edit_message_text("✅ تم التحقق! الآن أرسل رابط TikTok")
    else:
        await query.answer("❌ لسا ما اشتركت", show_alert=True)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not await check_join(user_id, context):
        keyboard = [
            [InlineKeyboardButton("📢 اشترك بالقناة", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")],
            [InlineKeyboardButton("✅ تحققت من الاشتراك", callback_data="check")]
        ]
        await update.message.reply_text(
            "🚫 لازم تشترك بالقناة أولاً",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

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

        except:
            await update.message.reply_text("❌ صار خطأ")

    else:
        await update.message.reply_text("📩 أرسل رابط TikTok فقط")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(check_button))
app.add_handler(MessageHandler(filters.TEXT, handle_message))

app.run_polling()
