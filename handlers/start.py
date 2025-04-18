
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services.storage import knowledge_base
from services.users import user_ids, save_users

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_ids.add(update.effective_user.id)
    save_users(user_ids)

    welcome_text = (
        "👋 *Добро пожаловать!*\n\n"
        "Я — бот-помощник Университета. Я помогу вам найти ответы на популярные вопросы "
        "о переводе между направлениями, формах обучения, справках и многом другом.\n\n"
        "👇 Выберите интересующий раздел ниже:"
    )

    keyboard = [
        [InlineKeyboardButton(text=section, callback_data=f"section|{section}")]
        for section in knowledge_base.keys()
    ]
    keyboard.append([InlineKeyboardButton("❓ Задать вопрос", callback_data="ask_direct")])

    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(welcome_text, parse_mode="Markdown", reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.edit_message_text(welcome_text, parse_mode="Markdown", reply_markup=reply_markup)
