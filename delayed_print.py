from time import sleep

def dprint(string:str):
    for char in string:
        print(char, end='', flush=True)
        sleep(0.05)
    print()