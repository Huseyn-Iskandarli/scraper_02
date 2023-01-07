from urllib.request import Request, urlopen
import bs4 as bs


def requestSample(u):
    req = Request(u, headers={"User-agent": "Mozilla/5.0"})
    sauce = urlopen(req).read()
    soup = bs.BeautifulSoup(sauce, "lxml")
    return soup
