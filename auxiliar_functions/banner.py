from colorama import Fore
from colorama import Style


def banner():
    b = """
_____              _                          ____     __     _  _______ 
|  __ \            | |                        |  __ \  |   \  | ||  ___  |
| |__) |__ __ ____ | | __   __ __  ____   ___ | |  \ \ | |\ \ | || |___| |
|  ___// _` |/  __)| |/ /  / _` | / _  | / _ \| |   | || | \ \| ||  ___  |
| |   | (_| || (__ | |\ \ | (_| || (_| ||  __/| |__/ / | |  \   || |   | |
|_|    \__,_|\____)|_| \_\ \__,_| \__  | \___||_____/  |_|   \__||_|   |_|
                                   __| |
                                  (____|

Modular Packages Analyzer Framework
By ElevenPaths https://www.elevenpaths.com/
Usage: python3 ./packagedna.py
"""
    print(Fore.GREEN + Style.BRIGHT + b)
