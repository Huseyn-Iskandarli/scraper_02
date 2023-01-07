import datetime
current_time = datetime.datetime.now()
with open("test.txt", "a") as file:
    file.write("\nHello World " + str(current_time))