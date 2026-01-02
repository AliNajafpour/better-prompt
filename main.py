from google import genai
import asyncio
import logging
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, ConversationHandler

import os
from dotenv import load_dotenv

load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")
GOOGLE_TOKENS = os.getenv("GOOGLE_TOKENS").split(',')



logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


WAITING_FOR_PROMPT = 1
with open('prompt_base.txt', 'r') as f:
    prompt_base = f.read()

async def improve_prompt(user_text, prompt_base, api_token):

    client = genai.Client(api_key=api_token)

    response = client.models.generate_content(model='gemma-3-27b-it', contents=prompt_base + user_text)

    return response.text


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    text = '''Welcome to Better Prompt! 🚀\nSend any prompt, and get a clearer, stronger, AI-optimized version.\n⚡ Early development — more features coming soon!\nIdeas or issues? Contact: @Ali_Najafpour07\n(send /quit for end)'''
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    
    return WAITING_FOR_PROMPT


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Conversation ended. come back soon! (send /start to start again)')
    return ConversationHandler.END


async def handle_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_input = update.message.text

    improved_text = await improve_prompt(user_input, prompt_base, random.choice(GOOGLE_TOKENS))
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
        allow_reentry=True
    )

    application.add_handler(conv_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
