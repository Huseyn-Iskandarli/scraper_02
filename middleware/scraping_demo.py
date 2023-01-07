twebimport bs4 as bs
import csv
import time
import random
import multiprocessing

from requestData import requestSample 
from formatData import formatSample
import exportData

numberOfPages = []
# How many pages?
for i in range(217):
    numberOfPages.append(i+1)

types = ["kohne-tikili", "yeno-tikili", "menziller", ]

url = "https://bina.az/baki/alqi-satqi/menziller/kohne-tikili?page="
doc = "BinaAZ_11.12.20_All.txt"

def scrape(pagenum, url_1, doc_1):
        properties = []  
        # New Buildings
        # "https://bina.az/baki/alqi-satqi/menziller/yeni-tikili?page="

        # Old Buildings
        # "https://bina.az/baki/alqi-satqi/menziller/kohne-tikili?page="

        # All Buildings  
        # "https://bina.az/baki/alqi-satqi/menziller?page="

        url = url_1 +str(pagenum)
        soup = bs.BeautifulSoup(requestSample(url), "lxml")
        try: 
            page = formatSample(soup)
        except:
            page = []
        properties += page
        exportData.exportSampleTXT(properties,doc_1)
        print("Page " + str(pagenum) + " done")

if __name__ == "__main__":
    # file = open(doc, "a+", encoding="utf-8")
    # file.write('Price, Currency, Location, Area, Rooms, Floor, FloorMax, isOld, isNew\n')
    # file.close()
    for i in numberOfPages:
        print(i,"===========")
        p = multiprocessing.Process(target=scrape, args=(i,url,doc))
        p.start()
        p.join()