import requests
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, ConversationHandler, filters, CallbackQueryHandler


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def movie_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query.data
    print(query, ' is the query')
    url = 'https://imdb-api.com/en/API/Title/k_28bw6iz0/' + update.callback_query.data
    response = requests.request("GET", url, headers={}, params={})
    print(response.text.encode('utf8'))
    data = response.json()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=data['title'])
    await context.bot.send_message(chat_id=update.effective_chat.id, text=data['plot'])
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=data['image'])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="What movie are you looking for?")

    return 0

IMDB_API_ENDPOINT = 'https://imdb-api.com/en/API/SearchMovie/'
IMDB_API_KEY = 'k_28bw6iz0'


async def movie_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    movie_title = update.message.text
    print(movie_title + ' is the movie title')
    url = IMDB_API_ENDPOINT + IMDB_API_KEY + '/' + movie_title
    response = requests.request("GET", url, headers={}, params={})
    print(response.text.encode('utf8'))
    data = response.json()
    if not data['results']:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="No movie found")
        return ConversationHandler.END
    else:
        buttons = []
        for result in data['results']:
            buttons.append([InlineKeyboardButton(text=result['title'], callback_data=result['id'])])
        keyboard = InlineKeyboardMarkup(buttons)
        message = 'Please select a movie:'
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message, reply_markup=keyboard)
        application.add_handler(CallbackQueryHandler(movie_callback))
        return ConversationHandler.END

if __name__ == '__main__':
    application = ApplicationBuilder().token('5836901752:AAEcpwk7BxdeovucyUkEQfKygc7Alytc9fQ').build()

    movie_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            0: [MessageHandler(filters.TEXT, movie_handler)]
        },
        fallbacks=[]
    )
    application.add_handler(movie_handler)

    application.run_polling()
