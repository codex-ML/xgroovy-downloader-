import telebot
import requests
from bs4 import BeautifulSoup
import os

# Replace 'YOUR_BOT_TOKEN' with your actual Telegram bot token
bot_token = '6396637491:AAGA8P4jxTIMwpn-sFe-COW0y1TdbVzwG9M'
bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start'])
def handle_start(message):
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
        download_video(last_link)

        # Send the downloaded video to the user
        video_file = open('evil_video.mp4', 'rb')
        bot.send_video(message.chat.id, video_file)
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

def download_video(url):
    file_name = 'evil_video.mp4'

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
