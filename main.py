import logging
import os
import sentry_sdk
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from flask import Flask
from threading import Thread
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 集成Sentry
sentry_sdk.init(os.getenv("SENTRY_DSN"))

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "AI妃 Telegram Bot 正常运行中 🚀"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("欢迎使用 AI 妃系统！请输入 /auth 授权 Google")

async def auth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    auth_url = os.getenv("WEBHOOK_URL").replace('/webhook', '/oauth2callback')
    await update.message.reply_text(f"点击链接进行Google授权：{auth_url}")

def run_flask():
    app_flask.run(host='0.0.0.0', port=int(os.getenv("PORT", 8080)))

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"出现错误: {context.error}")
    sentry_sdk.capture_exception(context.error)

if __name__ == '__main__':
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("auth", auth))

    application.add_error_handler(error_handler)

    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT", 8080)),
        url_path='webhook',
        webhook_url=WEBHOOK_URL
    )
