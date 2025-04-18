
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from config import BOT_TOKEN

from handlers.start import start
from handlers.callback import handle_callback
from handlers.admin import reload_excel, show_stats, broadcast
from handlers.edit import add_question, edit_question, delete_question, handle_edit_flow
from handlers.help import help_command
from handlers.user import handle_message

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("reload", reload_excel))
    app.add_handler(CommandHandler("stats", show_stats))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("add", add_question))
    app.add_handler(CommandHandler("edit", edit_question))
    app.add_handler(CommandHandler("delete", delete_question))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_edit_flow), group=1)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.add_handler(CallbackQueryHandler(handle_callback))

    print("✅ Бот запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
