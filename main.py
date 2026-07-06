from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

TOKEN = "APNA_BOT_TOKEN"
ADMIN_ID = 5668848369

NAME, AGE, GENDER, PROBLEM, ADDRESS = range(5)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalamualaikum\n\nApna Naam Likhiye:")
    return NAME

async def name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Umar Likhiye:")
    return AGE

async def age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["age"] = update.message.text

    keyboard = [["Mard", "Aurat"]]
    await update.message.reply_text(
        "Gender Chuniye:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=True,
        ),
    )
    return GENDER

async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["gender"] = update.message.text
    await update.message.reply_text("Bimari Ya Masla Likhiye:")
    return PROBLEM

async def problem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["problem"] = update.message.text
    await update.message.reply_text("Pura Address Likhiye:")
    return ADDRESS

async def address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["address"] = update.message.text

    msg = f"""
📋 Naya Mareez

👤 Naam: {context.user_data['name']}
🎂 Umar: {context.user_data['age']}
🚹 Gender: {context.user_data['gender']}
🩺 Masla: {context.user_data['problem']}
🏠 Address: {context.user_data['address']}
"""

    await context.bot.send_message(chat_id=ADMIN_ID, text=msg)

    await update.message.reply_text(
        "✅ Aapki Tafseel Jama Ho Gayi.\nJald Aapse Rabta Kiya Jayega."
    )

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cancel.")
    return ConversationHandler.END

app = Application.builder().token(TOKEN).build()

conv = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)],
        AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, age)],
        GENDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, gender)],
        PROBLEM: [MessageHandler(filters.TEXT & ~filters.COMMAND, problem)],
        ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, address)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

app.add_handler(conv)

if __name__ == "__main__":
    app.run_polling()
