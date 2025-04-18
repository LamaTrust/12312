
import datetime
import json
import os

from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_ID
from services.users import user_ids

def save_question_from_user(user, question: str):
    entry = {
        "user_id": user.id,
        "username": user.username,
        "name": user.full_name,
        "question": question,
        "timestamp": datetime.datetime.now().isoformat()
    }
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "user_questions.json")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []
    data.append(entry)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("awaiting_broadcast"):
        text = update.message.text
        count = 0
        for uid in user_ids:
            try:
                await context.bot.send_message(chat_id=uid, text=f"📢 Рассылка:{text}")
                count += 1
            except:
                continue
        context.user_data["awaiting_broadcast"] = False
        await update.message.reply_text(f"✅ Рассылка завершена ({count} пользователей).")

    elif context.user_data.get("awaiting_user_question"):
        question = update.message.text.strip()
        context.user_data["awaiting_user_question"] = False
        save_question_from_user(update.effective_user, question)

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📨 Новый вопрос от @{update.effective_user.username or update.effective_user.first_name}:{question}"
        )
        await update.message.reply_text("✅ Ваш вопрос отправлен. Спасибо!")

    else:
        if update.effective_user.id not in user_ids:
            await update.message.reply_text("⚠️ Пожалуйста, нажмите /start, чтобы начать.")
