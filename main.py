from google import genai
import asyncio
import logging

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, ConversationHandler

BOT_TOKEN = '8286997548:AAGNAVERznnt7UpIYT01cvIlBq-NY_8ssqc'
WAITING_FOR_PROMPT = 1

async def improve_prompt(user_text):
    return 'we reached here good'


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = 'Welcome to the better prompt bot.\nPlease send your prompt so I can improve it (send /quit for end)'
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    return WAITING_FOR_PROMPT


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Conversation ended. come back soon!')
    return ConversationHandler.END


async def handle_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_input = update.message.text

    improved_text = await improve_prompt(user_input)
    print(improved_text)

    await update.message.reply_text(improved_text)

    await context.bot.send_message(chat_id=update.effective_chat.id, text='You can send another prompt to improve, or send /quit to end.')

    return WAITING_FOR_PROMPT


def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            WAITING_FOR_PROMPT: [
                # If text is sent, handle it as a prompt
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_prompt)
            ],
        },
        # If user sends /quit at any point, run the cancel function
        fallbacks=[CommandHandler("quit", cancel)],
    )

    application.add_handler(conv_handler)

    application.run_polling()


if __name__ == '__main__':
    main()

# API_KEY = 'aa-HAveKxHZIz3RNRJvTukHw2EOa8zX6yiuHitfEum208F9ahIP'
#
# client = genai.Client(
#     api_key=API_KEY, http_options={"base_url": "https://api.avalai.ir"}
# )



# response = client.models.generate_content(
#     model="gemini-2.5-flash-lite", contents="given this promt {make a orange two headed cat that standing on a chair} you will make this promt better and more sutible for llms you will use all prompt engeenering prociples"
# )


# print(response.text)