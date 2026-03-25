import yt_dlp
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, CallbackQueryHandler, filters, ContextTypes

TOKEN = "8751860405:AAHHuH5mRH5_NmNO402p_ESLQ8Nwf_DZpJ4"

user_links = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Отправь ссылку с YouTube 🎥")

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    user_links[update.message.chat_id] = url

    keyboard = [
        [InlineKeyboardButton("🎥 360p", callback_data="360")],
        [InlineKeyboardButton("🎥 720p", callback_data="720")],
        [InlineKeyboardButton("🎵 MP3", callback_data="mp3")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Выбери формат:", reply_markup=reply_markup)

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    choice = query.data
    url = user_links.get(query.message.chat_id)

    await query.message.reply_text("⏳ Готовлю...")

    if choice == "mp3":
        ydl_opts = {
            'format': 'bestaudio',
            'outtmpl': 'audio.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
        }
        filename = "audio.mp3"
    else:
        ydl_opts = {
            'format': f'bestvideo[height<={choice}]+bestaudio/best',
            'outtmpl': 'video.mp4',
        }
        filename = "video.mp4"

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        await query.message.reply_document(open(filename, 'rb'))

    except Exception as e:
        await query.message.reply_text(f"Ошибка: {e}")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle_link))
app.add_handler(CallbackQueryHandler(download))

app.run_polling()
