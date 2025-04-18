from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_ID

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return await update.message.reply_text("⛔ Команда недоступна.")
    
    await update.message.reply_text(
        "/start — начать\n"
        "/reload — перезагрузить Excel\n"
        "/stats — статистика\n"
        "/broadcast — рассылка\n"
        "/add — добавить вопрос с ответом\n"
        "/delete — удалить вопрос\n"
        "/edit — изменить ответ на вопрос"
    )
