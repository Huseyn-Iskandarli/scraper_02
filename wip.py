# import datetime
# current_time = datetime.datetime.now()
# with open("test.txt", "a") as file:
#     file.write("\nHello World " + str(current_time))


# z = [1,2,3,"w",4,5,6]

# for i in z:
#     try:
#         print(i+1)
#     except:
#         print("error")
#         continue

# text = "abc"
# print(text)
# text = True
# print(text)

from middleware import request_page as rp
z = rp.requestSample("https://bina.az/yasayis-kompleksleri/215")

x = z.find("div")
print(x)
# print(z.find_all("div", class_="someshit"))

# for i in z.find_all("div", class_="something_random"):
#     print(i)