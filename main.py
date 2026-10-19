import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp
TOKEN = os.environ.get("BOT_TOKEN")
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلا! ابعث رابط TikTok / Insta / YouTube")
async def dl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url=update.message.text
    if "http" not in url: return
    m=await update.message.reply_text("⏳ عم حمل...")
    try:
        with yt_dlp.YoutubeDL({'format':'best[ext=mp4]/best','outtmpl':'vid.%(ext)s','quiet':True}) as ydl:
            ydl.extract_info(url,download=True)
        import glob
        f=glob.glob("vid.*")[0]
        await update.message.reply_video(open(f,'rb'))
        os.remove(f)
        await m.delete()
    except Exception as e:
        await m.edit_text(f"❌ {e}")
app=ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start",start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,dl))
app.run_polling()
