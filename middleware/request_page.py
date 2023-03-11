import urllib
import requests
import os
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import cloudscraper
from dotenv import load_dotenv

load_dotenv()
SCRAPER_API = os.getenv("Scraper_ANT_API")

def requestSample(u, type):
    if type == "ordinary":    
        # ===== CLOUDSCRAPER =====
        scraper = cloudscraper.create_scraper()
        req = scraper.get(u).text
        # req = Request(u, headers={"User-agent": "Mozilla/5.0"})
        # sauce = urlopen(req).read()
        soup = BeautifulSoup(req, features="html.parser")
    elif type == "ScraperAnt":
        # ===== SCRAPER ANT SCRAPER =====
        sa_key = SCRAPER_API
        sa_api = 'https://api.scrapingant.com/v2/general'
        qParams = {'url': 'https://bina.az/items/3023313', 'x-api-key': sa_key}
        reqUrl = f'{sa_api}?{urllib.parse.urlencode(qParams)}'  
        r = requests.get(reqUrl)
        # print(r.text) # --> html
        soup = BeautifulSoup(r.content, 'html.parser')
    elif type == "old":
        req = Request(u, headers={"User-agent": "Mozilla/5.0"})
        sauce = urlopen(req).read()
        del req
        soup = BeautifulSoup(sauce, "lxml")
        del sauce
    else:
        print("Scraper not chosen")
    
    return soup