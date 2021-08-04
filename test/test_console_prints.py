#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from io import StringIO
from unittest.mock import patch

from console_prints.console_prints import print_library
from console_prints.console_prints import print_metadata_json
from console_prints.console_prints import print_user_dev_json
from console_prints.console_prints import print_hashfiles_json
from console_prints.console_prints import print_extract_data_json


class TestPackageDNA(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.stdout = 'sys.stdout'
        self.result = ''
        self.package_input_name = 'diario'
        self.libraries = {
            'diario':
                {'0.2.0': ['https://files.pythonhosted.org/packages/02/'
                           'c2/e80150377d7605f36065335c445692f8f96ce2d4053ff'
                           'ac9568e065bf931/diario-0.2.0-py3-none-any.whl',
                           'ec5e35a3f2b5c7bb6a9360b738aa7e4d712673480d282a8f'
                           '499aaec50e63a3c8']}}

    def test_print_library(self):
        result = '\n\n\x1b[32m\x1b[1m[*] ----------------------------------' \
                 '--------------------------------------------------------' \
                 '-------------------- [*]' \
                 '\n\x1b[32m\x1b[1m[*]			Library : diario' \
                 '\n\x1b[32m\x1b[1m[*] -------------------------------------' \
                 '--------------------------------------------------------' \
                 '----------------- [*]' \
                 '\n[*]' \
                 '\n[*]\t0.2.0:' \
                 '\n[*]\t\tURL   : https://files.pythonhos' \
                 'ted.org/packages/02/c2/e80150377d7605f36065335c445692f8f' \
                 '96ce2d4053ffac9568e065bf931/diario-0.2.0-py3-none-any.whl' \
                 '\n[*]\t\tSHA256: ec5e35a3f2b5c7bb6a9360b7' \
                 '38aa7e4d712673480d282a8f499aaec50e63a3c8\n'

        with patch(self.stdout, new=StringIO()) as library_out:
            print_library(self.libraries)
            self.assertEqual(library_out.getvalue(), result)

    def test_print_metadata_json(self):
        metadata_json = ['{"pkg_hashid": "ec5e35a3f2b5c7bb6a9360b738aa7e4d'
                         '712673480d282a8f499aaec50e63a3c8", "name": "diario"'
                         ', "path_pack": "/home/dsespitia/Scripts/python/pac'
                         'kagedna/downloads/pypi_pkgs/diario-0.2.0-py3-none-'
                         'any.whl", "author": "ElevenPaths", "author_email":'
                         ' "innovationlab@11paths.com", "version": "0.2.0",'
                         ' "date": "2020-05-13", "license": "<UNREGISTERED>",'
                         ' "home_page": "https://diario.elevenpaths.com"}']

        result = '\n\n\x1b[32m\x1b[1m[*] --------------------------------' \
                 '-------------------------------------------------------' \
                 '----------------------- [*]' \
                 '\n\x1b[32m\x1b[1m[*]			Metadata found in diario' \
                 '\n\x1b[32m\x1b[1m[*] ----------------------------------' \
                 '--------------------------------------------------------' \
                 '-------------------- [*]' \
                 '\n[*]\t Name: diario' \
                 '\n[*]\t Author: ElevenPaths' \
                 '\n[*]\t Author Email: innovationlab@11paths.com' \
                 '\n[*]\t Version: 0.2.0' \
                 '\n[*]\t Date: 2020-05-13' \
                 '\n[*]\t License: <UNREGISTERED>' \
                 '\n[*]\t Home Page: https://diario.elevenpaths.com' \
                 '\n[*]\n\n'

        with patch(self.stdout, new=StringIO()) as metadata_out:
            print_metadata_json(metadata_json, self.package_input_name)
            self.assertEqual(metadata_out.getvalue(), result)

    def test_hashfiles_json(self):
        hashfiles_json = ['{"pkg_hashid": "ec5e35a3f2b5c7bb6a9360b738aa7e4'
                          'd712673480d282a8f499aaec50e63a3c8", "diario/__'
                          'init__-py": "a5f03523c41c150abbc50ba7c40b64302263'
                          'a4bb7c9fc54cb69fc6600af61c0d", "diario/admin-py":'
                          ' "c93a8aabf4b76c52a209bd5e8b7e9a6190a609001ec2156'
                          '72872dc412abebf7e", "diario-0-2-0-dist-info/LICEN'
                          'SE": "afda1e604fa2a862cbc0fc70ad1eddced569e83302bf'
                          '3d93c49f3d732e14ebdc", "diario-0-2-0-dist-info/MET'
                          'ADATA": "d416f1181aaeee9d51187dd2681ec8ac056d14597'
                          '98037620703313725f18548", "diario-0-2-0-dist-info/'
                          'WHEEL": "53cf04846230f128f6fe986a6a37aefc4022dd1028'
                          'f3e0bacd5dd112c59b59bb", "diario-0-2-0-dist-info/t'
                          'op_level-txt": "4b63a8d16e3e5ef5b8ff40660f6ae62200'
                          'ac732a8e54cd9ec0f8727af5deb94f", "diario-0-2-0-dis'
                          't-info/RECORD": "69fa742c779d2eee43356bf54b3c64e5'
                          '3525c2316a5dd6b09a5992cd18b9737b"}']

        result = '\n\n\x1b[32m\x1b[1m[*] -----------------------------------' \
                 '----------------------------------------------------------' \
                 '----------------- [*]' \
                 '\n\x1b[32m\x1b[1m[*]\t\t\tHash SHA-256 of  diario' \
                 '\n\x1b[32m\x1b[1m[*] ------------------------------------' \
                 '---------------------------------------------------------' \
                 '----------------- [*]' \
                 '\n[*] SHA256 - diario/__init__-py: a5f03523c41c150abbc50ba' \
                 '7c40b64302263a4bb7c9fc54cb69fc6600af61c0d' \
                 '\n[*] SHA256 - diario/admin-py: c93a8aabf4b76c52a209bd5e8b' \
                 '7e9a6190a609001ec215672872dc412abebf7e' \
                 '\n[*] SHA256 - diario-0-2-0-dist-info/LICENSE: afda1e604fa' \
                 '2a862cbc0fc70ad1eddced569e83302bf3d93c49f3d732e14ebdc' \
                 '\n[*] SHA256 - diario-0-2-0-dist-info/METADATA: d416f1181' \
                 'aaeee9d51187dd2681ec8ac056d1459798037620703313725f18548' \
                 '\n[*] SHA256 - diario-0-2-0-dist-info/WHEEL: 53cf04846230' \
                 'f128f6fe986a6a37aefc4022dd1028f3e0bacd5dd112c59b59bb' \
                 '\n[*] SHA256 - diario-0-2-0-dist-info/top_level-txt: 4b63' \
                 'a8d16e3e5ef5b8ff40660f6ae62200ac732a8e54cd9ec0f8727af5de' \
                 'b94f' \
                 '\n[*] SHA256 - diario-0-2-0-dist-info/RECORD: 69fa742c779d' \
                 '2eee43356bf54b3c64e53525c2316a5dd6b09a5992cd18b9737b\n'

        with patch(self.stdout, new=StringIO()) as hashfiles_out:
            print_hashfiles_json(hashfiles_json, self.package_input_name)
            self.assertEqual(hashfiles_out.getvalue(), result)

    def test_print_extract_data_json(self):
        extract_data_json = ['{"pkg_hashid": "ec5e35a3f2b5c7bb6a9360b738aa'
                             '7e4d712673480d282a8f499aaec50e63a3c8", "name":'
                             ' "/packagedna/downloads/pypi_pkgs/diario-0.2.0'
                             '-py3-none-any.whl", "urls": ["https://diario.e'
                             'levenpaths.com/dashboard/apispecification/index"'
                             ', "https://pypi.python.org/pypi/diario", "https'
                             '://diario.elevenpaths.com", "https://img.shield'
                             's.io/pypi/v/diario.svg"], "hashs": ["23203f9264'
                             '161714cdb8d2f474b9b641e6a735f8cea4098c40a3cab87'
                             '439d749"], "ips": [], "emails": ["innovationlab'
                             '@11paths.com"]}']
        result = '\n\n\x1b[32m\x1b[1m[*] ----------------------------------' \
                 '---------------------------------------------------------' \
                 '------------------- [*]' \
                 '\n\x1b[32m\x1b[1m[*]\t\t\tCollected Data in diario' \
                 '\n\x1b[32m\x1b[1m[*] ------------------------------------' \
                 '---------------------------------------------------------' \
                 '----------------- [*]' \
                 '\n\x1b[32m\x1b[1m[*]\t\tURLs in /packagedna/downloads/pyp' \
                 'i_pkgs/diario-0.2.0-py3-none-any.whl' \
                 '\n\x1b[32m\x1b[1m[*] -----------------------------------' \
                 '---------------------------------------------------------' \
                 '------------------ [*]' \
                 '\n[*]	https://diario.elevenpaths.com/dashboard/apispecifi' \
                 'cation/index' \
                 '\n[*]	https://pypi.python.org/pypi/diario' \
                 '\n[*]	https://diario.elevenpaths.com' \
                 '\n[*]	https://img.shields.io/pypi/v/diario.svg\n[*]\n' \
                 '\n\x1b[32m\x1b[1m[*]\t\tHASHs in /packagedna/downloads/' \
                 'pypi_pkgs/diario-0.2.0-py3-none-any.whl' \
                 '\n\x1b[32m\x1b[1m[*] ------------------------------------' \
                 '--------------------------------------------------------' \
                 '------------------ [*]' \
                 '\n[*]	23203f9264161714cdb8d2f474b9b641e6a735f8cea4098' \
                 'c40a3cab87439d749\n[*]\n' \
                 '\n\x1b[32m\x1b[1m[*]\t\te-mails in /packagedna/downloads' \
                 '/pypi_pkgs/diario-0.2.0-py3-none-any.whl' \
                 '\n\x1b[32m\x1b[1m[*] -------------------------------------' \
                 '----------------------------------------------------------' \
                 '--------------- [*]' \
                 '\n[*]	innovationlab@11paths.com\n[*]\n\n'

        with patch(self.stdout, new=StringIO()) as extract_data_out:
            print_extract_data_json(extract_data_json, self.package_input_name)
            self.assertEqual(extract_data_out.getvalue(), result)

    def test_print_user_dev_json(self):
        user_dev_json = ['{"0": {"username": "deibit", "name": "David", '
                         '"yours_repositories": {"diario": {"language": '
                         '"Python", "url": "https://pypi.org/project/'
                         'diario"}}}}']
        result = '\n\n\x1b[32m\x1b[1m[*] ---------------------------------' \
                 '--------------------------------------------------------' \
                 '--------------------- [*]' \
                 '\n\x1b[32m\x1b[1m[*]			Packages made by the de' \
                 'velopers of diario' \
                 '\n\x1b[32m\x1b[1m[*] ---------------------------' \
                 '--------------------------------------------------------' \
                 '--------------------------- [*]' \
                 '\n\x1b[32m\x1b[1m[*]\t\tUsername: deibit' \
                 '\n\x1b[32m\x1b[1m[*]\t\tName: David' \
                 '\n\x1b[32m\x1b[1m[*]\t\tRepositories:' \
                 '\n\x1b[32m\x1b[1m[*]\t\t\tLanguage: Python' \
                 '\n\x1b[32m\x1b[1m[*]\t\t\t\tUrl: https://pypi.org' \
                 '/project/diario\n[*]\n\n'

        with patch(self.stdout, new=StringIO()) as user_dev_out:
            print_user_dev_json(user_dev_json, self.package_input_name)
            self.assertEqual(user_dev_out.getvalue(), result)


if __name__ == "__main__":
    unittest.main()
