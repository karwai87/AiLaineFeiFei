from flask import Flask
from telegram.ext import Application
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot is running!'

# Telegram bot 启动函数
async def start_bot():
    application = Application.builder().token(BOT_TOKEN).build()

    # 注册命令
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), gpt_chat))

    # 启动 polling（非阻塞）
    await application.initialize()
    await application.start()
    await application.updater.start_polling()

# 启动 Flask + Telegram
if __name__ == '__main__':
    # 启动 Telegram bot 线程
    bot_thread = threading.Thread(target=lambda: asyncio.run(start_bot()))
    bot_thread.start()

    # 启动 Flask
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
