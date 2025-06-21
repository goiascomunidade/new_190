import os
import telebot
from prompt_loader import load_sys_prompt
from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')

bot = telebot.TeleBot(TELEGRAM_API_KEY)
open_ai_client = OpenAI(api_key=OPENAI_API_KEY)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    print('[INFO] start command received.')
    bot.send_message(message.chat.id, "Olá! Como posso ajudar você?")

@bot.message_handler(content_types=['text'])
def process_text_report(message):
    print('[INFO] message received.')

    response = open_ai_client.responses.parse(
        model='chatgpt-4o-latest',
        input=[{"role": "system", "content": load_sys_prompt()},
               {"role": "user", "content": message.text}]
    )

    bot.send_message(message.chat.id, response.output_text)
    print('[INFO] message response sent.')
    

@bot.message_handler(content_types=['voice'])
def process_audio_report(message):
    print('[INFO] audio received.')
    file_id = message.voice.file_id
    file_url = bot.get_file_url(file_id)
    print('[INFO] audio file url: ' + file_url)

    transcription = []
    
    with open(file_url, 'r') as audio_file:
        transcription = open_ai_client.audio.transcriptions.create(
            model="gpt-4o-transcribe", 
            file=audio_file, 
            response_format="text"
        )
    
    print(transcription)


def main():
    bot.polling()


if __name__ == '__main__':
    main()