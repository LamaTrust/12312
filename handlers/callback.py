
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ContextTypes

from handlers.start import start
from services.storage import knowledge_base, question_id_map, reverse_id_map, attachments_map
from services.stats import usage_stats

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("section|"):
        section = data.split("|")[1]
        questions = knowledge_base.get(section, [])
        keyboard = [
            [InlineKeyboardButton(text=qa["Question"], callback_data=f"question|{reverse_id_map[qa['Question']]}")]
            for qa in questions
        ]
        keyboard.append([InlineKeyboardButton("🔙 Назад к разделам", callback_data="back_to_sections")])
        await query.edit_message_text(
            text=f"📚 *{section}*Выберите вопрос:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    elif data.startswith("question|"):
        qid = data.split("|")[1]
        qa = question_id_map.get(qid)
        if not qa:
            await query.message.reply_text("⚠️ Вопрос не найден.")
            return
        try:
            await query.message.delete()
        except:
            pass
        await query.message.chat.send_message(
            text=f"📌 *{qa['question']}*{qa['answer']}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Вернуться к разделу", callback_data=f"section|{qa['section']}")]
            ])
        )

        if qa["question"] in attachments_map:
            path = attachments_map[qa["question"]]
            if os.path.exists(path):
                filename = os.path.basename(path)
                try:
                    with open(path, "rb") as f:
                        await query.message.chat.send_document(document=f, filename=filename)
                except Exception as e:
                    await query.message.reply_text(f"❌ Ошибка при отправке файла: {e}")

        usage_stats[qa["question"]] = usage_stats.get(qa["question"], 0) + 1

    elif data == "back_to_sections":
        await start(update, context)

    elif data == "ask_direct":
        context.user_data["awaiting_user_question"] = True
        await query.edit_message_text(
            "✉️ Введите свой вопрос, и мы передадим его администрации. "
            "Ответ может быть добавлен позже.",
        )
