import sys

from colorama import Fore, Style
from tqdm import tqdm
from console_prints.console_prints import print_username
from external_analyzers.users.user_bitbucket import user_bitbucker
from external_analyzers.users.user_github import user_github
from menu_classes.menu import Menu
from npm_analyzers.npmuser import npm_user
from py_analyzers.pyuser import py_user
from rb_analyzers.rbuser import rb_user


class UserMenu(Menu):

    back_enable = True

    def __init__(self, last_menu):
        Menu.__init__(self, last_menu)


    def start_analysis(self, username=None):
        if not username:
            username = input(Fore.CYAN + Style.NORMAL + "[!] Enter the username: " + Style.RESET_ALL)

        pbar = tqdm(total=5, desc=' Starting user analysis...')
        py_rta = py_user(username)
        pbar.update(1)
        rb_rta = rb_user(username)
        pbar.update(1)
        npm_rta = npm_user(username)
        pbar.update(1)
        github_rta = user_github(username)
        pbar.update(1)
        bitbuckets_rta = user_bitbucker(username)
        pbar.update(1)
        pbar.close()

        print_username(py_rta, 'Python')
        print_username(rb_rta, 'Ruby')
        print_username(npm_rta, 'Npm')
        print_username(github_rta, 'Github')
        print_username(bitbuckets_rta, 'Bitbuckets')

        sys.exit()

