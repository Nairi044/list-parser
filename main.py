#!venv/bin/python3.10

import telebot
import requests, os, json
import config, parser
from PIL import Image

bot = telebot.TeleBot(config.BOT_TOKEN)

# if __name__ == "__main__":
#     parser.parse()
need_to_send = True
headers = {
    "Accept" :  "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "User-Agent":   "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"
    }

def download_file(url, local_filename):
    global headers
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open(local_filename+".webp", 'wb') as f:
            f.write(response.content)
        print(f"Image downloaded successfully as {local_filename}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")
    im = Image.open(f"{local_filename}.webp").convert("RGB")
    im.save(f"{local_filename}.jpeg", "jpeg")
    os.remove(local_filename+".webp")

@bot.message_handler(commands=["start", "help"])
def start(message):
    global need_to_send
    need_to_send = True
    bot.send_message(message.chat.id, "Ողջույն, դուք գտնվում եք աշխարհի ամենագարլախ բոտում։ Շնորհակալություն մեր ծառայություններից օգտվելու համար։ ❤️")

@bot.message_handler(commands=["start_tracking"])
def start_tracking(message):
    global need_to_send
    if not need_to_send:
        return
    with open("output/cards.json", "r") as f:
        cards = json.loads(f.read())
    for card in cards:
        download_file(card["img_url"], "image")
        text = f'{card["title"]}\n'
        text += f'{card["price"]}  |  {card["place"]}\n'
        text += f'{card["url"]}'
        with open("image.jpeg", "rb") as photo:
            sent_photo = bot.send_photo(message.chat.id, photo, caption=text)
        os.remove("image.jpeg")

@bot.message_handler(commands=["stop"])
def start(message):
    global need_to_send
    need_to_send = False
    bot.send_message(message.chat.id, "Լավ դե սկտր: Մինչեւ /start չգրես, իմ փայից պատասխանողի ․․․🖕🤬")

@bot.message_handler(content_types=["text"])
def reply(message):
    if not need_to_send:
        return
    bot.send_message(message.chat.id, message.text)

bot.infinity_polling()
