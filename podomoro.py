import time
import threading

flag = 1
j = 10


def counting():
    global j
    while j > 0:
        time.sleep(1)
        j = j - 1
        if flag == 1:
            print(str(int(j / 60))+":"+str(j % 60), end='\r')
        else:
            print("Paused at:"+str(int(j / 60))+":"+str(j % 60), end='\r')
            while flag == 0:
                continue


def inputer():
    global flag
    x = input(">")
    if x == "pause":
        flag = 0
        print("Enter con")
        if input("") == 'con':
            flag = 1


timer = threading.Thread(target=counting, daemon=True)
status = threading.Thread(target=inputer, daemon=True)
timer.start()
status.start()
while True:
    if j == 0:
        break
print("You've done it, Child. I'm truly proud.")
