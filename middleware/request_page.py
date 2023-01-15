from urllib.request import Request, urlopen
import bs4 as bs
import cloudscraper

scraper = cloudscraper.create_scraper()

def requestSample(u):
    req = scraper.get(u).text
    # req = Request(u, headers={"User-agent": "Mozilla/5.0"})
    # sauce = urlopen(req).read()
    soup = bs.BeautifulSoup(req, features="html.parser")
    return soup
