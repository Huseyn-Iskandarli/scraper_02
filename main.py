# from middleware.keep_alive import keep_alive
from middleware.request_page import requestSample
from middleware.page_scraper import page_scraper
from pymongo import MongoClient
from bson.objectid import ObjectId
import time
from datetime import datetime
import pytz
import os
from dotenv import load_dotenv
import time


# Time track for logging
start = time.time()

# Connecting to DB
load_dotenv()
DB_URL = os.getenv("DB_URL")
cluster = MongoClient(DB_URL)
db = cluster["test_db"]
collection = db["test_col"]

# try: 

# LOGGING
with open("logs.txt", "a") as file:
	file.write("\nStarted Scraping @ " + str(datetime.now(pytz.timezone("Asia/Baku"))))
	
# All scraping will happen here =============================================
# Collect all the links to the properties	todays_properties = []
todays_properties = []
pages = range(300)
for i in pages:
	try:
		soup = requestSample("https://bina.az/alqi-satqi?page=" + str(i + 1), "ordinary")
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
	except:
		continue
print(str(len(todays_properties)) + "properties")
    

# LOGGING
with open("logs.txt","a") as file:
	file.write("\nProperties to be scraped: " + str(len(todays_properties)))

# Scrap from the individual ad pages ========================================
z = 0
error_counter = 0
for url in todays_properties:
	try: 
		print("Property #: " + str(z) + " " + str(url))
		x = 0
		tries = 0
		while tries < 3:
			try:
				x =	page_scraper(url,"new")
				tries += 3
			except:
				tries += 1
		if x != 0:
			x["link"] = url
			collection.insert_one(x)
			print(x["category"], x["price"], x["currency"], x["link"])
			z += 1
		else:
			continue
	except Exception as e:
		error_counter += 1
		with open("logs.txt","a") as file:
			file.write("\nPage Error @ " + str(datetime.now(pytz.timezone("Asia/Baku"))) + " " + str(e) + " " + x["link"])
		continue

# All scraping ends here
print("=== Action Complete | Pages with Errors: " + str(error_counter))	

end = time.time()

time_taken = end-start

# LOGGING
with open("logs.txt","a") as file:
	file.write("\nDone Scraping @ " + str(datetime.now(pytz.timezone("Asia/Baku"))) + " // " + "Ads Scraped: " + str(z) + " Time Taken: " + str(time_taken))

# Send email on completion of the scraping for day
import ssl
import smtplib
from email.message import EmailMessage

email_password = os.getenv("EMAIL_PASSWORD")

from_email      = "huseyn.iskandarli@gmail.com"
to_email        = "huseyn_isk@hotmail.com"
from_password   = email_password

subject = "Bina AZ Scraping DONE"
body = "Time done: " + str(datetime.now(pytz.timezone("Asia/Baku"))) + "\n" + "Properties scraped / Out of: " + str(z) + " / " + str(len(todays_properties))  + "\n" + "Time taken: " + str(time_taken/3600)

em = EmailMessage()

em["from"] = from_email
em["to"] = to_email
em["subject"] = subject
em.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
    smtp.login(from_email, email_password)
    smtp.sendmail(from_email, to_email, em.as_string())

# except Exception as e:
# 	exc_type, exc_obj, exc_tb = sys.exc_info()
# 	fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

# 	error_message = "! SERVER DOWN ! Link: " + x["link"] + " " + str(e) + "line #: " + str(exc_tb.tb_lineno)

# 	# LOGGING
# 	with open("logs.txt","a") as file:
# 		file.write("\nError in Scraping @ " + str(datetime.now(pytz.timezone("Asia/Baku"))) + " " + error_message)
# 	print("===ERROR===", str(e))