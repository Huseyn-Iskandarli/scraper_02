from middleware.request_page import requestSample
import datetime
import pytz
import time

def page_scraper(url, method):
	soup = requestSample(url, "old")
	# with open("test_html.txt", "a", encoding="utf-8") as file:
	# 	file.write(str(soup) + "\n ====================================================================")

	if(method == "old"):
		
		price = float(soup.find("span", class_="price-val").text.replace(" ",""))
		currency = str(soup.find("span", class_="price-cur").text)
		lat = float(soup.find(id="item_map").get("data-lat"))
		lon = float(soup.find(id="item_map").get("data-lng"))	

		# Filler in case there is no table on page
		repaired = 			"N/A"
		district = 			"N/A"
		category = 			"N/A"
		area = 				"N/A"
		outer_area = 		"N/A"
		rooms = 			"N/A"
		floor_actual = 		"N/A"
		floor_max = 		"N/A"
		dateScraped =		datetime.datetime.now(pytz.timezone("Asia/Baku")) - datetime.timedelta(days=1)
		datePosted = 		"N/A"

		# Repaired
		for z in soup.find_all("tr"):
				repaired_array = []
				for t in z.find_all("td"):
						repaired_array.append(t.text)
				if repaired_array[0] == "Təmir" and repaired_array[1] == "var":
						repaired = True
						break
				else:
						repaired = False
		# District
		c = soup.find("ul", class_="locations")
		for z in c.find_all("li"):
				if z.text[-2:] == "r.":
					district = z.text[:-2].strip()
					break
				else:
					district = "N/A"
		# Category
		for z in soup.find_all("tr"):
				category_array = []
				for t in z.find_all("td"):
					category_array.append(t.text)
				if category_array[0] == "Kateqoriya":
					category = category_array[1]
					break
		# Area
		for z in soup.find_all("tr"):
				area_array = []
				for t in z.find_all("td"):
					area_array.append(t.text)
				if area_array[0] == "Sahə":
					if area_array[1].split(" ")[1] == "sot":
						area = "N/A"
						outer_area = float(area_array[1].split(" ")[0])
						break
					elif area_array[1].split(" ")[1] == "m²":
						area = float(area_array[1].split(" ")[0])
						outer_area = "N/A"
						break
					else:
						area = "N/A"
						outer_area = "N/A"
						break
				else:
					area = "N/A"
					outer_area = "N/A"
		#Outer Area
		for z in soup.find_all("tr"):
			if outer_area == "N/A":
				area_array = []
				for t in z.find_all("td"):
					area_array.append(t.text)
				if area_array[0] == "Torpaq sahəsi":
					if area_array[1].split(" ")[1] == "sot":
						outer_area = float(area_array[1].split(" ")[0])
						break
					else:
						outer_area = "N/A"
						break
				else:
					outer_area = "N/A"
			else:
				break
		# Rooms
		for z in soup.find_all("tr"):
				rooms_array = []
				for t in z.find_all("td"):
					rooms_array.append(t.text)
				if rooms_array[0] == "Otaq sayı":
					rooms = int(rooms_array[1])
					break
				else:
					rooms = "N/A"
		# Floor Actual + Max
		for z in soup.find_all("tr"):
				floor_actual_array = []
				for t in z.find_all("td"):
					floor_actual_array.append(t.text)
				if floor_actual_array[0] == "Mərtəbə":
					l = floor_actual_array[1].split(" ")
					floor_actual = int(l[0])
					floor_max = int(l[2])
					break
				else:
					floor_actual = "N/A"
					floor_max = "N/A"
		
  		# Date Posted
		time_soup = soup.find("div", class_="item_info").find_all("p")
		hour = time_soup[2].text.split(" ")[2].split(":")[0]
		minute = time_soup[2].text.split(" ")[2].split(":")[1]
		datePosted = datetime.datetime.now(pytz.timezone("Asia/Baku")).replace(hour=int(hour), minute=int(minute)) - datetime.timedelta(days=1)

		del soup
		return {
			'price': 				price,
			'currency': 			currency,
			'lat': 					lat,
			'lon': 					lon,
			'repaired': 			repaired,
			'district': 			district,
			'category': 			category,
			'area': 				area,
			'outer_area':			outer_area,
			'rooms': 				rooms,
			'floor_actual': 		floor_actual,
			'floor_max': 			floor_max,
			'date_scraped':			dateScraped,
			'date_posted':			datePosted
		}
	elif (method == "new"):
		
		price = float(soup.find("span", class_="price-val").text.replace(" ",""))
		currency = str(soup.find("span", class_="price-cur").text)
		lat = float(soup.find(id="item_map").get("data-lat"))
		lon = float(soup.find(id="item_map").get("data-lng"))	

		# Filler in case there is no table on page
		category = 			"N/A"		
		repaired = 			"N/A"
		district = 			"N/A"
		area = 				"N/A"
		outer_area = 		"N/A"
		rooms = 			"N/A"
		floor_actual = 		"N/A"
		floor_max = 		"N/A"
		dateScraped = 		datetime.datetime.now(pytz.timezone("Asia/Baku")) - datetime.timedelta(days=1)
		datePosted = 		"N/A"

		for i in soup.find("div", class_="product-properties").find_all("div", class_="product-properties__i"):
			name = i.find("label", class_="product-properties__i-name").text
			value = i.find("span", class_="product-properties__i-value").text
			if name == "Kateqoriya":
				category = value

			elif name == "Təmir":
				if value == "var":
					repaired = True
				else:
					repaired = False

			elif name == "Sahə":
				if value.split(" ")[1] == "sot":
					area 		= "N/A"				
					outer_area 	= float(value.split(" ")[0])				
				elif value.split(" ")[1] == "m²":
					area 		= float(value.split(" ")[0])				
			
			elif name == "Torpaq sahəsi":
				if outer_area == "N/A":
					outer_area = float(value.split(" ")[0])

			elif name == "Otaq sayı":
				rooms = int(value)

			elif name == "Mərtəbə":
				floor_actual 	= int(value.split("/")[0])
				floor_max		= int(value.split("/")[0])

		# District
		c = soup.find("ul", class_="product-extras")
		for z in c.find_all("li"):
				if z.text[-2:] == "r.":
					district = z.text[:-2].strip()
					break
				else:
					district = "N/A"
		
		# Date Posted
		time_soup = soup.find("div", class_="product-statistics").find("span", class_="product-statistics__i-text").text.split(" ")[2]

		# time_soup = soup.find("div", class_="item_info").find_all("p")

		hour = time_soup.split(":")[0]
		minute = time_soup.split(":")[1]
		datePosted = datetime.datetime.now(pytz.timezone("Asia/Baku")).replace(hour=int(hour), minute=int(minute)) - datetime.timedelta(days=1)
		
		del soup
		return {
			'price': 				price,
			'currency': 			currency,
			'lat': 					lat,
			'lon': 					lon,
			'repaired': 			repaired,
			'district': 			district,
			'category': 			category,
			'area': 				area,
			'outer_area':			outer_area,
			'rooms': 				rooms,
			'floor_actual': 		floor_actual,
			'floor_max': 			floor_max,
			'date_scraped':			dateScraped,
			'date_posted':			datePosted
		}
	else:
		return "N/A"