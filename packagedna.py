#!/usr/bin/env python3

"""
------------------------------------------------------------------------------
PackageDNA - diciembre 2019 - Carlos Avila @badboy_nt
                            - Diego Espitia @dsespitia
                            - Franco Piergallini @francoguida
------------------------------------------------------------------------------
"""

# %%%%%%%%%%% Libraries %%%%%%%%%%%#


import os
import sys
import click
import logging
import colorama
import subprocess
from flask_server.run_server import run_server
from menu_classes.main_menu import MainMenu
from auxiliar_functions.banner import banner
from auxiliar_functions.auxiliar_functions import create_dir
from auxiliar_functions.auxiliar_functions import end_execution

# %%%%%%% Context Variables %%%%%%%#
from menu_classes.single_library_menu import SingleLibraryMenu
from menu_classes.user_menu import UserMenu

VERSION = 0.1
LOG_ERRORS_FILENAME = 'log_errors.txt'
logging.basicConfig(filename=LOG_ERRORS_FILENAME, filemode='a+')

# %%%%%%%%%% Main %%%%%%%%%#


@click.group()
def cli():
    pass


@click.group(help='Packages related commands')
def packages():
    """Function generated for use the command line"""
    pass


@click.group(help='Users related commands')
def users():
    """Function generated for use the command line"""
    pass


cli.add_command(packages)
cli.add_command(users)


@users.command()
@click.option('--user_name', help='Analyze a username over platforms')
def analyze_user(user_name):
    UserMenu(None).start_analysis(user_name)


@packages.command()
@click.option('--package_name', help='Analyze a python package all versions')
def analyze_python_package(package_name):
    SingleLibraryMenu(None).get_python_package(package_name=package_name)
    run_server(package_name)


@packages.command()
@click.option('--package_name', help='Analyze a ruby package all versions')
def analyze_ruby_package(package_name):
    SingleLibraryMenu(None).get_ruby_gem(package_name=package_name)
    run_server(package_name)


@packages.command()
@click.option('--package_name', help='Analyze a npm package all versions')
def analyze_npm_package(package_name):
    SingleLibraryMenu(None).get_npm_package(package_name=package_name)
    run_server(package_name)


@packages.command(help='List analyzed packages')
def list_packages():
    packages = os.listdir('flask_server/static/data')
    click.secho('Analyzed packages:\n\t' + "\n\t".join(packages), fg='green')


@packages.command(help='Run analyzed package')
@click.option('--package_name', help='Name of an analized package')
def run_package(package_name):
    if os.path.isfile(f'flask_server/static/data/{package_name}'):
        run_server(package_name)
    else:
        click.secho('Package not found', fg='red')


packages.add_command(analyze_python_package)
packages.add_command(analyze_ruby_package)
packages.add_command(analyze_npm_package)
packages.add_command(list_packages)
packages.add_command(run_package)
users.add_command(analyze_user)


def main():

    if len(sys.argv) > 1:
        cli()
    else:
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
            colorama.init(autoreset="True")
            create_dir()
            main_menu = MainMenu()
            banner()
            main_menu.generate_menu()
        except KeyboardInterrupt:
            end_execution()
        except Exception as e:
            print(f'Error unexpected: {e}')
            print('Something went very wrong ...' + u"\U0001F62D"*3)
            logging.error(e, exc_info=True)
            print(f'Please send the file {LOG_ERRORS_FILENAME}'
                  f' to innovationlab@11paths.com')


if __name__ == '__main__':
    main()

# %%%%%%%%%% The End %%%%%%%%%%
