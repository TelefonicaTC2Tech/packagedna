#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import os
import tarfile
from analyzers.hashfiles import get_hash_pkg

from rb_analyzers.rbdev import rb_dev
from rb_analyzers.rbuser import rb_user
from rb_analyzers.rblibrary import rb_library
from rb_analyzers.rbmetadata import rb_metadata
from rb_analyzers.rbdowngems import rb_download


from auxiliar_functions.globals import tests
from auxiliar_functions.globals import url_rb
from auxiliar_functions.globals import ruby_pkgs


class TestRbFunctions(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.path_pack = ''
        self.pack_name = ''
        self.packname = ''
        self.username = ''
        self.library = {}

    def test_rb_download(self):
        path = ruby_pkgs + os.sep
        result = f'["{path}bus-o-matic-0.0.7.gem",' \
                 f' "{path}bus-o-matic-0.0.6.gem",' \
                 f' "{path}bus-o-matic-0.0.5.gem",' \
                 f' "{path}bus-o-matic-0.0.4.gem",' \
                 f' "{path}bus-o-matic-0.0.3.gem",' \
                 f' "{path}bus-o-matic-0.0.2.gem",' \
                 f' "{path}bus-o-matic-0.0.1.gem"]'

        libraries = {
            'bus-o-matic': {
                '0.0.7':
                    ['https://rubygems.org/downloads/bus-o-matic-0.0.7.gem',
                     '51cb9b33e1e7acbafd372ad2b94820d01912e27b593adeb5be'
                     '4632ede3222a78'],
                '0.0.6':
                    ['https://rubygems.org/downloads/bus-o-matic-0.0.6.gem',
                     'dce97589dd38f6c66549d8c14f047db969739063f8c265ab0eab9'
                     '103f4102509'],
                '0.0.5':
                    ['https://rubygems.org/downloads/bus-o-matic-0.0.5.gem',
                     'd42cfda3c78a2d8c1dc225f650d8b780c94ce4acf039d2594659'
                     'edbd9b68fc5f'],
                '0.0.4':
                    ['https://rubygems.org/downloads/bus-o-matic-0.0.4.gem',
                     '421735d767150acf3729dc526d6c51d157e9c038296915e02a531'
                     'bedab4fb2e7'],
                '0.0.3':
                    ['https://rubygems.org/downloads/bus-o-matic-0.0.3.gem',
                     '68b642dcd71ff2466431b8d3a977931fb3ad8c235ae58a182fd5'
                     '8e413a4fff9d'],
                '0.0.2':
                    ['https://rubygems.org/downloads/bus-o-matic-0.0.2.gem',
                     '4dee1e69b185bfbd3a41a5f1500a0e09d400d267aee62191dc0d'
                     '3d27d7009dee'],
                '0.0.1':
                    ['https://rubygems.org/downloads/bus-o-matic-0.0.1.gem',
                     '27d983570708de30a70024d1c38228360440aa1dc35a37d7c8d'
                     '035408964e5c9']}}

        rb_download_rta = rb_download(libraries)
        self.assertEqual(rb_download_rta, result)

    def test_rb_metadata(self):
        path_pack = tests + os.sep + 'bus-o-matic-0.0.7.gem'
        pack_name = 'bus-o-matic'
        result_net = '{"pkg_hashid": "51cb9b33e1e7acbafd372ad2b94820d01912' \
                     'e27b593adeb5be4632ede3222a78", "name": "bus-o-matic",' \
                     ' "path_pack": "' + path_pack + \
                     '", "author": "Matt Cone", "author_email": ' \
                     '"<UNREGISTERED>", "version": "0.0.7", "date": ' \
                     '"2015-06-28T00:00:00.000Z", "license": "MIT", ' \
                     '"home_page": "https://rubygems.org/gems/bus-o-matic"}'

        result_local = '{"pkg_hashid": "51cb9b33e1e7acbafd372ad2b94820d0' \
                       '1912e27b593adeb5be4632ede3222a78", "name": ' \
                       '"bus-o-matic", "path_pack": "' + path_pack + \
                       '", "author": "Matt Cone", "author_email": ' \
                       '"matt@macinstruct.com", "version": "0.0.7", ' \
                       '"date": "2015-06-28", "license": "MIT", ' \
                       '"home_page": "https://www.busomatic.com/"}'

        with tarfile.open(path_pack) as files:
            package_hash = get_hash_pkg(path_pack)
            rb_metadata_rta = rb_metadata(path_pack, package_hash, files,
                                          False, pack_name)
            self.assertEqual(rb_metadata_rta, result_net)

    def test_rb_library(self):
        result = '{"wall_e": {"0.1.0": ["https://rubygems.org/downloads/' \
                 'wall_e-0.1.0.gem", "2cbe882170d508c9208eb75aa6b81aed04d' \
                 '991336daed21b39158ff7b24c9481"], "0.0.4": ["https://ruby' \
                 'gems.org/downloads/wall_e-0.0.4.gem", "abf1af087a5c2efd2' \
                 'a06b0f1a402b500230d521b139c3c3f01e13a29ff0bc73a"], "0.0.3' \
                 '": ["https://rubygems.org/downloads/wall_e-0.0.3.gem", ' \
                 '"e4666bcdd27a149e82c5612ee745004562e423f8a0f5ab6e8246b307' \
                 '9bf11a6f"], "0.0.2": ["https://rubygems.org/downloads/' \
                 'wall_e-0.0.2.gem", "d11386fad862f0c7062d7deee86d8e192816' \
                 '0220c84ef9a80c0933b38242ce82"], "0.0.1": ["https://' \
                 'rubygems.org/downloads/wall_e-0.0.1.gem", "86cc84503fdfb9' \
                 '7863abc8ea994b0381da1be8a3b82582c6a91c89b9823b707a"]}}'

        url = url_rb + '/' + 'wall_e'
        libraries = {}
        rb_library_rta = rb_library(url, libraries)
        self.assertEqual(rb_library_rta, result)

    def test_rb_user(self):
        username = 'nu7hatch'
        result = '{"username": "nu7hatch", ' \
                 '"name": "Chris Kowalik", ' \
                 '"yours_repositories": ' \
                 '{"foreman-export-mir": {"language": "Ruby", ' \
                 '"url": "https://rubygems.org/gems/foreman-export-mir"}, ' \
                 '"rosey": {"language": "Ruby", ' \
                 '"url": "https://rubygems.org/gems/rosey"}, ' \
                 '"exoteric": {"language": "Ruby", ' \
                 '"url": "https://rubygems.org/gems/exoteric"}, ' \
                 '"rspec-jasmine": {"language": "Ruby",' \
                 ' "url": "https://rubygems.org/gems/rspec-jasmine"}, ' \
                 '"jagger": {"language": "Ruby", ' \
                 '"url": "https://rubygems.org/gems/jagger"}, ' \
                 '"mike": {"language": "Ruby", ' \
                 '"url": "https://rubygems.org/gems/mike"}, ' \
                 '"mustang": {"language": "Ruby", ' \
                 '"url": "https://rubygems.org/gems/mustang"}, ' \
                 '"redis-aid": {"language": "Ruby", ' \
                 '"url": "https://rubygems.org/gems/redis-aid"}, ' \
                 '"rocket-core": {"language": "Ruby", ' \
                 '"url": "https://rubygems.org/gems/rocket-core"}, ' \
                 '"rocket": {"language": "Ruby", ' \
                 '"url": "https://rubygems.org/gems/rocket"}, ' \
                 '"rocket-js": {"language": "Ruby", ' \
                 '"url": "https://rubygems.org/gems/rocket-js"}, ' \
                 '"rocket-server": {"language": "Ruby", ' \
                 '"url": "https://rubygems.org/gems/rocket-server"}, ' \
                 '"wizard": {"language": "Ruby", ' \
                 '"url": "https://rubygems.org/gems/wizard"}, ' \
                 '"gmail": {"language": "Ruby", ' \
                 '"url": "https://rubygems.org/gems/gmail"}, ' \
                 '"konfigurator": {"language": "Ruby", ' \
                 '"url": "https://rubygems.org/gems/konfigurator"}, ' \
                 '"aclatraz": {"language": "Ruby",' \
                 ' "url": "https://rubygems.org/gems/aclatraz"}, ' \
                 '"padrino-form-errors": {"language": "Ruby",' \
                 ' "url": "https://rubygems.org/gems/padrino-form-errors"}, ' \
                 '"react": {"language": "Ruby",' \
                 ' "url": "https://rubygems.org/gems/react"}, ' \
                 '"objectpool": {"language": "Ruby",' \
                 ' "url": "https://rubygems.org/gems/objectpool"}, ' \
                 '"leech": {"language": "Ruby",' \
                 ' "url": "https://rubygems.org/gems/leech"}, ' \
                 '"a13g": {"language": "Ruby",' \
                 ' "url": "https://rubygems.org/gems/a13g"}, ' \
                 '"haml-magic-translations": {"language": "Ruby",' \
                 ' "url": "https://rubygems.org/gems/haml-magic-' \
                 'translations"},' \
                 ' "padrino-responders": {"language": "Ruby",' \
                 ' "url": "https://rubygems.org/gems/padrino-responders"},' \
                 ' "mongoid_taggable": {"language": "Ruby",' \
                 ' "url": "https://rubygems.org/gems/mongoid_taggable"},' \
                 ' "authtools": {"language": "Ruby",' \
                 ' "url": "https://rubygems.org/gems/authtools"}, ' \
                 '"shaven": {"language": "Ruby",' \
                 ' "url": "https://rubygems.org/gems/shaven"}, ' \
                 '"kosmonaut": {"language": "Ruby",' \
                 ' "url": "https://rubygems.org/gems/kosmonaut"}, ' \
                 '"rails-block-labels": {"language": "Ruby",' \
                 ' "url": "https://rubygems.org/gems/rails-block-labels"}}}'
        self.assertEqual(rb_user(username), result)

    def test_rb_dev(self):
        packname = 'codecov'
        result = '{"0": {"username": "thomasrockhu", ' \
                 '"name": "Steve Peak, Tom Hu", ' \
                 '"yours_repositories": ' \
                 '{"codecov": {"language": "Ruby", ' \
                 '"url": "https://rubygems.org/gems/codecov"}}}, ' \
                 '"1": {"username": "codecov-joe", ' \
                 '"name": "Steve Peak, Tom Hu", ' \
                 '"yours_repositories": ' \
                 '{"codecov": {"language": "Ruby", ' \
                 '"url": "https://rubygems.org/gems/codecov"}}}, ' \
                 '"2": {"username": "hootener", ' \
                 '"name": "Steve Peak, Tom Hu", ' \
                 '"yours_repositories": ' \
                 '{"codecov": {"language": "Ruby", ' \
                 '"url": "https://rubygems.org/gems/codecov"}}}}'

        self.assertEqual(rb_dev(packname), result)


if __name__ == "__main__":
    unittest.main()

# %%%%%%%%%% The End %%%%%%%%%%#
