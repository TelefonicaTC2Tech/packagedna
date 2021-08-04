#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import unittest

from zipfile import ZipFile

from auxiliar_functions.globals import tests
from auxiliar_functions.globals import url_py
from auxiliar_functions.globals import pypi_pkgs

from py_analyzers.pydev import py_dev
from py_analyzers.pyuser import py_user
from py_analyzers.pylibrary import py_library
from py_analyzers.pymetadata import py_metadata
from py_analyzers.pydownpackage import py_download
from py_analyzers.pydangerousfunctions import py_dangerous_functions

from analyzers.hashfiles import get_hash_pkg


class TestPyFunctions(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.result = ''
        self.result_true = ''
        self.result_false = ''
        self.pack = ''
        self.path_pack = ''
        self.username = ''
        self.url = ''
        self.metadata_found = ''
        self.library = {
            'aosman-foo': {
                'aosman-foo-0.1.tar.gz':
                    ['https://files.pythonhosted.org/packages/d6/9d/'
                     '078e611b79374f01eae5d775829db3be943d51ed32792961'
                     '3745b22f0b57/'
                     'aosman_foo-0.1.tar.gz',
                     '6468938400e6510f68f461f4dfcec76fd7abcde8c606b0113'
                     '870f93437be2f8d'],
                'aosman-foo-0.2.tar.gz':
                    ['https://files.pythonhosted.org/packages/8e/20/'
                     'e7245d694615a1ec16bab48b975ce89350bf53cab508ec0b7'
                     '7a230c656d9/'
                     'aosman_foo-0.2.tar.gz',
                     'fa3d29807c7d3857d6d039f3dc3440e52276741de04732be1'
                     '4c09eae210f0cb6'
                     ]
                }
           }

    def test_py_download(self):
        path = pypi_pkgs + os.sep
        result = f'["{path}aosman_foo-0.1.tar.gz",' \
                 f' "{path}aosman_foo-0.2.tar.gz"]'

        libraries = self.library
        py_download_rta = py_download(libraries)
        self.assertEqual(py_download_rta, result)

    def test_py_library(self):
        result = '{"0": {"0.0.0": ["https://' \
                 'files.pythonhosted.org/packages/8c/e6/' \
                 '83748ba1e232167de61f2bf31ec53f4b7acdd1ced52bdf3ea3366ea' \
                 '48132/0-0.0.0-py2.py3-none-any.whl", "d8c8aeb13d410f713ea1' \
                 '32d4268ef3dc1e113be6ec3ef2c31420df5c44e8e634"]}}'

        url = url_py + '0'
        libraries = {}
        py_library_rta = py_library(url, libraries)
        self.assertEqual(py_library_rta, result)

    def test_py_metadata(self):
        pack = 'diario'
        path_pack = tests + os.sep + 'diario-0.1.9-py3-none-any.whl'
        result_true = '{"pkg_hashid": "74dd449282c5dc5708a32d2112f404506b76' \
                      '0fc0eb39eb4c07a34e307856ee90", "name": "diario", ' \
                      '"path_pack": "' + path_pack + \
                      '", "author": "ElevenPaths", "author_email": ' \
                      '"innovationlab@11paths.com", "version": "2.1", ' \
                      '"date": "2019-12-10", "license":' \
                      ' "<UNREGISTERED>", "home_page": ' \
                      '"https://diario.e-paths.com/index.html"}'

        result_false = '{"pkg_hashid": "74dd449282c5dc5708a32d2112f404506b' \
                       '760fc0eb39eb4c07a34e307856ee90", "name": "diario",' \
                       ' "path_pack": "' + path_pack +\
                       '", "author": "ElevenPaths", "author_email": ' \
                       '"innovationlab@11paths.com", "version": "0.1.9", ' \
                       '"date": "2019-12-10T16:45:10", "license": ' \
                       '"<UNREGISTERED>", "home_page": ' \
                       '"https://diario.e-paths.com/index.html"}'

        with ZipFile(path_pack, 'r') as files:
            package_hash = get_hash_pkg(path_pack)
            py_metadata_rta = py_metadata(
                path_pack, files, pack, package_hash, False)
            self.assertEqual(py_metadata_rta, result_false)

    def test_py_dangerous_functions(self):
        path_pack = tests + os.sep + 'sick11paths-0.1-py3-none-any.whl'
        result = '{"pkg_hashid": "322edbfd7b4c87bed2178d304a35da824f7c48' \
                 '15cc13aab71a7e53d6ef23606f", "file": "-/sick11paths/' \
                 '11paths-py", "dangerous_functions": ["[*] Ln: 3, Col:' \
                 ' 40  --   E999 SyntaxError: invalid syntax"]}'

        with ZipFile(path_pack, 'r') as files:
            package_hash = get_hash_pkg(path_pack)
            py_dangerous_functions_rta = py_dangerous_functions(
                path_pack, files, package_hash)
            self.assertEqual(py_dangerous_functions_rta, result)

    def test_py_user(self):
        username = 'deibit'
        result = '{"username": "deibit", ' \
                 '"name": "David", "yours_repositories": {' \
                 '"diario": {"language": "Python", ' \
                 '"url": "https://pypi.org/project/diario"}}}'

        self.assertEqual(py_user(username), result)

    def test_py_dev(self):
        pack = 'diario'
        result = '{"0": {"username": "deibit", ' \
                 '"name": "David", "yours_repositories": ' \
                 '{"diario": {"language": "Python", ' \
                 '"url": "https://pypi.org/project/diario"}}}}'
        self.assertEqual(py_dev(pack), result)


if __name__ == "__main__":
    unittest.main()

# %%%%%%%%%% The End %%%%%%%%%%#
