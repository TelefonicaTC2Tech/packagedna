#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import unittest

from auxiliar_functions.globals import url_go
from auxiliar_functions.globals import go_pkgs

from go_analyzers.godev import go_dev
from go_analyzers.golibrary import go_library
from go_analyzers.godownpackage import go_download


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
            "github.com/terra-project/mantle":
                {"v0.3.1": ["https://api.github.com/repos/terra-project/"
                            "mantle/zipball/v0.3.1",
                            "ead2574222ebaf3da262195ccabf3244b336ffe7"],
                 "v0.3.0": ["https://api.github.com/repos/terra-project/"
                            "mantle/zipball/v0.3.0",
                            "b443eed3ad74ec9995d279f51ca38eacbf83cd32"],
                 "v0.3.0-rc.4": ["https://api.github.com/repos/terra-project/"
                                 "mantle/zipball/v0.3.0-rc.4",
                                 "c6407cec4d9cd1f1edd2fd0ae14cfc744348c284"]}}

    def test_go_library(self):
        result = ['{"github.com/goburrow/modbus": '
                  '{"v0.1.0": ["https://api.github.com/repos/goburrow/modbus'
                  '/zipball/refs/tags/v0.1.0", '
                  '"606c02f4eef527a1d4cf7d8733d5fd7ba34f91d8"]}}',
                  '{"dmitri.shuralyov.com/service/change": {}}',
                  '{"dmitri.shuralyov.com/service/change": '
                  '{"v0.0.0-20191123213520-957083f7751c": '
                  '["https://gotools.org/dmitri.shuralyov.com/service/'
                  'change?rev=957083f7751c", ""], '
                  '"v0.0.0-20191123213520-813ec28aab09": '
                  '["https://gotools.org/dmitri.shuralyov.com/service/'
                  'change?rev=813ec28aab09", ""], "v0.0.0-20191102175858-'
                  '011d2fcff0d7": ["https://dmitri.shuralyov.com/service/'
                  'change/...", ""], "v0.0.0-20190811215010-bd27112db59b":'
                  ' ["https://dmitri.shuralyov.com/service/change/...", ""], '
                  '"v0.0.0-20190626024955-a289f548ed13": ["https://dmitri.'
                  'shuralyov.com/service/change/...", ""], "v0.0.0-20190416'
                  '035432-7103ed879ef7": ["https://dmitri.shuralyov.com/'
                  'service/change/...", ""], "v0.0.0-20190416035141-'
                  '59022927fa7d": ["https://dmitri.shuralyov.com/service'
                  '/change/...", ""], "v0.0.0-20190416034845-e8a331073e94": '
                  '["https://dmitri.shuralyov.com/service/change/...", ""], '
                  '"v0.0.0-20190327024903-e9885884f070": ["https://dmitri.'
                  'shuralyov.com/service/change/...", ""], "v0.0.0-20190324'
                  '223045-c30c625107fb": ["https://dmitri.shuralyov.com'
                  '/service/change/...", ""]}}']
        urls = [url_go + 'github.com/goburrow/modbus',
                url_go + 'dmitri.shuralyov.com/service/change']
        libraries = {}
        for url in urls:
            go_library_rta = go_library(url, libraries)
            self.assertEqual(go_library_rta, result[urls.index(url)])
            libraries = {}

    def test_go_download(self):
        path = go_pkgs + os.sep
        result = f'["{path}github.com_-_terra-project_-_mantle_-_v0.3.1", ' \
                 f'"{path}github.com_-_terra-project_-_mantle_-_v0.3.0",' \
                 f' "{path}github.com_-_terra-project_-_mantle_-_v0.3.0-rc.4"]'

        libraries = self.library
        go_download_rta = go_download(libraries)
        self.assertEqual(go_download_rta, result)

    def test_go_dev(self):
        packs = ['github.com/goburrow/modbus', 'cmd/vet/whitelist']
        result = ['{"0": {"username": "andig", "name": "andig", '
                  '"yours_repositories": {"actions": {"language": "Go", '
                  '"url": "https://github.com/andig/actions"}, "AdaPi": '
                  '{"language": "Python", "url": "https://github.com/andig'
                  '/AdaPi"}, "alexa": {"language": "JavaScript", "url": '
                  '"https://github.com/andig/alexa"}, "alpine-php": '
                  '{"language": "Dockerfile", "url": "https://github.com'
                  '/andig/alpine-php"}, "arduino-esp32": {"language": "C",'
                  ' "url": "https://github.com/andig/arduino-esp32"}, '
                  '"AudiAPI": {"language": null, "url": "https://github.com/'
                  'andig/AudiAPI"}, "backup-MyAudi": {"language": null, '
                  '"url": "https://github.com/andig/backup-MyAudi"}, '
                  '"bar": {"language": "Go", "url": "https://github.com/andig'
                  '/bar"}, "beats4pi": {"language": "Shell", "url": '
                  '"https://github.com/andig/beats4pi"}, "blackfriday": '
                  '{"language": "Go", "url": "https://github.com/andig/'
                  'blackfriday"}, "brokenglass": {"language": "Go", "url":'
                  ' "https://github.com/andig/brokenglass"}, "canprogs": '
                  '{"language": "PHP", "url": "https://github.com/andig/'
                  'canprogs"}, "carddav2fb": {"language": "PHP", "url": '
                  '"https://github.com/andig/carddav2fb"}, "Chart.js": {'
                  '"language": "JavaScript", "url": "https://github.com/'
                  'andig/Chart.js"}, "chartjs-plugin-axispadding": '
                  '{"language": "JavaScript", "url": "https://github.com/'
                  'andig/chartjs-plugin-axispadding"}, "dbal": {"language": '
                  '"PHP", "url": "https://github.com/andig/dbal"}, "dbcopy":'
                  ' {"language": "PHP", "url": "https://github.com/andig/'
                  'dbcopy"}, "discovergy": {"language": "PHP", "url": '
                  '"https://github.com/andig/discovergy"}, "dlf": {"language":'
                  ' "PHP", "url": "https://github.com/andig/dlf"}, "docker": '
                  '{"language": "PHP", "url": "https://github.com/andig/'
                  'docker"}, "docker-homebridge": {"language": "Shell", '
                  '"url": "https://github.com/andig/docker-homebridge"}, '
                  '"ebusd-configuration": {"language": "C++", "url": '
                  '"https://github.com/andig/ebusd-configuration"}, '
                  '"ebusd-logging": {"language": null, "url": '
                  '"https://github.com/andig/ebusd-logging"}, "elk-docker": '
                  '{"language": "Shell", "url": "https://github.com/andig/'
                  'elk-docker"}, "evcc": {"language": "Go", "url": '
                  '"https://github.com/andig/evcc"}, "evcc-config": '
                  '{"language": "Go", "url": "https://github.com/andig/'
                  'evcc-config"}, "evcc-hassio-addon": {"language": null,'
                  ' "url": "https://github.com/andig/evcc-hassio-addon"}, '
                  '"Fire2016": {"language": "C++", "url": "https://github.com'
                  '/andig/Fire2016"}, "foo": {"language": "Go", "url": '
                  '"https://github.com/andig/foo"}, "fritzapi": {"language":'
                  ' "JavaScript", "url": "https://github.com/andig/fritzapi"'
                  '}}}}', '{}']

        for pack in packs:
            self.assertEqual(go_dev(pack), result[packs.index(pack)])


if __name__ == "__main__":
    unittest.main()

# %%%%%%%%%% The End %%%%%%%%%%#
