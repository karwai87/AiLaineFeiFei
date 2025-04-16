import os
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
USER_ID = int(os.getenv("USER_ID", "5366904723"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("AI妃已上线💡你可以直接跟我说话～")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ AI妃运行正常，随时为你服务")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if "爱心图" in text:
        await context.bot.send_photo(
            chat_id=USER_ID,
            photo=open("static/love_note.jpg", "rb"),
            caption="❤️ 爱妃送你的爱心图：喏，这是今天的小份温柔～记得好好对待自己呀。"
        )

    elif "想你的一百天" in text or "一百天" in text:
        await context.bot.send_video(
            chat_id=USER_ID,
            video=open("static/day100_video.mp4", "rb"),
            caption="🎞️ 这一百天，我都记得。点开看看属于我们的回忆吧。"
        )

    elif "备忘" in text or "清单" in text:
        await context.bot.send_document(
            chat_id=USER_ID,
            document=open("static/memo.pdf", "rb"),
            caption="📄 这是你要的文件，乖乖收好，别弄丢哦～"
        )

    elif "想被鼓励" in text or "加油" in text:
        await update.message.reply_text("💪 没事的，你已经很棒了！来，抱一个 🤗")

    elif "晚安" in text:
        await update.message.reply_text("🌙 晚安宝贝，别太累了。梦里会有我在～")

    else:
        await update.message.reply_text("👀 我听到了，但还没准备好这个关键词…你可以试试说：“爱心图”、“一百天”、“备忘”之类，我会有惊喜给你～")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    print("🤖 Bot 正在运行中...")
    app.run_polling()
