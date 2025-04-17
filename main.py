import os
import asyncio
from flask import Flask
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import threading
from dotenv import load_dotenv

# 加载 .env 环境变量（Railway 会自动读取）
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
USER_ID = os.getenv("USER_ID")

# Flask 应用（用于保活）
app = Flask(__name__)

@app.route('/')
def home():
    return "AI妃上线中 💡"

# /start 指令处理
async def start_command(update, context):
    await update.message.reply_text("AI妃已上线 💡 你可以直接跟我说话～")

# 普通文本消息处理
async def echo_message(update, context):
    if USER_ID and str(update.effective_user.id) != USER_ID:
        await update.message.reply_text("你无权访问此 bot")
        return

    user_message = update.message.text
    await update.message.reply_text(f"你说了：{user_message}")

# 启动 Telegram Bot
async def start_bot():
    app_bot = Application.builder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start_command))
    app_bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo_message))

    await app_bot.initialize()
    await app_bot.start()
    await app_bot.updater.start_polling()

# 启动 Flask + Telegram
if __name__ == "__main__":
    bot_thread = threading.Thread(target=lambda: asyncio.run(start_bot()))
    bot_thread.start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
