import pathlib
import textwrap
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
import google.generativeai as genai
import json
import os
import logging
import PIL.Image
from io import BytesIO
import requests

API_KEY = "AIzaSyA7xWfA-t4oVuOgBzMgnMbnq1VLwptKNPI"

# ... (your existing code)

# Your existing code...


def generate_response(question, chat_history):
  try:
    url = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key=" + API_KEY

    headers = {'Content-Type': 'application/json'}

    data = {
        "contents":
        chat_history + [{
            "role":
            "user",
            "parts": [{
                "text":
                "System: Your name is Gemini Pro. Try to speak clearly and shortly"
            }]
        }, {
            "role":
            "model",
            "parts": [{
                "text":
                "Ok. Gotcha. I'm a Gemini Pro. How can I help you?"
            }]
        }, {
            "role": "user",
            "parts": [{
                "text": question
            }]
        }]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    generated_response = response.json(
    )['candidates'][0]['content']['parts'][0]['text']

    user_message = {"role": "user", "parts": [{"text": question}]}
    assistant_message = {
        "role": "model",
        "parts": [{
            "text": generated_response
        }]
    }

    all_texts = ''
    for dicts in chat_history:
      all_texts += dicts['parts'][0]['text']
    if len(all_texts) > 100000:
      chat_history = []

    chat_history.append(user_message)
    chat_history.append(assistant_message)
    print(chat_history)
    return generated_response, chat_history
  except Exception as e:
    print(e)
    print(
        e.response.json())  # Use e.response.json() instead of response.json()
    return 'Something went wrong. Please try again', chat_history


# Function to handle text messages
def handle_message(update: Update, context: CallbackContext):
  user_message = update.message.text
  global chat

  if chat is None:
    chat = model.start_chat(history=[])
  else:
    print(chat.history)

  # Check if the message contains keywords related to medicine subjects
  if any(keyword in user_message.lower() for keyword in medicine_keywords):
    # Use the generate_response function to get the AI-generated response
    generated_response, chat.history = generate_response(
        user_message, chat.history)

    # Send the AI-generated response back to the user
    update.message.reply_text(generated_response)
  else:
    # If the message doesn't contain medicine-related keywords, inform the user
    update.message.reply_text(
        "Sorry, this topic is not allowed. Please stick to medicine-related subjects."
    )

  # Inside the message_handler function
  async def message_handler(message: types.Message):
    await bot.send_chat_action(message.chat.id, 'typing')

    user_id = message.from_user.id
    user_data = user_data_dict.get(user_id)
    if not user_data:
      user_data = UserData()
      user_data_dict[user_id] = user_data

    response, user_data.chat_history = generate_response(
        message.text, user_data.chat_history)
    parse_mode = types.ParseMode.MARKDOWN if any(
        markdown_chars in response
        for markdown_chars in ['*', '_', '`']) else types.ParseMode.HTML

    print("Response before sending:",
          response)  # Print the response before sending

    await message.reply(response, parse_mode=parse_mode)


# Function to handle photo messages
def handle_photo(update: Update, context: CallbackContext):
  photo = update.message.photo[-1]
  file = context.bot.get_file(photo.file_id)
  file.download('photo.jpg')
  img = PIL.Image.open('photo.jpg')

  user_message = update.message.caption or "What's in the picture? Watch carefully and describe all details."

  vision_model = genai.GenerativeModel('gemini-pro-vision')

  response = vision_model.generate_content([user_message, img], stream=False)
  response.resolve()

  # Use the generate_response function to get the AI-generated response
  generated_response, chat.history = generate_response(user_message,
                                                       chat.history)

  # Send the AI-generated response back to the user
  update.message.reply_text(textwrap.indent(response.text, '> '))
  update.message.reply_text(generated_response)


# gemini_pro.py


def handle_photo_processing(user_message, photo):
  # Your logic to process the photo using gemini vision pro
  # ...

  # Placeholder response for testing
  return "Processed photo response", []


# Main function


def main():
  TOKEN = os.getenv("TELEGRAM_API_KEY")
  updater = Updater(TOKEN, use_context=True)
  dp = updater.dispatcher

  dp.add_handler(CommandHandler("start", start))
  dp.add_handler(
      MessageHandler(Filters.text & ~Filters.command, handle_message))
  dp.add_handler(MessageHandler(Filters.photo, handle_photo))

  updater.start_polling()
  updater.idle()


if __name__ == '__main__':
  main()
