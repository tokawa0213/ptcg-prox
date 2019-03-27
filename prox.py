from bs4 import BeautifulSoup
from selenium import webdriver
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
#try lazy
from reportlab.pdfgen import canvas
import requests
import os
import re

def change_url(url):
    if len(url) == 20:
        return "https://www.pokemon-card.com/deck/confirm.html/deckID/" + url + "/"
    if "result.html" in url:
        return url.replace("result.html","confirm.html")
    if 'https://www.pokemon-card.com' not in url:
        return 'failure'
    return url

class Deck():
    def __init__(self,dcode):
        self.dcode = dcode
        self.dfolder_name = self.dcode.lstrip("https://www.pokemon-card.com/deck/confirm.html/deckID/").rstrip("/")
        self.image_base_link = "https://www.pokemon-card.com/card-search/details.php/card/"
        self.uri = dcode
        self.deck = []

    def scrape(self):
        print("Scraping...")
        driver = webdriver.PhantomJS()
        try:
            driver.get(self.uri)
            r = driver.page_source
            driver.close()
            driver.quit()
            soup = BeautifulSoup(r,"lxml")
            soup = soup.find(id="cardImagesView")
            c_list = soup.findAll(class_="cPos")
            tup = []
            for c in c_list:
                img = c.find("img")
                num = c.find("span")
                if num != None:
                    tup.append(num.text)
                try:
                    tup.append(re.sub("&amp;","&",img["alt"]))
                    tup.append(img["src"])
                    tup.append(img["id"].lstrip("img_"))
                except:
                    pass
                if len(tup) == 4:
                    self.deck.append(tup)
                    tup = []
        except:
            pass

    def download_img(self,id):
        print("Downloading image...")
        base_page_link = self.image_base_link + id
        print(base_page_link)
        r = requests.get(base_page_link)
        soup = BeautifulSoup(r.text,"lxml")
        image_link = "https://www.pokemon-card.com" + soup.find(class_="fit").get("src")
        os.system(
            "aria2c -x 16 -s 16  -o static/imdir/"+ id + ".jpg" + " " + image_link
        )

class PDF_generater():
    def __init__(self,url):
        self.image_path = "static/imdir"
        self.p_tate = 297 * mm
        self.p_yoko = 210 * mm
        self.c_tate = 88 * mm
        self.c_yoko = 63 * mm
        self.c_per_p_tate = self.p_tate//self.c_tate
        self.c_per_p_yoko = self.p_yoko//self.c_yoko
        self.c_per_p = int(self.c_per_p_yoko * self.c_per_p_yoko)
        self.mar_tate = 0.8*(self.p_tate-self.c_per_p_tate*self.c_tate)/(self.c_per_p_tate-1)
        self.mar_yoko = 0.8*(self.p_yoko-self.c_per_p_yoko*self.c_yoko)/(self.c_per_p_yoko-1)
        self.url = url

    def make_pdf(self,d):
        print("making pdf...")
        c = canvas.Canvas("static/" + self.url.lstrip("https://www.pokemon-card.com/deck/confirm.html/deckID/").rstrip("/") +".pdf")
        new_deck_info = []
        for f_info in d:
            c_num = int(f_info[1].rstrip("枚"))
            if f_info[0] == "on" and c_num != 0:
                for t in range(c_num):
                    new_deck_info.append(self.image_path+ "/" +str(f_info[2])+".jpg")
        new_deck_info = [new_deck_info[i:i+self.c_per_p] for i in range(0,len(new_deck_info),self.c_per_p)]
        for page in new_deck_info:
            x_pos = 0
            y_pos = 0
            for num,image_path in enumerate(page):
                if num%self.c_per_p_yoko == 0 and num !=0:
                    x_pos = 0
                    y_pos += self.c_tate
                image = ImageReader(image_path)
                c.drawImage(image,x_pos,y_pos,width=self.c_yoko,height=self.c_tate)
                x_pos += self.c_yoko
            c.showPage()
        return c.getpdfdata()

if __name__ == "__main__":
    d = Deck()
    d.scrape()
    d.download_img()