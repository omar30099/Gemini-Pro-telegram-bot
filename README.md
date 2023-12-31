# Gemini Pro Telegram Bot
Gemini Pro is a Telegram bot designed to generate conversational responses using a generative language model.
## Getting Started
To use the Gemini Pro bot, follow the steps below:
1. Clone the repository to your local machine:
```
git clone https://github.com/RahmatillaMarvel/gemini-pro-telegram-bot.git
```
2. Install the required dependencies using pip:

```
pip install -r requirements.txt
```

3. Obtain a Telegram Bot API token and a Google Cloud API key.
4. Replace the placeholder values in **main.py** and **gemini_pro.py** with your Telegram Bot API token and Google Cloud API key.

5. Run the bot using the following command:
```
python main.py
```
## Features
* **Chatting**: Start a conversation with the Gemini Pro bot by sending messages to it.
* **Generative Responses**: The bot generates responses using a pre-trained language model hosted on Google Cloud.
* **User History**: The bot maintains a chat history for each user to provide context for generating responses.
## Usage

1. Start the conversation by sending the '**/start**' command to the bot.
2. The bot will respond with a welcome message.
3. Send your messages to the bot, and it will generate responses based on the conversation history.

## Example
```
# Start the bot
python main.py
```

