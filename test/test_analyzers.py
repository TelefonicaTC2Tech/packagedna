#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import unittest
import tarfile

from zipfile import ZipFile

from analyzers.cve_git import cve_git
from analyzers.cve_git import comp_versions
from analyzers.hashfiles import hash_files
from analyzers.hashfiles import get_hash_pkg
from analyzers.datafiles import extract_data
from analyzers.typosquatting import typos_create
from auxiliar_functions.globals import tests


class TestPackageDNA(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.path_pack = ''
        self.packname = ''

    def test_hash_files(self):
        path_pack = tests + os.sep + 'sick11paths-0.1-py3-none-any.whl'
        result = '{"pkg_hashid": "322edbfd7b4c87bed2178d304a35da824f7c4' \
                 '815cc13aab71a7e53d6ef23606f", "sick11paths-0-1-dist-info' \
                 '/LICENSE": "ddc345af19d6e297dd85fbba7c9d52286ee516c7e2bf' \
                 'cf0b9eabea8a2a373f9a", "sick11paths-0-1-dist-info/' \
                 'METADATA": "6f2b8f4c413628a3db55ecbdef2d020f86e9648195' \
                 '3a5290f99fa82a2cb4059c", "sick11paths-0-1-dist-info/' \
                 'RECORD": "4469f072ef167b0e2fcf7922d6769ef4470507129638f' \
                 '788cc42b3158634bb72", "sick11paths-0-1-dist-info/WHEEL":' \
                 ' "a78ebfe54873ab3e80cde4a8b223a7c4afb39858dad62db60ab402' \
                 '8e661ef1e7", "sick11paths-0-1-dist-info/entry_points-txt' \
                 '": "97d90b3ed7e972cae58ec282510e61e2465ecf8c6862fbbf329d8' \
                 '7695255fdbf", "sick11paths-0-1-dist-info/top_level-txt":' \
                 ' "9dac3dd23a3c3120d9d8eca01e0f85306cda25788ac2f4adfdd90' \
                 '9597dafc278", "sick11paths/11paths-py": "abf0fc7aed97505' \
                 '02a5804c43aec77db9c0fdfb863331df9172ca89008d30b6c", ' \
                 '"sick11paths/libs/DNSLibrary-dll": "47abb5497ad4e2004fc6' \
                 '7136a3fd8e731d738a3291fbcf47b1b0d5677eb606b1", "' \
                 'sick11paths/libs/eicar-com": "275a021bbfb6489e54d471899' \
                 'f7db9d1663fc695ec2fe2a2c4538aabf651fd0f", "sick11paths/' \
                 'script-py": "2e971e5fa8848abd3b49e93b3096aa00ca1e69d74a' \
                 'b1a96a78fd31a8d2185814", "sick11paths/stack-py": "1bbb10' \
                 '54a4419414a0fc463c04f2f618a2d0d5ec0c4e24bb4e675b618bea5e4d"}'

        with ZipFile(path_pack, 'r') as files:
            package_hash = get_hash_pkg(path_pack)
            hash_files_rta = hash_files(path_pack, package_hash, files)
            self.assertEqual(hash_files_rta, result)

    def test_extract_data(self):
        path_pack = tests + os.sep + 'PyIF-0.1.tar.gz'
        result = '{"pkg_hashid": "f52fff3f78a4deeec64775d51a01c470791c48d5' \
                 '02572804c7591718ce6ea301", "name": "' + path_pack +\
                 '", "urls": ["https://github.com/lcdm-uiuc/PyTE"], ' \
                 '"hashs": [], "ips": [], "emails": ["bigdog@illinois.edu",' \
                 ' "ikegwu2@illinois.edu", "jtt2@illinois.edu"]}'

        with tarfile.open(path_pack, 'r:gz') as files:
            package_hash = get_hash_pkg(path_pack)
            extract_rta = extract_data(path_pack, files, package_hash)
            self.assertEqual(extract_rta, result)

    def test_typos_create(self):
        packname = 'electron'
        result = ['-1electron', '-addselectron', '-docselectron', '-electron',
                  '-extraselectron', '-inlineelectron', '-js-liteelectron',
                  '-pluselectron', '-py3electron', '-pyelectron',
                  '-python3electron', '-pythonelectron', '-rbelectron',
                  '-rubyelectron', '.rbelectron', '3electron', '3lectron',
                  '4electron', '4lectron', '_1electron', '_liteelectron',
                  '_py3electron', '_pyelectron', '_python3electron',
                  '_pythonelectron', '_rbelectron', '_rubyelectron',
                  'delectron', 'dlectron', 'e-lectron', 'e3lectron',
                  'e4lectron', 'edlectron', 'eectron', 'eelctron', 'eelectron',
                  'eflectron', 'ekectron', 'eklectron', 'el-cron', 'el-ectron',
                  'el3ctron', 'el3ectron', 'el4ctron', 'el4ectron', 'elcetron',
                  'elctron', 'eldctron', 'eldectron', 'ele-ctron']
        self.assertListEqual(typos_create(packname, 'npm')[:50], result)

    def test_cve_git(self):
        packname = 'pillow'
        library = 'pip'
        version = '8.1.2'
        result = '{"8.1.2": {"CVE-2021-28676": {"name": "Potential infinite ' \
                 'loop ", "date": "2021-06-08", "severity": "high severity",' \
                 ' "affected": [["lt; 8.2.0"]], "url": "https://github.com/' \
                 'advisories/GHSA-7r7m-5h27-29hp"}, "CVE-2021-25287": {' \
                 '"name": "Out-of-bounds Read", "date": "2021-06-08", ' \
                 '"severity": "critical severity", "affected": [["gt;= ' \
                 '2.4.0", "&lt; 8.2.0"]], "url": "https://github.com/' \
                 'advisories/GHSA-77gc-v2xv-rvvh"}, "CVE-2021-28675": {' \
                 '"name": "Denial of service", "date": "2021-06-08", ' \
                 '"severity": "moderate severity", "affected": [["lt; ' \
                 '8.2.0"]], "url": "https://github.com/advisories/' \
                 'GHSA-g6rj-rv7j-xwp4"}, "CVE-2021-28678": {"name": ' \
                 '"Uncontrolled Resource Consumption", "date": "2021-06-08",' \
                 ' "severity": "moderate severity", "affected": [["gt;= ' \
                 '5.1.0", "&lt; 8.2.0"]], "url": "https://github.com/' \
                 'advisories/GHSA-hjfx-8p6c-g7gx"}, "CVE-2021-25288": {' \
                 '"name": "Out-of-bounds Read", "date": "2021-06-08", ' \
                 '"severity": "critical severity", "affected": [["gt;= ' \
                 '2.4.0", "&lt; 8.2.0"]], "url": "https://github.com/' \
                 'advisories/GHSA-rwv7-3v45-hg29"}, "CVE-2021-28677": {' \
                 '"name": "Uncontrolled Resource Consumption", "date": ' \
                 '"2021-06-08", "severity": "high severity", "affected": ' \
                 '[["lt; 8.2.0"]], "url": "https://github.com/advisories/' \
                 'GHSA-q5hq-fp76-qmrc"}}}'

        self.assertEqual(cve_git(packname, library, version), result)

    def test_comp_versions(self):
        cve_affect = [
             ["lt; 3.2.22.3"],
             ["gt; 4.0.0", "&lt; 4.2.7.1"],
             ["gt;= 5.0.0", "&lt;= 5.0.0.1"]]
        self.assertTrue(comp_versions(cve_affect, '5.0.0'))


if __name__ == "__main__":
    unittest.main()
