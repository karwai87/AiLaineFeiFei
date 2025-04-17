import os
from flask import Flask
from threading import Thread
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
USER_ID = os.getenv("USER_ID")

# Flask 心跳应用
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "AI妃 正常运行中 💡"

# /start 指令
async def start_command(update, context):
    await update.message.reply_text("AI妃已上线 💡 你可以直接跟我说话～")

# 普通消息回应
async def echo_message(update, context):
    if USER_ID and str(update.effective_user.id) != USER_ID:
        await update.message.reply_text("你无权访问此 bot")
        return
    await update.message.reply_text(f"你说了：{update.message.text}")

# 启动 Flask 的线程函数
def run_flask():
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# 主入口
if __name__ == '__main__':
    # Flask 在独立线程启动
    Thread(target=run_flask).start()

    # 启动 Telegram Bot（使用 run_polling）
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo_message))

    application.run_polling()
