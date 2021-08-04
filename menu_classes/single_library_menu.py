import json

from analysis_pipeline.go_pipeline import GoProcessPipeline
from go_analyzers.golibrary import go_library
from menu_classes.menu import Menu
from py_analyzers.pylibrary import py_library
from rb_analyzers.rblibrary import rb_library
from go_analyzers.golibrary import go_library
from flask_server.run_server import run_server
from npm_analyzers.npmlibrary import npm_library

from analysis_pipeline.go_pipeline import GoProcessPipeline
from analysis_pipeline.npm_pipeline import NpmProcessPipeline
from analysis_pipeline.ruby_pipeline import RubyProcessPipeline
from analysis_pipeline.python_pipeline import PythonProcessPipeline

from auxiliar_functions.globals import menu_libraries
from auxiliar_functions.messages import wrongs
from auxiliar_functions.messages import code_extract_print
from auxiliar_functions.auxiliar_functions import input_pack
from auxiliar_functions.auxiliar_functions import end_execution
from auxiliar_functions.auxiliar_functions import input_code_extract
from auxiliar_functions.auxiliar_functions import not_implemented_yet


class SingleLibraryMenu(Menu):
    list_items = menu_libraries
    back_enable = True

    def __init__(self, last_menu, last_version=False):
        Menu.__init__(self, last_menu)
        self.last_version = last_version

    def manage_choice(self):
        if int(self.choice) == 1:
            self.get_python_package(last_version=self.last_version)
        elif int(self.choice) == 2:
            self.get_ruby_gem(last_version=self.last_version)
        elif int(self.choice) == 3:
            self.get_go_package(last_version=self.last_version)
        elif int(self.choice) == 4:
            self.get_npm_package(last_version=self.last_version)
        else:
            pass

    def start_pipeline(self):
        self.process_pipeline.start_process_pipeline()
        self.process_pipeline.print_process_pipeline()
        run_server(self.package_name)

    def get_python_package(self, last_version=False, package_name=None):
        data = input_pack(lang='py', package_name=package_name)
        self.package_name = data[0]
        libraries = json.loads(py_library(data[1], data[2]))
        self.__error_library(libraries, self.package_name)
        if last_version:
            libraries = {
                self.package_name: {
                    list(libraries[self.package_name].keys())[-1]: libraries[self.package_name]
                    [list(libraries[self.package_name].keys())[-1]]
                }
            }
        self.process_pipeline = PythonProcessPipeline(
            libraries, package_input_name=self.package_name)

    def get_ruby_gem(self, last_version=False, package_name=None):
        data = input_pack(lang='rb', package_name=package_name)
        self.package_name = data[0]
        libraries = json.loads(rb_library(data[1], data[2]))
        self.__error_library(libraries, self.package_name)
        if last_version:
            libraries = {
                self.package_name: {
                    list(libraries[self.package_name]
                         .keys())[0]: libraries[self.package_name]
                                               [list(libraries[
                                                         self.package_name]
                                                .keys())[0]]
                         }
                        }
        self.process_pipeline = RubyProcessPipeline(
            libraries, package_input_name=self.package_name)

    def get_go_package(self, last_version=False, package_name=None):
        data = input_pack(lang='go', package_name=package_name)
        self.package_name = data[0]
        libraries = json.loads(go_library(data[1], data[2]))
        self.__error_library(libraries, self.package_name)
        if last_version:
            libraries = {
                self.package_name: {
                    list(libraries[self.package_name]
                         .keys())[0]: libraries[self.package_name]
                                               [list(libraries[
                                                         self.package_name]
                                                .keys())[0]]
                         }
                        }
        self.process_pipeline = GoProcessPipeline(libraries, package_input_name=self.package_name)

    def get_npm_package(self, last_version=False, package_name=None):
        data = input_pack(lang='npm', package_name=package_name)
        self.package_name = data[0]
        libraries = json.loads(npm_library(data[1], data[2]))
        self.__error_library(libraries, self.package_name)
        if last_version:
            libraries = {
                self.package_name: {
                    list(libraries[self.package_name].keys())[-1]: libraries[
                        self.package_name]
                    [list(libraries[self.package_name].keys())[-1]]
                }
            }
        self.process_pipeline = NpmProcessPipeline(
            libraries, package_input_name=self.package_name)

    def __error_library(self, libraries, pack):
        if len(libraries.keys()) == 0:
            wrongs(4, pack)
            self.generate_menu()
        elif 'error' in list(libraries.keys()):
            wrongs(3, pack)
            self.generate_menu()

    def code_analysis(self):
        code_extract = input_code_extract(
            message='Insert input code extract: ')

        result = self.process_pipeline.get_code_analysis(code_extract)
        code_extract_print(result)
        end_execution()
