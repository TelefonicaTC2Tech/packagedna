#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from external_analyzers.users.user_github import user_github
from external_analyzers.users.user_bitbucket import user_bitbucker


class TestPackageDNA(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.username = ''

    def test_user_github(self):
        username = 'wesm'
        result = '{"username": "wesm", "name": "Wes McKinney", ' \
                 '"created_at": "2015-02-03T01:23:19.636Z", ' \
                 '"email": null, "website": "http://wesmckinney.com", ' \
                 '"location": "Nashville, TN", ' \
                 '"company": "@ursa-labs / @rstudio", "yours_repositories":' \
                 ' {"pydata-book": {"language": "Jupyter Notebook", ' \
                 '"url": "https://github.com/wesm/pydata-book"}, ' \
                 '"feather": {"language": "JavaScript", ' \
                 '"url": "https://github.com/wesm/feather"}, ' \
                 '"vbench": {"language": "Python", ' \
                 '"url": "https://github.com/wesm/vbench"}, ' \
                 '"vldb-2019-apache-arrow-workshop": ' \
                 '{"language": "Jupyter Notebook", ' \
                 '"url": "https://github.com/wesm/' \
                 'vldb-2019-apache-arrow-workshop"}, ' \
                 '"statlib": {"language": "Python", ' \
                 '"url": "https://github.com/wesm/statlib"}, ' \
                 '"ib-flex-analyzer": {"language": "Python", ' \
                 '"url": "https://github.com/wesm/ib-flex-analyzer"}, ' \
                 '"strata-sj-2015": {"language": "Python", ' \
                 '"url": "https://github.com/wesm/strata-sj-2015"}, ' \
                 '"pandas2-design": {"language": "JavaScript", ' \
                 '"url": "https://github.com/wesm/pandas2-design"}, ' \
                 '"read-table": {"language": null, ' \
                 '"url": "https://github.com/wesm/read-table"}, ' \
                 '"fye_2010": {"language": null, ' \
                 '"url": "https://github.com/wesm/fye_2010"}, ' \
                 '"charlton": {"language": "Python", ' \
                 '"url": "https://github.com/wesm/charlton"}, ' \
                 '"cyhello": {"language": null, ' \
                 '"url": "https://github.com/wesm/cyhello"}, ' \
                 '"pyarrow-windows-wheels": {"language": "Batchfile", ' \
                 '"url": "https://github.com/wesm/pyarrow-windows-' \
                 'wheels"}, ' \
                 '"arrow-io-test": {"language": null, ' \
                 '"url": "https://github.com/wesm/arrow-io-test"}, ' \
                 '"libhdfs3-downstream": {"language": null, ' \
                 '"url": "https://github.com/wesm/libhdfs3-downstream"' \
                 '}, "drawarray": {"language": null, ' \
                 '"url": "https://github.com/wesm/drawarray"}, ' \
                 '"arrow-site-test": {"language": null, ' \
                 '"url": "https://github.com/wesm/arrow-site-test"}, ' \
                 '"toolchain-build": {"language": null, ' \
                 '"url": "https://github.com/wesm/toolchain-build"}, ' \
                 '"hello": {"language": null, ' \
                 '"url": "https://github.com/wesm/hello"}}}'

        self.assertEqual(user_github(username), result)


if __name__ == "__main__":
    unittest.main()
