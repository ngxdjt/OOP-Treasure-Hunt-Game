from time import sleep
import os
from getch import getch

def dprint(string:str):
    for char in string:
        print(char, end='', flush=True)
        sleep(0.03)
    print()

def space_to_continue():
    print("\nPress space to continue")
    opt = getch()
    while opt != " ":
        print("\033[K\033[F")
        opt = getch()
    os.system("clear")