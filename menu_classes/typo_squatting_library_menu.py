from colorama import Fore
from colorama import Style

from analyzers.typosquatting import typo_web
from analyzers.typosquatting import typo_local
from analyzers.typosquatting import typos_create
from analyzers.typosquatting import update_files

from auxiliar_functions.globals import menu_typo

from auxiliar_functions.messages import tittles
from auxiliar_functions.messages import SEPARATOR
from auxiliar_functions.auxiliar_functions import input_pack
from auxiliar_functions.auxiliar_functions import clear_terminal
from auxiliar_functions.auxiliar_functions import selection_wrong

from console_prints.console_prints import print_typosquatting
from menu_classes.single_library_menu import SingleLibraryMenu


class TypoSquattingLibraryMenu(SingleLibraryMenu):

    def manage_choice(self):
        if int(self.choice) == 1:
            typosquatting_run_options = TypoSquattingRunOptions(last_menu=self,
                                                                lenguaje='py')
            typosquatting_run_options.generate_menu()
        elif int(self.choice) == 2:
            typosquatting_run_options = TypoSquattingRunOptions(last_menu=self,
                                                                lenguaje='rb')
            typosquatting_run_options.generate_menu()
        elif int(self.choice) == 3:
            typosquatting_run_options = TypoSquattingRunOptions(last_menu=self,
                                                                lenguaje='go')
            typosquatting_run_options.generate_menu()
        elif int(self.choice) == 4:
            typosquatting_run_options = TypoSquattingRunOptions(last_menu=self,
                                                                lenguaje='npm')
            typosquatting_run_options.generate_menu()


class TypoSquattingRunOptions(SingleLibraryMenu):
    list_items = menu_typo

    def __init__(self, last_menu, lenguaje):
        SingleLibraryMenu.__init__(self, last_menu=last_menu)
        self.__lenguaje = lenguaje
        clear_terminal()

    def manage_choice(self):

        if int(self.choice) == 1:
            data = input_pack(self.__lenguaje)
            typo_combinations = typos_create(data[0], self.__lenguaje)
            typo_download_results = typo_local(self.__lenguaje,
                                               typo_combinations)
        elif int(self.choice) == 2:
            data = input_pack(self.__lenguaje)
            typo_combinations = typos_create(data[0], self.__lenguaje)
            update_files(self.__lenguaje)
            typo_download_results = typo_local(self.__lenguaje,
                                               typo_combinations)
        elif int(self.choice) == 3:
            data = input_pack(self.__lenguaje)
            typo_combinations = typos_create(data[0], self.__lenguaje)
            typo_download_results = typo_web(self.__lenguaje,
                                             typo_combinations)
        else:
            selection_wrong()

        print_typosquatting(typo_download_results, data[0])

    def typo_options(self):
        clear_terminal()
        tittles(1)
        options = enumerate(menu_typo, 1)
        for c, i in options:
            print(Fore.GREEN + Style.BRIGHT + '\t[' + str(c) + '] ' + i)

        print(Fore.GREEN + Style.BRIGHT + SEPARATOR)
        choice = input(
            Fore.CYAN + Style.NORMAL + "[!] Enter your selection: "
            + Style.RESET_ALL)
        return choice
