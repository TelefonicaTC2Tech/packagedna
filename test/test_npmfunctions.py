#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import tarfile
import unittest

from analyzers.hashfiles import get_hash_pkg
from auxiliar_functions.globals import tests
from auxiliar_functions.globals import url_npm
from auxiliar_functions.globals import npm_pkgs

from npm_analyzers.npmdev import npm_dev
from npm_analyzers.npmuser import npm_user
from npm_analyzers.npmdownjs import npm_download
from npm_analyzers.npmlibrary import npm_library
from npm_analyzers.npmmetadata import npm_metadata


class TestNpmFunctions(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.path_pack = ''
        self.pack_name = ''
        self.pack = ''
        self.username = ''
        self.metadata_found = ''
        self.library = {
            '12env': {
                '1.0.0': ['https://registry.npmjs.org/12env/-/12env-1.0.0.tgz',
                          'd919dae01bc2ad56cd026e77c702bb32530b6982'],
                '1.0.1': ['https://registry.npmjs.org/12env/-/12env-1.0.1.tgz',
                          '5294dd1a7109fcc03b2bc7fbf463e512fa440cf8']}}

    def test_npm_library(self):
        result = json.dumps(self.library)
        url = url_npm + '12env'
        libraries = {}
        self.assertEqual(npm_library(url, libraries), result)

    def test_npm_download(self):
        path = npm_pkgs + os.sep
        result = f'["{path}12env-1.0.0.tgz", "{path}12env-1.0.1.tgz"]'
        libraries = self.library
        self.assertEqual(npm_download(libraries), result)

    def test_npm_metadata(self):
        path_pack = tests + os.sep + '12env-1.0.1.tgz'
        pack_name = '12env'
        result = '{"pkg_hashid": "a4af0d98c97883e6573257e24602de077e3557' \
                 '35775681165682910196bd740b", "name": "12env", "path_pack"' \
                 ': "' + path_pack + \
                 '", "author": "Kent Primrose", "author_email": ' \
                 '"KPrimrose@TheOpenWay.com", "version": "1.0.1",' \
                 ' "date": "2015-05-15", "license": "MIT",' \
                 ' "home_page": "http://github.com/kentprimrose/12env"}'

        with tarfile.open(path_pack) as files:
            package_hash = get_hash_pkg(path_pack)
            npm_metadata_rta = npm_metadata(
                path_pack, package_hash, files, pack_name)
            self.assertEqual(npm_metadata_rta, result)

    def test_npm_user(self):
        username = 'kszucs'
        result = '{"username": "kszucs", ' \
                 '"name": "Krisztian Szucs", ' \
                 '"yours_repositories": ' \
                 '{"@apache-arrow/es5-cjs": {"language": "NPM", ' \
                 '"url": "https://www.npmjs.com/package/@apache-arrow/' \
                 'es5-cjs"}, "@apache-arrow/es5-esm": {"language": "NPM", ' \
                 '"url": "https://www.npmjs.com/package/@apache-arrow' \
                 '/es5-esm"}, "@apache-arrow/es5-umd": {"language": "NPM", ' \
                 '"url": "https://www.npmjs.com/package/@apache-arrow/' \
                 'es5-umd"}, "@apache-arrow/es2015-cjs": {"language": "NPM' \
                 '", "url": "https://www.npmjs.com/package/@apache-arrow' \
                 '/es2015-cjs"}, "@apache-arrow/es2015-esm": {"language":' \
                 ' "NPM", "url": "https://www.npmjs.com/package/@apache-a' \
                 'rrow/es2015-esm"}, "@apache-arrow/es2015-umd": {"languag' \
                 'e": "NPM", "url": "https://www.npmjs.com/package/@apache' \
                 '-arrow/es2015-umd"}, "@apache-arrow/esnext-cjs": {"langu' \
                 'age": "NPM", "url": "https://www.npmjs.com/package/@apac' \
                 'he-arrow/esnext-cjs"}, "@apache-arrow/esnext-esm": {"lan' \
                 'guage": "NPM", "url": "https://www.npmjs.com/package/@ap' \
                 'ache-arrow/esnext-esm"}, "@apache-arrow/esnext-umd": {"l' \
                 'anguage": "NPM", "url": "https://www.npmjs.com/package/@' \
                 'apache-arrow/esnext-umd"}, "apache-arrow": {"language": ' \
                 '"NPM", "url": "https://www.npmjs.com/package/apache-arro' \
                 'w"}, "@apache-arrow/ts": {"language": "NPM", "url": "htt' \
                 'ps://www.npmjs.com/package/@apache-arrow/ts"}}}'

        self.assertEqual(npm_user(username), result)

    def test_npm_dev(self):
        pack = list(self.library.keys())[0]
        result = '{"0": {"username": "krose", ' \
                 '"name": "<UNREGISTERED>", ' \
                 '"yours_repositories": ' \
                 '{"12env": {"language": "NPM", ' \
                 '"url": "https://www.npmjs.com/package/12env"}}}}'

        self.assertEqual(npm_dev(pack), result)


if __name__ == "__main__":
    unittest.main()

# %%%%%%%%%% The End %%%%%%%%%%#
