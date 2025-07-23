from time import sleep
import os
from getch import getch
from timedinput import timedinput

def dprint(string:str):
    n = 0
    for char in string:
        print(char, end='', flush=True)
        skip = timedinput("", timeout=0.02, default="continue")
        n += 1
        print(f"\033[1A\033[{n}C", end='')
        if skip == "":
            print(f"\r{string}", end='', flush=True)
            break
        sleep(0.01)
    print()

def space_to_continue():
    print("\nPress space to continue")
    opt = getch()
    while opt != " ":
        print("\033[K\033[F")
        opt = getch()
    os.system("clear")

def list_select(lst, msg):
    pages = [lst[i:i + 9] for i in range(0, len(lst), 9)]
    currentPage = 0

    for number, element in enumerate(pages[currentPage]):
        print(f"{number+1}:", element.name.capitalize())  
    print(f"\nPage {currentPage+1}/{len(pages)}")

    print(msg)

    num = getch()
    while True:
        if num == " ":
            break
        if num == "a":
            currentPage -= 1
            if currentPage < 0:
                currentPage = 0
        elif num == "d":
            currentPage += 1
            if currentPage > len(pages)-1:
                currentPage = len(pages)-1
        try:
            num = int(num)
            if num in range(len(pages[currentPage])+1):
                break
        except:
            pass
        os.system("clear")
        for number, element in enumerate(pages[currentPage]):
            print(f"{number+1}:", element.name.capitalize())
        print(f"\nPage {currentPage+1}/{len(pages)}")
        print(msg)  
        num = getch()

    if num != " ":
        return (pages[currentPage][num-1], num+(9*currentPage)-1)
    else:
        return " ", "  "