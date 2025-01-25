from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)

# Replace 'YOUR_API_TOKEN' with your bot's API token
API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
PASSWORD = "sandeep"  # Set your password here

# Conversation states
ASK_PASSWORD = 1


# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! Please enter the password to receive the image."
    )
    return ASK_PASSWORD


# Password validation handler
async def validate_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == PASSWORD:
        await update.message.reply_text("Password is correct! Sending the image...")

        # Send the image
        chat_id = update.effective_chat.id
        image_path = "./image.jpg"  # Replace with your image path

        with open(image_path, "rb") as image:
            await context.bot.send_photo(chat_id=chat_id, photo=image)

        await update.message.reply_text("Here is your image. Have a great day!")

        # End the conversation
        return ConversationHandler.END
    else:
        await update.message.reply_text("Incorrect password. Please try again.")
        # Stay in ASK_PASSWORD state
        return ASK_PASSWORD


# Cancel handler
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END


# Main function
def main():
    application = Application.builder().token(API_TOKEN).build()
    print("application running .......")
    # Define the conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_PASSWORD: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, validate_password)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Add the conversation handler to the application
    application.add_handler(conv_handler)

    # Start the bot
    print("Bot is running...")
    application.run_polling()


if __name__ == "__main__":
    main()
