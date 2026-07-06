from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

TOKEN = "APNA_BOT_TOKEN_YAHAN"
ADMIN_ID = 5668848369

NAME, AGE, GENDER, CITY, DISEASE = range(5)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["🩺 Naya Mashwara"]]
    await update.message.reply_text(
        "Assalamu Alaikum\n\nRoohani Markaz me Khush Aamdeed.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
        ),
    )


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Apna Naam Likhiye",
        reply_markup=ReplyKeyboardRemove(),
    )
    return NAME


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Apni Umar Likhiye")
    return AGE


async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["age"] = update.message.text

    keyboard = [["Male", "Female"]]

    await update.message.reply_text(
        "Gender Select Kare",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=True,
        ),
    )
    return GENDER


async def get_gender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["gender"] = update.message.text

    await update.message.reply_text(
        "Apna Shehar Likhiye",
        reply_markup=ReplyKeyboardRemove(),
    )
    return CITY


async def get_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["city"] = update.message.text
    await update.message.reply_text("Apni Bimari Tafseel Se Likhiye")
    return DISEASE


async def get_disease(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["disease"] = update.message.text

    text = f"""
🩺 Naya Mashwara

👤 Naam: {context.user_data['name']}
🎂 Umar: {context.user_data['age']}
👤 Gender: {context.user_data['gender']}
🏙 Shehar: {context.user_data['city']}

📝 Bimari:
{context.user_data['disease']}
"""

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=text,
    )

    await update.message.reply_text(
        "✅ Aapka Mashwara Safalta Se Submit Ho Gaya."
    )

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Cancel",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


def main():
    app = Application.builder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            MessageHandler(
                filters.Regex("^🩺 Naya Mashwara$"),
                menu,
            ),
        ],
        states={
            NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)
            ],
            AGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)
            ],
            GENDER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_gender)
            ],
            CITY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_city)
            ],
            DISEASE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_disease)
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel)
        ],
    )

    app.add_handler(conv)
    app.add_handler(CommandHandler("start", start))

    print("Bot Started...")
    app.run_polling()


if __name__ == "__main__":
    app.run_polling()
