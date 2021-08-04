#!/usr/bin/env python3

# Funtions for visualization general messages
# -*- coding: utf-8 -*-

# %%%%%%%%%%% Libraries %%%%%%%%%%%#
import json

from colorama import Fore
from colorama import Style

# %%%%%%% Context Variables %%%%%%%#

SEPARATOR = "[*] {0} [*]".format('-' * 110)

# %%%%%%%%%%% Functions %%%%%%%%%%%#


def wrongs(op, messages=''):
    print(Fore.RED + Style.BRIGHT + SEPARATOR)
    if op == 1:
        print(Fore.RED + Style.BRIGHT + '[*] Selection is wrong. Try Again.')
    elif op == 2:
        print(Fore.RED + Style.BRIGHT + '[*] Archive isn\'t recognized '
                                        'as a known library.')
    elif op == 3:
        print(Fore.RED + Style.BRIGHT + '[*] Library ' + messages
              + ' don\'t exist.')
    elif op == 4:
        print(Fore.RED + Style.BRIGHT + '[*] Library ' + messages
              + ' is empty.')
    elif op == 5:
        print(Fore.RED + Style.BRIGHT +
              '[*] Creation of the directory ' + messages + 'failed')
    elif op == 6:
        print(Fore.RED + Style.BRIGHT + '[*] Thanks and coming soon.')
    elif op == 7:
        print(Fore.RED + Style.BRIGHT + '[*] Download ' + messages +
              ' has failed')
    elif op == 8:
        print(Fore.RED + Style.BRIGHT + '[*] Download ' + messages +
              ' is corrupted')
    elif op == 9:
        print(Fore.RED + Style.BRIGHT +
              "[*]\t\t\tAppInspector analysis on " + messages)
        print(Fore.RED + Style.BRIGHT +
              "[*]\tThis is an external dependency, you can find this"
              " project on this link: https://github.com/microsoft/App"
              "licationInspector")
    elif op == 10:
        print(Fore.RED + Style.BRIGHT +
              "[*]\t\t\tNot implemented yet " + messages)
    print(Fore.RED + Style.BRIGHT + SEPARATOR)


def tittles(op, messages=''):
    print('\n')
    print(Fore.GREEN + Style.BRIGHT + SEPARATOR)
    if op == 1:
        print(Fore.GREEN + Style.BRIGHT + "[!] Select from the menu:")
    elif op == 2:
        print(Fore.GREEN + Style.BRIGHT + '[*]\t\t\tLibrary : ' + messages)
    elif op == 3:
        print(Fore.GREEN + Style.BRIGHT +
              "[*]\t\t\tMetadata found in " + messages)
    elif op == 4:
        print(Fore.GREEN + Style.BRIGHT +
              "[*]\t\t\tHash SHA-256 of  " + messages)
    elif op == 5:
        print(Fore.GREEN + Style.BRIGHT +
              "[*]\t\t\tCollected Data in " + messages)
    elif op == 6:
        print(Fore.GREEN + Style.BRIGHT +
              "[*]\t\t\tAnalysis Dangerous or "
              "Obsoletes Functions found in " + messages)
    elif op == 7:
        print(Fore.GREEN + Style.BRIGHT +
              "[*]\t\t\tAdvisories CVEs associated on " + messages)
    elif op == 8:
        print(Fore.GREEN + Style.BRIGHT +
              "[*]\t\t\tAppInspector analysis on " + messages)
        print(Fore.GREEN + Style.BRIGHT +
              "[*]\tThis is an external dependency, you can find this"
              " project on this link: https://github.com/microsoft/"
              "ApplicationInspector")
    elif op == 9:
        print(Fore.GREEN + Style.BRIGHT +
              "[*]\t\t\tTyposquatting combinations found " + messages)
    elif op == 10:
        print(Fore.GREEN + Style.BRIGHT +
              "[*]\t\t\tPackage DNA WebReport " + messages)
    elif op == 11:
        print(Fore.GREEN + Style.BRIGHT +
              "[*]\t\t\tPackages made by the developers of " + messages)
    print(Fore.GREEN + Style.BRIGHT + SEPARATOR)


def subtittles(op, messages):
    if op == 1:
        print(Fore.GREEN + Style.BRIGHT + "[*]\t\tURLs in " + messages)
    elif op == 2:
        print(Fore.GREEN + Style.BRIGHT + "[*]\t\tHASHs in " + messages)
    elif op == 3:
        print(Fore.GREEN + Style.BRIGHT + "[*]\t\tIPs in " + messages)
    elif op == 4:
        print(Fore.GREEN + Style.BRIGHT + "[*]\t\te-mails in " + messages)
    elif op == 5:
        print(Fore.GREEN + Style.BRIGHT + "[*]\t\tResult of " + messages)

    print(Fore.GREEN + Style.BRIGHT + SEPARATOR)


def hashes_differences(package, hash_reported, hash_calculated):
    print('\n')
    print(Fore.GREEN + Style.BRIGHT + SEPARATOR)
    print(Fore.YELLOW + Style.BRIGHT + "[*] Hash reported differs from"
                                       " calculated [*]")
    print(Fore.YELLOW + Style.BRIGHT + f"[*] On package: {package} [*]")
    print(Fore.YELLOW + Style.BRIGHT + f"[*] Hash "
                                       f"reported: {hash_reported} [*]")
    print(Fore.YELLOW + Style.BRIGHT + f"[*] Hash "
                                       f"calculated: {hash_calculated} [*]")
    print(Fore.YELLOW + Style.BRIGHT + "[*]\n")


def code_extract_print(result):
    for r in result:
        try:
            r = json.loads(r)
            if r:
                print('\n')
                print(Fore.GREEN + Style.BRIGHT + SEPARATOR)
                print(Fore.GREEN + Style.BRIGHT + f"[*] Package: {r['name']}")
                print(Fore.GREEN + Style.BRIGHT + f"[*] File: {r['filename']}")
                print(Fore.GREEN + Style.BRIGHT +
                      f'Code extract:\n\t{r["code_extract"]}\n\n')
                print(Fore.GREEN + Style.BRIGHT + "[*]\n")
        except:
            pass


def rate_limit_exceeded(url):
    print('\n')
    print(Fore.YELLOW + Style.BRIGHT + SEPARATOR)
    print(Fore.YELLOW + Style.BRIGHT + f"Rate limit exceeded in {url} trying to gather metadata about the authors."
                                       f"\nIf this data is needed try again later.")
    print(Fore.YELLOW + Style.BRIGHT + "[*]\n")
