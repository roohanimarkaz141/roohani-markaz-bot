from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

# ==========================
# CONFIG
# ==========================
BOT_TOKEN = "YOUR_BOT_TOKEN"
ADMIN_ID = 5668848369

# ==========================
# STATES
# ==========================
MENU, NAME, MOTHER, AGE, GENDER, PROBLEM  = range(7)

# ==========================
# START
# ==========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["📿 Istikhara"],
        ["🕋 Roohani Ilaj"],
        ["📜 Taweez"],
        ["🤲 Wazifa"],
        ["☎️ Ham se Rabta"],
    ]

    await update.message.reply_text(
        "🌙 Assalamu Alaikum\n\n"
        "Roohani Markaz me khush aamdeed.\n\n"
        "Neeche se ek option select karein.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
        ),
    )

    return MENU


# ==========================
# MENU
# ==========================
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["service"] = update.message.text

    await update.message.reply_text(
        "Apna Poora Naam Likhiye:",
        reply_markup=ReplyKeyboardRemove(),
    )

    return NAME


# ==========================
# NAME
# ==========================
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["name"] = update.message.text

    await update.message.reply_text(
        "Walida Ka Naam Likhiye:"
    )

    return MOTHER


# ==========================
# MOTHER
# ==========================
async def get_mother(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["mother"] = update.message.text

    await update.message.reply_text(
        "Umar Likhiye:"
    )

    return AGE


# ==========================
# AGE
# ==========================
async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["age"] = update.message.text

    keyboard = [["Mard", "Aurat"]]

    await update.message.reply_text(
        "Gender Select Karein:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=True,
        ),
    )

    return GENDER


# ==========================
# GENDER
# ==========================
async def get_gender(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["gender"] = update.message.text

    await update.message.reply_text(
        "Apna Masla Tafseel Se Likhiye:",
        reply_markup=ReplyKeyboardRemove(),
    )

    return PROBLEM


# ==========================
# PROBLEM
# ==========================
async def get_problem(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["problem"] = update.message.text

    await update.message.reply_text(
        "Agar Photo bhejna chahein to bhej dein.\n\n"
        "Ya /skip likh dein."
    )

    caption = f"""
🆕 Nayi Request

Service:
{context.user_data['service']}

Naam:
{context.user_data['name']}

Walida:
{context.user_data['mother']}

Umar:
{context.user_data['age']}

Gender:
{context.user_data['gender']}

Masla:
{context.user_data['problem']}
"""

    
            ADMIN_ID,
            file_id,
            caption=caption,
        )

    else:

        await context.bot.send_message(
            ADMIN_ID,
            caption,
        )

    await update.message.reply_text(
        "✅ Aapki Request Submit Ho Gayi.\n\nIn Sha Allah Jald Rabta Kiya Jayega."
    )

    return ConversationHandler.END


# ==========================
# SKIP
# ==========================
async def skip(update: Update, context: ContextTypes.DEFAULT_TYPE):

    caption = f"""
🆕 Nayi Request

Service:
{context.user_data['service']}

Naam:
{context.user_data['name']}

Walida:
{context.user_data['mother']}

Umar:
{context.user_data['age']}

Gender:
{context.user_data['gender']}

Masla:
{context.user_data['problem']}
"""

    await context.bot.send_message(
        ADMIN_ID,
        caption,
    )

    await update.message.reply_text(
        "✅ Request Submit Ho Gayi."
    )

    return ConversationHandler.END


# ==========================
# CANCEL
# ==========================
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Cancelled."
    )

    return ConversationHandler.END


# ==========================
# MAIN
# ==========================
def main():

    app = Application.builder().token(BOT_TOKEN).build()

    conv = ConversationHandler(

        entry_points=[
            CommandHandler("start", start),
        ],

        states={

            MENU: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    menu,
                )
            ],

            NAME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_name,
                )
            ],

            MOTHER: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_mother,
                )
            ],

            AGE: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_age,
                )
            ],

            GENDER: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_gender,
                )
            ],

            PROBLEM: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_problem,
                )
            ],


                CommandHandler(
                    "skip",
                    skip,
                ),
            ],
        },

        fallbacks=[
            CommandHandler(
                "cancel",
                cancel,
            )
        ],
    )

    app.add_handler(conv)

    print("Bot Started...")

    app.run_polling()


if __name__ == "__main__":
    main()
