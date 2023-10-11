import json

class Card:
    def __init__(self, title):
        self.title = title

    def setPlace(self, place):
        self.place = place

    def setUrl(self, url):
        self.url = url

    def setPrice(self, price):
        self.price = price

    def setImgUrl(self, img_url):
        self.img_url = img_url

    def toJson(self):
        json_object = {
            "title"   : self.title,
            "price"   : self.price,
            "place"   : self.place,
            "url"     : self.url,
            "img_url" : self.img_url
        }
        return json_object
