from google import genai
import asyncio
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, ConversationHandler

WAITING_FOR_PROMPT = 1


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = 'Welcome to the better prompt bot.\nPlease send your prompt so I can improve it (send /quit for end)'
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Conversation ended. come back soon!')
    return ConversationHandler.END

TOKEN = "8286997548:AAGNAVERznnt7UpIYT01cvIlBq-NY_8ssqc"

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)

    quit_handler = CommandHandler('quit', cancel)

    application.add_handler(start_handler)
    application.add_handler(quit_handler)

    application.run_polling()


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)


    application.add_handler(start_handler)
    application.add_handler(echo_handler)

    application.run_polling()


# API_KEY = 'aa-HAveKxHZIz3RNRJvTukHw2EOa8zX6yiuHitfEum208F9ahIP'
#
# client = genai.Client(
#     api_key=API_KEY, http_options={"base_url": "https://api.avalai.ir"}
# )



# response = client.models.generate_content(
#     model="gemini-2.5-flash-lite", contents="given this promt {make a orange two headed cat that standing on a chair} you will make this promt better and more sutible for llms you will use all prompt engeenering prociples"
# )


# print(response.text)