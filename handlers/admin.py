from telegram import Update
from telegram.ext import ContextTypes

from config import ADMIN_ID
from services.storage import load_knowledge_from_excel, rebuild_question_maps, EXCEL_FILE, knowledge_base, attachments_map
from services.users import user_ids
from services.stats import usage_stats

async def reload_excel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return await update.message.reply_text("⛔ Нет доступа.")
    try:
        global knowledge_base, attachments_map
        knowledge_base, attachments_map = load_knowledge_from_excel(EXCEL_FILE)
        rebuild_question_maps()
        await update.message.reply_text("🔄 Excel перезагружен.")
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {e}")

async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return await update.message.reply_text("⛔ Нет доступа.")
    if not usage_stats:
        return await update.message.reply_text("📊 Пока нет статистики.")
    result = "📊 Статистика:\n" + "\n".join([f"{q} — {c} раз(а)" for q, c in usage_stats.items()])
    await update.message.reply_text(result)

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return await update.message.reply_text("⛔ Нет доступа.")
    context.user_data["awaiting_broadcast"] = True
    await update.message.reply_text("✉️ Введите текст рассылки:")
