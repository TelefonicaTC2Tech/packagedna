import re
from pathlib import Path

from menu_classes.menu import Menu
from flask_server.run_server import run_server

from menu_classes.inf_gathering import InfoGatheringMenu
from menu_classes.single_library_menu import SingleLibraryMenu
from menu_classes.list_libraries_menu import ListLibrariesMenu
from menu_classes.configurations_menu import ConfigurationsMenu
from menu_classes.previously_analyzed_packages import \
    PreviouslyAnalyzedPackages

from analysis_pipeline.npm_pipeline import NpmProcessPipeline
from analysis_pipeline.ruby_pipeline import RubyProcessPipeline
from analysis_pipeline.python_pipeline import PythonProcessPipeline

from auxiliar_functions.globals import menu_start
from auxiliar_functions.messages import wrongs
from auxiliar_functions.auxiliar_functions import input_pack
from auxiliar_functions.auxiliar_functions import clear_terminal


class MainMenu(Menu):
    list_items = menu_start
    back_enable = False

    def manage_choice(self):
        clear_terminal()
        if int(self.choice) == 1:
            one_library_last_version = SingleLibraryMenu(last_menu=self,
                                                         last_version=True)
            one_library_last_version.generate_menu()
            one_library_last_version.start_pipeline()
        elif int(self.choice) == 2:
            one_library_all_versions = SingleLibraryMenu(last_menu=self)
            one_library_all_versions.generate_menu()
            one_library_all_versions.start_pipeline()
        elif int(self.choice) == 3:
            try:
                path_pack = input_pack(
                    message='[!] Digit local path of the package ')[0]
                package_input_name = Path(path_pack).resolve().stem.split('-')[0]
            except ValueError:
                wrongs(2)
                self.generate_menu()
            if re.search(".whl$", path_pack) or \
                    re.search(".tar.gz$", path_pack) or \
                    re.search(".egg$", path_pack):
                py_process = PythonProcessPipeline(
                    path_pack, local=True,
                    package_input_name=package_input_name)
                py_process.start_process_pipeline()
                py_process.print_process_pipeline()
            elif re.search(".gem$", path_pack):
                rb_process = RubyProcessPipeline(
                    path_pack, local=True,
                    package_input_name=package_input_name)
                rb_process.start_process_pipeline()
                rb_process.print_process_pipeline()
            elif re.search(".tgz$", path_pack):
                npm_process = NpmProcessPipeline(
                    path_pack, local=True,
                    package_input_name=package_input_name)
                npm_process.start_process_pipeline()
                npm_process.print_process_pipeline()
            else:
                wrongs(2, path_pack)
            run_server(package_input_name)
        elif int(self.choice) == 4:
            info_gathering_menu = InfoGatheringMenu(last_menu=self)
            info_gathering_menu.generate_menu()
        elif int(self.choice) == 5:
            list_libraries_menu = ListLibrariesMenu(last_menu=self)
            list_libraries_menu.generate_menu()
        elif int(self.choice) == 6:
            previously_analyzed_packages = PreviouslyAnalyzedPackages(
                last_menu=self)
            previously_analyzed_packages.generate_menu()
            previously_analyzed_packages.select_package()
        elif int(self.choice) == 7:
            configurations_menu = ConfigurationsMenu(last_menu=self)
            configurations_menu.generate_menu()
