from telegram import Update
from telegram.ext import ContextTypes

from config import ADMIN_ID
from services.storage import knowledge_base, save_knowledge_to_excel, rebuild_question_maps

async def add_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return await update.message.reply_text("⛔ Нет доступа.")
    context.user_data['edit_mode'] = 'add'
    await update.message.reply_text("➕ Введите раздел, куда добавить вопрос:")

async def edit_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return await update.message.reply_text("⛔ Нет доступа.")
    context.user_data['edit_mode'] = 'edit'
    await update.message.reply_text("✏️ Введите точный текст вопроса, который хотите изменить:")

async def delete_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return await update.message.reply_text("⛔ Нет доступа.")
    context.user_data['edit_mode'] = 'delete'
    await update.message.reply_text("🗑 Введите точный текст вопроса, который нужно удалить:")

async def handle_edit_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mode = context.user_data.get('edit_mode')

    if mode == 'add':
        if 'new_section' not in context.user_data:
            context.user_data['new_section'] = update.message.text.strip()
            await update.message.reply_text("✍️ Теперь введите текст нового вопроса:")
        elif 'new_question' not in context.user_data:
            context.user_data['new_question'] = update.message.text.strip()
            await update.message.reply_text("📋 Введите ответ на этот вопрос:")
        elif 'new_answer' not in context.user_data:
            context.user_data['new_answer'] = update.message.text.strip()
            section = context.user_data['new_section']
            question = context.user_data['new_question']
            answer = context.user_data['new_answer']
            if section not in knowledge_base:
                knowledge_base[section] = []
            knowledge_base[section].append({"Question": question, "answer": answer})
            save_knowledge_to_excel()
            rebuild_question_maps()
            context.user_data.clear()
            await update.message.reply_text("✅ Вопрос добавлен.")

    elif mode == 'edit':
        if 'edit_target' not in context.user_data:
            question = update.message.text.strip()
            context.user_data['edit_target'] = question
            found = False
            for section, qas in knowledge_base.items():
                for qa in qas:
                    if qa["Question"] == question:
                        found = True
                        break
            if not found:
                context.user_data.clear()
                return await update.message.reply_text("❌ Вопрос не найден.")
            await update.message.reply_text("📝 Введите новый текст ответа:")
        else:
            new_answer = update.message.text.strip()
            target = context.user_data['edit_target']
            for section, qas in knowledge_base.items():
                for qa in qas:
                    if qa["Question"] == target:
                        qa["answer"] = new_answer
            save_knowledge_to_excel()
            rebuild_question_maps()
            context.user_data.clear()
            await update.message.reply_text("✅ Ответ обновлён.")

    elif mode == 'delete':
        target = update.message.text.strip()
        removed = False
        for section in list(knowledge_base.keys()):
            qas = knowledge_base[section]
            filtered = [qa for qa in qas if qa["Question"] != target]
            if len(filtered) != len(qas):
                knowledge_base[section] = filtered
                removed = True
        if removed:
            save_knowledge_to_excel()
            rebuild_question_maps()
            await update.message.reply_text("🗑 Вопрос удалён.")
        else:
            await update.message.reply_text("❌ Вопрос не найден.")
        context.user_data.clear()
