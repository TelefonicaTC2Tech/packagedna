#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from io import StringIO
from unittest.mock import patch
from menu_classes.menu import Menu
from auxiliar_functions.globals import menu_start
from auxiliar_functions.auxiliar_functions import input_pack
from console_prints.console_prints import print_library


class TestPackageDNA(unittest.TestCase, Menu):
    maxDiff = None

    def setUp(self):
        self.libraries = {}

    def test_input_pack(self):
        libraries = {}
        result_py = ['mock', 'https://pypi.org/simple/mock', libraries]
        result_rb = ['m', 'https://rubygems.org/gems/m', libraries]
        with patch('builtins.input', return_value='mock'):
            pack = input_pack('py')
        self.assertListEqual(pack, result_py)

        with patch('builtins.input', return_value='m'):
            pack = input_pack('rb')
        self.assertListEqual(pack, result_rb)

    def test_print_library(self):
        libraries = {
            'aosman-foo': {
                'aosman-foo-0.2.tar.gz':
                    ['https://files.pythonhosted.org/packages/8e/20/e7245d'
                     '694615a1ec16bab48b975ce89350bf53cab508ec0b77a230c656d9/'
                     'aosman_foo-0.2.tar.gz',
                     'fa3d29807c7d3857d6d039f3dc3440e52276741de04732be14c09'
                     'eae210f0cb6']}}
        result = "\n\n\x1b[32m\x1b[1m[*] --------------------------------" \
                 "-------------------------------------------------------" \
                 "----------------------- [*]" \
                 "\n\x1b[32m\x1b[1m[*]			Library : aosman-foo" \
                 "\n\x1b[32m\x1b[1m[*] -----------------------------------" \
                 "--------------------------------------------------------" \
                 "------------------- [*]" \
                 "\n[*]" \
                 "\n[*]	aosman-foo-0.2.tar.gz:" \
                 "\n[*]		URL   : https://files.pythonhosted.org/packages" \
                 "/8e/20/e7245d694615a1ec16bab48b975ce89350bf53cab508ec0b77" \
                 "a230c656d9/aosman_foo-0.2.tar.gz" \
                 "\n[*]		SHA256: fa3d29807c7d3857d6d039f3dc3440e52276741" \
                 "de04732be14c09eae210f0cb6\n"

        with patch('sys.stdout', new=StringIO()) as library_out:
            print_library(libraries)
            self.assertEqual(library_out.getvalue(), result)

    @patch('builtins.input', return_value='7')
    def test_generate_menu(self, choice):
        i = 0
        if i != 0:
            i += 1
            self.list_items = menu_start
            self.back_enable = False
            result = "\n\x1b[32m\x1b[1m[*] ------------------------------" \
                     "---------------------------------------------------" \
                     "----------------------------- [*]"\
                     "\n\x1b[32m\x1b[1m[*] Selection is wrong. Try Again." \
                     "\n\x1b[32m\x1b[1m[*] ------------------------------" \
                     "---------------------------------------------------" \
                     "----------------------------- [*]\n"
            with patch('sys.stdout', new=StringIO()) as select_out:
                Menu.generate_menu(self)
                self.assertEqual(select_out.getvalue(), result)


if __name__ == "__main__":
    unittest.main()

# %%%%%%%%%% The End %%%%%%%%%%#
