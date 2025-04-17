import os
import asyncio
from flask import Flask
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import openai
import threading
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
USER_ID = os.getenv("USER_ID")  # 可选，用于限制用户

openai.api_key = OPENAI_API_KEY

# Flask 保活服务
app = Flask(__name__)

@app.route('/')
def home():
    return 'AI妃 运行中 💡'

# /start 指令
async def start_command(update, context):
    await update.message.reply_text("AI妃已上线 💡 你可以直接跟我说话～")

# ChatGPT 回复
async def gpt_chat(update, context):
    if USER_ID and str(update.effective_user.id) != USER_ID:
        await update.message.reply_text("你无权使用此 bot")
        return

    user_input = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        reply = response.choices[0].message.content.strip()
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text("出错了：" + str(e))

# 启动 Bot
async def start_bot():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), gpt_chat))
    await application.initialize()
    await application.start()
    await application.updater.start_polling()

# 启动 Flask + Telegram
if __name__ == '__main__':
    bot_thread = threading.Thread(target=lambda: asyncio.run(start_bot()))
    bot_thread.start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
