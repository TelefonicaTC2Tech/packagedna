import sys

from menu_classes.menu import Menu
from menu_classes.single_library_menu import SingleLibraryMenu
from menu_classes.user_menu import UserMenu
from auxiliar_functions.auxiliar_functions import clear_terminal
from auxiliar_functions.globals import menu_information_gathering
from menu_classes.typo_squatting_library_menu import TypoSquattingLibraryMenu


class InfoGatheringMenu(Menu):
    list_items = menu_information_gathering
    back_enable = True

    def __init__(self, last_menu):
        Menu.__init__(self, last_menu)

    def manage_choice(self):
        clear_terminal()
        if int(self.choice) == 1:
            user_menu = UserMenu(last_menu=self)
            user_menu.start_analysis()
        elif int(self.choice) == 2:
            typo_squatting_menu = TypoSquattingLibraryMenu(last_menu=self)
            typo_squatting_menu.generate_menu()
        elif int(self.choice) == 3:
            one_library_all_versions = SingleLibraryMenu(last_menu=self)
            one_library_all_versions.generate_menu()
            one_library_all_versions.code_analysis()
            sys.exit(1)
        else:
            pass