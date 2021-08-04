import os
import abc
import json
import logging

from time import sleep
from colorama import Fore
from colorama import Style

from auxiliar_functions.messages import wrongs
from py_analyzers.pylibrary import py_library
from rb_analyzers.rblibrary import rb_library
from npm_analyzers.npmlibrary import npm_library

from flask_server.run_server import run_server

from auxiliar_functions.globals import url_py
from auxiliar_functions.globals import url_rb
from auxiliar_functions.globals import url_npm

from analysis_pipeline.npm_pipeline import NpmProcessPipeline
from analysis_pipeline.ruby_pipeline import RubyProcessPipeline
from analysis_pipeline.python_pipeline import PythonProcessPipeline

from menu_classes.single_library_menu import SingleLibraryMenu

from auxiliar_functions.auxiliar_functions import selection_wrong
from auxiliar_functions.auxiliar_functions import not_implemented_yet


class ListLibrariesMenu(SingleLibraryMenu):

    def manage_choice(self):
        if int(self.choice) == 1:
            packages_parser = PythonPackagesParser(last_menu=self)
        elif int(self.choice) == 2:
            packages_parser = GenericPackagesParser(
                last_menu=self, lang='ruby')
        elif int(self.choice) == 3:
            packages_parser = PythonPackagesParser(last_menu=self)
            not_implemented_yet()
            self.generate_menu()
        elif int(self.choice) == 4:
            packages_parser = JavaScriptPackagesParser(last_menu=self)

        try:
            packages_parser.input_packages_list()
        except FileNotFoundError:
            print(f'Invalid path, try again...')
            sleep(.5)
            packages_parser.input_packages_list()

        packages_parser.parse_list()
        packages_parser.start_process()


class PackagesParser(abc.ABC, SingleLibraryMenu):

    def __init__(self, last_menu):
        SingleLibraryMenu.__init__(self, last_menu=last_menu)
        self.packages_list = []

    @abc.abstractmethod
    def parse_list(self, list_packages_path):
        pass

    def input_packages_list(self, message="[!] Insert packages list path: "):
        packages_path = input(Fore.CYAN + Style.NORMAL + message +
                              Style.RESET_ALL)
        if os.path.isfile(packages_path):
            self.packages_path = packages_path
        else:
            raise FileNotFoundError

    @abc.abstractmethod
    def get_libraries(self):
        pass

    @abc.abstractmethod
    def get_process_pipeline(self):
        pass

    @abc.abstractmethod
    def get_url(self):
        pass

    def start_process(self):
        for package in self.packages_list:
            name = package[0]
            try:
                version = package[1]
            except:
                version = None
            try:
                url = self.get_url() + name
                library_rta = json.loads(self.get_libraries()(url, {}, version))
                if self.__error_library(library_rta, name):
                    continue
                process_pipeline = self.get_process_pipeline()(
                    library_rta, package_input_name=name)
                process_pipeline.start_process_pipeline()
                process_pipeline.print_process_pipeline()
            except Exception as e:
                msg = f'\n\nError unexpected package: {name}\n'
                print(msg)
                print(f'Error unexpected: {e}')
                logging.error(msg)
                logging.error(e, exc_info=True)
        self.select_package()

    def select_package(self):

        self.generate_menu([package[0] for package in self.packages_list])

        name = self.packages_list[int(self.choice) - 1][0]
        try:
            run_server(name)
        except:
            self.select_package()

    def get_choice(self):
        choice = input(Fore.CYAN + Style.NORMAL +
                       "[!] Enter your selection: " + Style.RESET_ALL)
        try:
            if self.input_validation(choice, items=self.packages_list):
                self.choice = choice
            else:
                selection_wrong()
                self.select_package()
        except ValueError:
            selection_wrong()
            self.select_package()

    def __error_library(self, libraries, pack):
        if len(libraries.keys()) == 0:
            wrongs(4, pack)
            return True
            # self.generate_menu()
        elif 'error' in list(libraries.keys()):
            wrongs(3, pack)
            # self.generate_menu()
            return True


class GenericPackagesParser(PackagesParser):

    def __init__(self, last_menu, lang):
        PackagesParser.__init__(self, last_menu=last_menu)
        self.lang = lang

    def parse_list(self):
        packages_list = self.packages_to_parse
        packages_list = packages_list.replace(' ', '')
        packages_list = packages_list.split(',')
        packages_list = [package.split('==') for package in packages_list]
        self.packages_list = packages_list

    def input_packages_list(self, message="[!] Insert packages list "
                                          "separated by comma (,)\nExample "
                                          "packageA==0.1, packageB==1.7,"
                                          " packageC "):
        packages_list = input(Fore.CYAN + Style.NORMAL +
                              message + Style.RESET_ALL)
        self.packages_to_parse = packages_list


    def get_libraries(self):
        if self.lang == 'ruby':
            return rb_library

    def get_process_pipeline(self):
        if self.lang == 'ruby':
            return RubyProcessPipeline

    def get_url(self):
        if self.lang == 'ruby':
            return url_rb + '/'


class PythonPackagesParser(PackagesParser):

    def parse_list(self):
        packages_list = open(self.packages_path, 'r').read()
        packages_list = packages_list.split('\n')
        packages_list = [package.split('==') for package in packages_list]
        self.packages_list = packages_list

    def get_libraries(self):
        return py_library

    def get_process_pipeline(self):
        return PythonProcessPipeline

    def get_url(self):
        return url_py


class JavaScriptPackagesParser(PackagesParser):

    def parse_list(self):
        with open(self.packages_path, 'r') as file:
            packages_list = json.loads(file.read())
        packages_list = packages_list['dependencies']
        for item in packages_list.items():
            name = item[0]
            version = item[1].replace('^', '')
            self.packages_list.append([name, version])

    def get_libraries(self):
        return npm_library

    def get_process_pipeline(self):
        return NpmProcessPipeline

    def get_url(self):
        return url_npm


