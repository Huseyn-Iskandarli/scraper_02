from middleware.keep_alive import keep_alive
from middleware.request_page import requestSample
from middleware.page_scraper import page_scraper
from pymongo import MongoClient
from bson.objectid import ObjectId
import time
from datetime import datetime
import pytz
import sys, os

cluster = MongoClient("mongodb+srv://data_researcher_01:Gusik0915@newtestdb.pjkbipz.mongodb.net/?retryWrites=true&w=majority")
db = cluster["test_db"]
collection = db["test_col"]

try: 
	# LOGGING
	with open("logs.txt", "a") as file:
		file.write("\nStarted Scraping @ " + str(datetime.now(pytz.timezone("Asia/Baku"))))
		
	# All scraping will happen here =============================================
	# Collect all the links to the properties	todays_properties = []
	todays_properties = []
	pages = range(450)
	for i in pages:
		soup = requestSample("https://bina.az/alqi-satqi?page=" + str(i + 1))
		for x in soup.find_all("div", class_="items-i"):
			# if not posted today
			if not x.find("div", class_="city_when").text.replace(" ", "").split(",")[1][:5] == "dünən":
				# ignore those ads not posted today
				continue
			# collect the links from the ads posted today
			else:
				link = "https://" + "bina.az/" + x.find("a", class_="item_link").get('href')
				todays_properties.append(link)
		print("Page " + str(i+1) + " DONE")
	print(str(len(todays_properties)) + "properties")
	
	# LOGGING
	with open("logs.txt","a") as file:
		file.write("\nProperties to be scraped: " + str(len(todays_properties)))
 
 	# Scrap from the individual ad pages ========================================
	z = 1
	for url in todays_properties:
		try: 
			print("Proprty #: " + str(z), url)
			x =	page_scraper(url)
			x["link"] = url
			collection.insert_one(x)
			print(x["category"], x["price"], x["currency"], x["link"])
			z += 1
		except Exception as e:
			with open("logs.txt","a") as file:
				file.write("\nPage Error @ " + str(datetime.now(pytz.timezone("Asia/Baku"))) + " " + str(e) + x["link"])
			continue
		
	# All scraping ends here
	print("=== Action Complete ! ===")	

	# LOGGING
	with open("logs.txt","a") as file:
		file.write("\nDone Scraping @ " + str(datetime.now(pytz.timezone("Asia/Baku"))) + " // " + " Ads Scraped: " + str(len(todays_properties)))

except Exception as e:
	exc_type, exc_obj, exc_tb = sys.exc_info()
	fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

	error_message = "! SERVER DOWN ! Link: " + x["link"] + " " + str(e) + "line #: " + str(exc_tb.tb_lineno)

	# LOGGING
	with open("logs.txt","a") as file:
		file.write("\nError in Scraping @ " + str(datetime.now(pytz.timezone("Asia/Baku"))) + " " + error_message)
	print("===ERROR===", str(e))