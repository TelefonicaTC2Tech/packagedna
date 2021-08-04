import os

from flask_server.run_server import run_server
from menu_classes.single_library_menu import SingleLibraryMenu
from auxiliar_functions.globals import flask_server_data_folder
from auxiliar_functions.auxiliar_functions import clear_terminal


class PreviouslyAnalyzedPackages(SingleLibraryMenu):

    def manage_choice(self):
        if int(self.choice) == 1:
            previously_python = PreviouslyAnalyzedPackage(self, 'python')
            previously_python.select_package()
        elif int(self.choice) == 2:
            previously_python = PreviouslyAnalyzedPackage(self, 'ruby')
            previously_python.select_package()
        elif int(self.choice) == 3:
            previously_python = PreviouslyAnalyzedPackage(self, 'go')
            previously_python.select_package()
        elif int(self.choice) == 4:
            previously_python = PreviouslyAnalyzedPackage(self, 'npm')
            previously_python.select_package()
        else:
            pass


class PreviouslyAnalyzedPackage(SingleLibraryMenu):

    def __init__(self, last_menu, language):
        SingleLibraryMenu.__init__(self, last_menu)
        self.language = language

    def select_package(self):
        self.packages_list = os.listdir(flask_server_data_folder + os.sep + self.language + os.sep)
        self.list_items = self.packages_list
        if self.packages_list:
            self.generate_menu([package for package in self.packages_list])
            self.manage_choice()
        else:
            print('yikes')

    def manage_choice(self):
        name = self.packages_list[int(self.choice) - 1]
        try:
            os.environ['PACKAGE_LANGUAGE'] = self.language
            run_server(name)
        except Exception:
            self.manage_choice()