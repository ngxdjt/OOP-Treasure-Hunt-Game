from time import sleep
import os
from getch import getch
from timedinput import timedinput
from termcolor import colored
import shutil

def dprint(string:str, cIndex:list=[], colour:str=''):
    n = 0
    textWrapped = False
    for i, char in enumerate(string):
        if char != " " and not textWrapped:
            if i in cIndex:
                print(colored(char, colour), end='', flush=True)
            else:
                print(char, end='', flush=True)
        skip = timedinput("", timeout=0.02, default="continue")
        if n > shutil.get_terminal_size().columns - 3:
            print()
            n = -1
            textWrapped = True
        if char == "\n":
            n = -1
            textWrapped = True
        if not textWrapped:
            print(f"\033[1A\033[{n+1}C", end='')
        else:
            print(f"\033[1A", end='')
        textWrapped = False
        n += 1
        textWrapped = False
        if skip == "":
            print("\r" + ''.join(colored(char, colour) if i in cIndex else char for i, char in enumerate(string)))
            print("\033[K\033[A", end='')
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
    
if __name__ == "__main__":
    dprint("1234567890 " * 10 + "\nNow we test the new line too.", cIndex=[5, 25, 40], colour='cyan')