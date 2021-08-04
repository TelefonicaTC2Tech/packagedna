import json
from colorama import Fore
from colorama import Style
from menu_classes.menu import Menu
from auxiliar_functions.globals import menu_configurations


class ConfigurationsMenu(Menu):
    back_enable = True

    def __init__(self, last_menu):
        Menu.__init__(self, last_menu=last_menu)

    def _get_file_configurations(self):
        self.list_items = []
        with open("configurations.json") as json_data_file:
            self.config_data = json.load(json_data_file)

        for key in menu_configurations:
            if self.config_data[key]:
                self.list_items.append([menu_configurations[key],
                                        'GREEN',
                                        self.config_data[key]])
            else:
                self.list_items.append([menu_configurations[key], 'RED'])

    def generate_menu(self):
        self._get_file_configurations()
        super(ConfigurationsMenu, self).generate_menu()

    def manage_choice(self):
        value = input(Fore.CYAN + Style.NORMAL +
                      f"Insert {self.list_items[int(self.choice)-1][0]}: " +
                      Style.RESET_ALL)
        key = list(self.config_data.keys())[int(self.choice)-1]
        self.config_data[key] = value
        with open("configurations.json", "w") as outfile:
            json.dump(self.config_data, outfile)
        self.generate_menu()
