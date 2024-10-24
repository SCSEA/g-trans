import random
import telebot
from telebot import types
import requests
import json
import os
import platform
import webbrowser
from colorama import Fore, init
import time as t
import subprocess
import sys

def sleep():
    t.sleep(3)
sleep()

# clear screen
def clear_screen():
       os.system("cls" if os.name == "nt" else "clear")
clear_screen()


# Initialize colorama for terminal colors
init(autoreset=True)

# Install missing libraries
def install_packages():
    try:
        # Install packages
        os.system(f"{sys.executable} -m pip install requests >/dev/null 2>&1")
        os.system(f"{sys.executable} -m pip install telebot >/dev/null 2>&1")
        os.system(f"{sys.executable} -m pip install pystyle >/dev/null 2>&1")
        os.system(f"{sys.executable} -m pip install colorama >/dev/null 2>&1")
        os.system(f"{sys.executable} -m pip install json >/dev/null 2>&1")
        os.system(f"{sys.executable} -m pip install webbrowser >/dev/null 2>&1")
        
    except Exception as e:
        print(Fore.RED + f"Failed to install packages: {e}")

# Open a URL depending on the OS
def open_url(url):
    os_name = platform.system().lower()
    
    try:
        if 'linux' in os_name or 'termux' in os_name:
            os.system(f"xdg-open {url} >/dev/null 2>&1")
        elif 'windows' in os_name:
            os.system(f"start {url}")
        elif 'darwin' in os_name:  # macOS
            os.system(f"open {url}")
        else:
            webbrowser.open(url)
    except Exception as e:
        print(Fore.RED + f"Failed to open URL: {e}")

# Author and Version Information
__version__ = "1.0"
__author__ = "Yousuf Shafii Muhammad"
__contact__ = "Telegram: @Programmerboy1"
__description__ = """
This script is a Telegram bot that translates text between multiple languages using the Google Translate API.
The user can specify the source and target languages along with the text to be translated.
For educational purposes only. Unauthorized or illegal use is strictly prohibited.
"""

# Print Author and Version Information in terminal
def print_info():
    info = f"""
    Version: {__version__}
    Author: {__author__}
    Contact: {__contact__}
    Description: {__description__}
    """
    print(Fore.CYAN + info)
    return info

# Function to send version info to Telegram bot as well
def send_info_to_telegram(chat_id):
    info = print_info()
    bot.send_message(chat_id, info)

# Warnings
def print_warnings():
    warning = Fore.RED + "CAUTION: Use this script for educational purposes only!"
    disclaimer = Fore.YELLOW + "WARNING: The developer is not responsible for any misuse of this script."
    print(warning)
    print(disclaimer)
    return warning, disclaimer

# Bot Setup
#bot = telebot.TeleBot("YOUR_TELEGRAM_BOT_TOKEN")

bot = telebot.TeleBot(input("Enter Your Telegram Bot Token API : "))
#print(Fore.Blue + bot)

# Create keyboard for Telegram bot
def create_language_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [types.KeyboardButton(text=f'Code: ({key}) - {value["country"]}') 
               for key, value in language_codes.items()]
    keyboard.add(*buttons)
    return keyboard

# State management
user_states = {}

# Translation function
def tran(text, source_lang='auto', target_lang='ar'):
    url = 'https://translate.googleapis.com/translate_a/single?client=gtx&dt=t'
    pay = {'sl': source_lang, 'tl': target_lang, 'q': text}
    head = {'Content-Type': 'application/x-www-form-urlencoded'}
    
    res = requests.post(url, data=pay, headers=head)
    
    if res.status_code == 200:
        sen = json.loads(res.text)
        senn = ""
        for s in sen[0]:
            senn += s[0] if s[0] else ''
        return senn
    else:
        return "Translation failed. Please try again."

def print_banner():
    # Define the banner text
    banner = """
    ______        ________                                      __              __
   /      \\      /        |                                    /  |            /  |
  /$$$$$$  |     $$$$$$$$/______   ______   _______    _______ $$ |  ______   _$$ |_     ______    ______
  $$ | _$$/  ______ $$ | /      \\ /      \\ /       \\  /       |$$ | /      \\ / $$   |   /      \\  /      \\
  $$ |/    |/      |$$ |/$$$$$$  |$$$$$$  |$$$$$$$  |/$$$$$$$/ $$ | $$$$$$  |$$$$$$/   /$$$$$$  |/$$$$$$  |
  $$ |$$$$ |$$$$$$/ $$ |$$ |  $$/ /    $$ |$$ |  $$ |$$      \\ $$ | /    $$ |  $$ | __ $$ |  $$ |$$ |  $$/
  $$ \\__$$ |        $$ |$$ |     /$$$$$$$ |$$ |  $$ | $$$$$$  |$$ |/$$$$$$$ |  $$ |/  |$$ \\__$$ |$$ |
  $$    $$/         $$ |$$ |     $$    $$ |$$ |  $$ |/     $$/ $$ |$$    $$ |  $$  $$/ $$    $$/ $$ |
   $$$$$$/          $$/ $$/       $$$$$$$/ $$/   $$/ $$$$$$$/  $$/  $$$$$$$/    $$$$/   $$$$$$/  $$/
    """

    # Print the banner
    print(Fore.CYAN + banner + Fore.RESET)  # Reset color after printing

# Bot commands
@bot.message_handler(commands=['start'])
def start_command(message):
    send_info_to_telegram(message.chat.id)
    bot.send_message(message.chat.id, 'Welcome to the translation bot! Please select a source language.', reply_markup=create_language_keyboard())
    user_states[message.chat.id] = {'state': 'waiting_for_source_lang'}

@bot.message_handler(func=lambda message: user_states.get(message.chat.id, {}).get('state') == 'waiting_for_source_lang')
def choose_source_language(message):
    source_lang = message.text.split('(')[1][:2]  # Extract language code from button text
    if source_lang in language_codes:
        user_states[message.chat.id]['source_lang'] = source_lang
        user_states[message.chat.id]['state'] = 'waiting_for_target_lang'
        bot.send_message(message.chat.id, 'Please select a target language.', reply_markup=create_language_keyboard())
    else:
        bot.send_message(message.chat.id, 'Invalid selection. Please choose again.')

@bot.message_handler(func=lambda message: user_states.get(message.chat.id, {}).get('state') == 'waiting_for_target_lang')
def choose_target_language(message):
    target_lang = message.text.split('(')[1][:2]  # Extract language code from button text
    if target_lang in language_codes:
        user_states[message.chat.id]['target_lang'] = target_lang
        user_states[message.chat.id]['state'] = 'waiting_for_text'
        bot.send_message(message.chat.id, 'Please enter the text you want to translate.')
    else:
        bot.send_message(message.chat.id, 'Invalid selection. Please choose again.')

@bot.message_handler(func=lambda message: user_states.get(message.chat.id, {}).get('state') == 'waiting_for_text')
def translate_text(message):
    source_lang = user_states[message.chat.id].get('source_lang', 'auto')
    target_lang = user_states[message.chat.id].get('target_lang', 'ar')
    text = message.text
    translation = tran(text, source_lang, target_lang)
    bot.reply_to(message, f"Translation from {language_codes[source_lang]['country']} to {language_codes[target_lang]['country']}:\n\n{translation}")

    # Reset the user's state
    del user_states[message.chat.id]

# Dictionary of supported languages (expand as needed)
language_codes = {
    'af': {'country': 'Afrikaans', 'count': 'ZA'},
    'sq': {'country': 'Albanian', 'count': 'AL'},
    'am': {'country': 'Amharic', 'count': 'ET'},
    'ar': {'country': 'Arabic', 'count': 'SA'},
    'hy': {'country': 'Armenian', 'count': 'AM'},
    'az': {'country': 'Azerbaijani', 'count': 'AZ'},
    'eu': {'country': 'Basque', 'count': 'ES'},
    'be': {'country': 'Belarusian', 'count': 'BY'},
    'bn': {'country': 'Bengali', 'count': 'BD'},
    'bs': {'country': 'Bosnian', 'count': 'BA'},
    'bg': {'country': 'Bulgarian', 'count': 'BG'},
    'ca': {'country': 'Catalan', 'count': 'ES'},
    'ceb': {'country': 'Cebuano', 'count': 'PH'},
    'ny': {'country': 'Chichewa', 'count': 'MW'},
    'zh-CN': {'country': 'Chinese (Simplified)', 'count': 'CN'},
    'zh-TW': {'country': 'Chinese (Traditional)', 'count': 'TW'},
    'co': {'country': 'Corsican', 'count': 'FR'},
    'hr': {'country': 'Croatian', 'count': 'HR'},
    'cs': {'country': 'Czech', 'count': 'CZ'},
    'da': {'country': 'Danish', 'count': 'DK'},
    'nl': {'country': 'Dutch', 'count': 'NL'},
    'en': {'country': 'English', 'count': 'US'},
    'eo': {'country': 'Esperanto', 'count': 'PL'},
    'et': {'country': 'Estonian', 'count': 'EE'},
    'tl': {'country': 'Filipino', 'count': 'PH'},
    'fi': {'country': 'Finnish', 'count': 'FI'},
    'fr': {'country': 'French', 'count': 'FR'},
    'fy': {'country': 'Frisian', 'count': 'NL'},
    'gl': {'country': 'Galician', 'count': 'ES'},
    'ka': {'country': 'Georgian', 'count': 'GE'},
    'de': {'country': 'German', 'count': 'DE'},
    'el': {'country': 'Greek', 'count': 'GR'},
    'gu': {'country': 'Gujarati', 'count': 'IN'},
    'ht': {'country': 'Haitian Creole', 'count': 'HT'},
    'ha': {'country': 'Hausa', 'count': 'NG'},
    'haw': {'country': 'Hawaiian', 'count': 'US'},
    'he': {'country': 'Hebrew', 'count': 'IL'},
    'hi': {'country': 'Hindi', 'count': 'IN'},
    'hmn': {'country': 'Hmong', 'count': 'LA'},
    'hu': {'country': 'Hungarian', 'count': 'HU'},
    'is': {'country': 'Icelandic', 'count': 'IS'},
    'ig': {'country': 'Igbo', 'count': 'NG'},
    'id': {'country': 'Indonesian', 'count': 'ID'},
    'ga': {'country': 'Irish', 'count': 'IE'},
    'it': {'country': 'Italian', 'count': 'IT'},
    'ja': {'country': 'Japanese', 'count': 'JP'},
    'jw': {'country': 'Javanese', 'count': 'ID'},
    'kn': {'country': 'Kannada', 'count': 'IN'},
    'km': {'country': 'Khmer', 'count': 'KH'},
    'ko': {'country': 'Korean', 'count': 'KR'},
    'ku': {'country': 'Kurdish', 'count': 'IQ'},
    'ky': {'country': 'Kyrgyz', 'count': 'KG'},
    'la': {'country': 'Latin', 'count': 'VA'},
    'lv': {'country': 'Latvian', 'count': 'LV'},
    'lt': {'country': 'Lithuanian', 'count': 'LT'},
    'lb': {'country': 'Luxembourgish', 'count': 'LU'},
    'mk': {'country': 'Macedonian', 'count': 'MK'},
    'ml': {'country': 'Malayalam', 'count': 'IN'},
    'mn': {'country': 'Mongolian', 'count': 'MN'},
    'my': {'country': 'Burmese', 'count': 'MM'},
    'ne': {'country': 'Nepali', 'count': 'NP'},
    'no': {'country': 'Norwegian', 'count': 'NO'},
    'or': {'country': 'Odia', 'count': 'IN'},
    'ps': {'country': 'Pashto', 'count': 'AF'},
    'fa': {'country': 'Persian', 'count': 'IR'},
    'pl': {'country': 'Polish', 'count': 'PL'},
    'pt': {'country': 'Portuguese', 'count': 'PT'},
    'pa': {'country': 'Punjabi', 'count': 'IN'},
    'ro': {'country': 'Romanian', 'count': 'RO'},
    'ru': {'country': 'Russian', 'count': 'RU'},
    'sm': {'country': 'Samoan', 'count': 'WS'},
    'sg': {'country': 'Sango', 'count': 'CF'},
    'sr': {'country': 'Serbian', 'count': 'RS'},
    'si': {'country': 'Sinhalese', 'count': 'LK'},
    'sk': {'country': 'Slovak', 'count': 'SK'},
    'sl': {'country': 'Slovenian', 'count': 'SI'},
    'so': {'country': 'Somali', 'count': 'SO'},
    'es': {'country': 'Spanish', 'count': 'ES'},
    'su': {'country': 'Sundanese', 'count': 'ID'},
    'sw': {'country': 'Swahili', 'count': 'KE'},
    'sv': {'country': 'Swedish', 'count': 'SE'},
    'tl': {'country': 'Tagalog', 'count': 'PH'},
    'ta': {'country': 'Tamil', 'count': 'IN'},
    'te': {'country': 'Telugu', 'count': 'IN'},
    'th': {'country': 'Thai', 'count': 'TH'},
    'tr': {'country': 'Turkish', 'count': 'TR'},
    'uk': {'country': 'Ukrainian', 'count': 'UA'},
    'ur': {'country': 'Urdu', 'count': 'PK'},
    'vi': {'country': 'Vietnamese', 'count': 'VN'},
    'cy': {'country': 'Welsh', 'count': 'GB'},
    'xh': {'country': 'Xhosa', 'count': 'ZA'},
    'yi': {'country': 'Yiddish', 'count': 'IL'},
    'yo': {'country': 'Yoruba', 'count': 'NG'},
    'zu': {'country': 'Zulu', 'count': 'ZA'}
}

if __name__ == "__main__":
    install_packages()
    print_banner()
    open_url("https://t.me/programmerboy1")
    print_warnings()

    try:
        bot.infinity_polling(none_stop=True, timeout=60)
    except Exception as e:
        print(Fore.RED + "Error with Telegram bot:", e)
