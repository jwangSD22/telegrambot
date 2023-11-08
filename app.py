from flask import Flask, request, jsonify
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters
from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup, InputTextMessageContent, InlineQueryResultArticle
from uuid import uuid4
import logging
from html import escape
import telegram

app = Flask(__name__)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

GENDER, PHOTO, LOCATION, BIO = range(4)

bot = telegram.Bot(token='6489754794:AAEunRQpRZ5DWNqETweM76p8G-70iwVx4dM')


def start(update: Update, context):
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [["Boy", "Girl", "Other"]]

    update.message.reply_text(
        "Hi! My name is Professor Bot. I will hold a conversation with you. "
        "Send /cancel to stop talking to me.\n\n"
        "Are you a boy or a girl?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Boy or Girl?"
        ),
    )

    return GENDER

def gender(update: Update, context):
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        "I see! Please send me a photo of yourself, "
        "so I know what you look like, or send /skip if you don't want to.",
        reply_markup=ReplyKeyboardRemove(),
    )

    return PHOTO

def photo(update: Update, context):
    """Stores the photo and asks for a location."""
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download("user_photo.jpg")
    logger.info("Photo of %s: %s", user.first_name, "user_photo.jpg")
    update.message.reply_text(
        "Gorgeous! Now, send me your location please, or send /skip if you don't want to."
    )

    return LOCATION

def skip_photo(update: Update, context):
    """Skips the photo and asks for a location."""
    user = update.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    update.message.reply_text(
        "I bet you look great! Now, send me your location please, or send /skip."
    )

    return LOCATION

def location(update: Update, context):
    """Stores the location and asks for some info about the user."""
    user = update.message.from_user
    user_location = update.message.location
    logger.info(
        "Location of %s: %f / %f", user.first_name, user_location.latitude, user_location.longitude
    )
    update.message.reply_text(
        "Maybe I can visit you sometime! At last, tell me something about yourself."
    )

    return BIO

def skip_location(update: Update, context):
    """Skips the location and asks for info about the user."""
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    update.message.reply_text(
        "You seem a bit paranoid! At last, tell me something about yourself."
    )

    return BIO

def bio(update: Update, context):
    """Stores the info about the user and ends the conversation."""
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    update.message.reply_text("Thank you! I hope we can talk again some day.")

    return ConversationHandler.END

def cancel(update: Update, context):
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(), bot)
        application = Application.builder().token("6489754794:AAEunRQpRZ5DWNqETweM76p8G-70iwVx4dM").build()
        conversation_handler = ConversationHandler(
            entry_points=[CommandHandler("start", start)],
            states={
                GENDER: [MessageHandler(filters.Regex("^(Boy|Girl|Other)$"), gender)],
                PHOTO: [MessageHandler(filters.PHOTO, photo), CommandHandler("skip", skip_photo)],
                LOCATION: [MessageHandler(filters.LOCATION, location), CommandHandler("skip", skip_location)],
                BIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, bio)],
            },
            fallbacks=[CommandHandler("cancel", cancel)],
        )
        application.add_handler(conversation_handler)
        application.process_update(update)
    return jsonify({'status': 'ok'})

if __name__ == "__main__":
    app.run()