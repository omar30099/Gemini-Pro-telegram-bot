import requests
import json

API_KEY = "Your API"

def generate_response(question, chat_history):
    try:
        url = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key=" + API_KEY

        headers = {'Content-Type': 'application/json'}

        data = {
            "contents":  chat_history+ [
                {
                    "role": "user",
                    "parts": [{"text": "System: Your name is Gemini Pro. Try to speak clearly and shortly"}]
                },
                
                {
                    "role": "model",
                    "parts": [{"text": "Ok. Gotcha. I'm a Gemini Pro. How can I help you?"}]
                }
                ,
                {
                    
                    "role": "user",
                    "parts": [{"text": question}]
                }
            ]
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        generated_respond = response.json()['candidates'][0]['content']['parts'][0]['text']

        user_message = {"role": "user", "parts": [{"text": question}]}
        assistant_message = {"role": "model", "parts":  [{"text": generated_respond}]}

        all_texts = ''
        for dicts in chat_history:
            all_texts += dicts['parts'][0]['text']
        if len(all_texts) > 100000 :
            chat_history = []

        chat_history.append(user_message)
        chat_history.append(assistant_message)
        print(chat_history)
        return generated_respond, chat_history
    except Exception as e:
        print(e)
        print(response.json())
        return 'Something went wrong. Please try again', chat_history
