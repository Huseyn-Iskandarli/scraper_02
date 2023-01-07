import time
x = 0
while True:
    x +=1
    with open("test.txt", "a") as file:
        file.write(str(x) + "\n")
    time.sleep(3)