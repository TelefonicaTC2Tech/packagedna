from colorama import Fore
from colorama import Style
from auxiliar_functions.messages import tittles
from auxiliar_functions.globals import SEPARATOR
from auxiliar_functions.auxiliar_functions import end_execution
from auxiliar_functions.auxiliar_functions import clear_terminal
from auxiliar_functions.auxiliar_functions import selection_wrong


class Menu:
    """
        This is a menu class
    """
    back_enable = False

    def __init__(self, last_menu=None):
        self.last_menu = last_menu

    def input_validation(self, choice, items=None):
        items = items if items else self.list_items
        # Reg to match any of the numbers given by number of items in the list
        list_range = list(range(1, len(items) + 1))
        input_reg = f'{"|".join(str(x) for x in list_range)}'

        # If the input is an X it ends the execution
        # If the input is a B it return to the last menu
        if choice.upper() == 'X':
            end_execution()
        elif choice.upper() == 'B':
            self.__back_last_menu()
        elif choice in input_reg:
            return True
        else:
            return False

    def __back_last_menu(self):
        if self.last_menu is None:
            pass
        else:
            clear_terminal()
            self.last_menu.generate_menu()

    def generate_menu(self, list_items=None):
        items = list_items if list_items else self.list_items

        tittles(1)
        for idx, item in enumerate(items):
            if isinstance(item, list):
                try:
                    if item[1] == 'GREEN':
                        print(Fore.GREEN + Style.BRIGHT +
                              f'\t[{idx+1}] ' + item[0] + ': ' + item[2])
                    else:
                        print(Fore.RED + Style.BRIGHT + f'\t[{idx+1}] '
                              + item[0])
                except IndexError:
                    print(Fore.GREEN + Style.BRIGHT + f'\t[{idx+1}] '
                          + item[0])
            else:
                print(Fore.GREEN + Style.BRIGHT + f'\t[{idx+1}] ' + item)
        if self.back_enable:
            print(Fore.GREEN + Style.BRIGHT + '\t' + '[B] Back')
        print(Fore.GREEN + Style.BRIGHT + '\t' + '[X] Exit')
        print(Fore.GREEN + Style.BRIGHT + SEPARATOR)
        self.get_choice()

    def get_choice(self):
        choice = input(Fore.CYAN + Style.NORMAL + "[!] Enter your selection: "
                       + Style.RESET_ALL)

        try:
            if self.input_validation(choice):
                self.choice = choice
                self.manage_choice()
            else:
                selection_wrong()
                self.generate_menu()
        except ValueError:
            selection_wrong()
            self.generate_menu()

    def manage_choice(self):
        pass
