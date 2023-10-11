import json, os, requests
from bs4 import BeautifulSoup
from card import Card

MAIN_URL = "https://list.am"

def parse():
    headers = {
        "Accept" :  "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "User-Agent":   "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"
        }
    BASE_URL = "https://www.list.am/category/23?n=0&bid=0&price2=500000&crc=0&gl=1"
    page_number = 1
    all_cards = []

    if not os.path.exists("output"):
        os.mkdir("output")

    while True:
        URL = f"https://www.list.am/category/23/{page_number}?n=0&bid=0&price2=500000&crc=0&gl=1"
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")

        new_url = soup.find("link", {"rel" : "canonical"}).get("href")
        print(BASE_URL, new_url)
        if page_number != 1 and new_url == BASE_URL:
            break

        post_containers = soup.findAll(class_="dl")

        for cont in post_containers:
            cards = cont.findAll("a")
            for card in cards:
                card_json = createCard(card)
                all_cards.append(card_json) if type(card_json) is dict else None
        page_number += 1

    with open("output/cards.json", "w", encoding="utf-8") as f:
        json.dump(all_cards, f, ensure_ascii=False, indent=4)

def createCard(card):
    card_link = card.get("href")
    if "/category" in card_link:
        return
    url = MAIN_URL+card_link
    title = card.find(class_="l").text
    price = card.find(class_="p").text
    place = card.find(class_="at").text
    img_url = card.find("img").get("data-original") if card.find("img").get("data-original") != None else card.find("img").get("src")
    card = Card(title)
    card.setPlace(place)
    card.setPrice(price)
    card.setImgUrl("https:"+img_url)
    card.setUrl(url)
    return card.toJson()
