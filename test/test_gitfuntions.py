#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import unittest


from auxiliar_functions.globals import tests
from auxiliar_functions.globals import git_pkgs

from analyzers.hashfiles import get_hash_pkg
from git_analyzers.gitdev import git_dev
from git_analyzers.gituser import git_user
from git_analyzers.gitlibrary import git_library
from git_analyzers.gitmetadata import git_metadata
from git_analyzers.gitdownpackage import git_download


class TestPyFunctions(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.result = ''
        self.result_true = ''
        self.result_false = ''
        self.pack = 'terra-project/mantle'
        self.path_pack = ''
        self.username = 'terra-project'
        self.url = ''
        self.metadata_found = ''
        self.library = {
            "terra-project/mantle":
                {"v0.3.1": ["https://api.github.com/repos/terra-project/"
                            "mantle/zipball/v0.3.1",
                            "ead2574222ebaf3da262195ccabf3244b336ffe7"],
                 "v0.3.0": ["https://api.github.com/repos/terra-project/"
                            "mantle/zipball/v0.3.0",
                            "b443eed3ad74ec9995d279f51ca38eac 'bf83cd32"],
                 "v0.3.0-rc.4": ["https://api.github.com/repos/terra-project/"
                                 "mantle/zipball/v0.3.0-rc.4",
                                 "c6407cec4d9cd1f1edd2fd0ae14cfc744348c284"]}}

    """def test_git_library(self):
        result = '{"terra-project/mantle": {"v0.3.2": ' \
                 '["https://api.github.com/repos/terra-project/mantle/' \
                 'zipball/v0.3.2", "3fa28fa87099cade86fb706c5fd73d7f20e8' \
                 '7714"], "v0.3.1": ' \
                 '["https://api.github.com/repos/terra-project/mantle/' \
                 'zipball/v0.3.1", "ead2574222ebaf3da262195ccabf3244b336ffe7' \
                 '"], "v0.3.0": ["https://api.github.com/repos/terra-project' \
                 '/mantle/zipball/v0.3.0", "b443eed3ad74ec9995d279f51ca38eac' \
                 'bf83cd32"], "v0.3.0-rc.4": ["https://api.github.com/repos/' \
                 'terra-project/mantle/zipball/v0.3.0-rc.4", "c6407cec4d9cd1' \
                 'f1edd2fd0ae14cfc744348c284"], "v0.3.0-rc.3": ["https://api' \
                 '.github.com/repos/terra-project/mantle/zipball/v0.3.0-rc.' \
                 '3", "b7437d6a973bae96b62e8c1d9ac480e11872db02"], "v0.3.0-r' \
                 'c.2": ["https://api.github.com/repos/terra-project/mantle/' \
                 'zipball/v0.3.0-rc.2", "04cb98d78bbdfa94ab5c15f99e77c8c1a9a' \
                 'aa20a"], "v0.3.0-rc.1": ["https://api.github.com/repos/ter' \
                 'ra-project/mantle/zipball/v0.3.0-rc.1", "c23bd2d385424a025' \
                 'ee5b748319afd118f3d407a"], "v0.3.0-rc.0": ["https://api.gi' \
                 'thub.com/repos/terra-project/mantle/zipball/v0.3.0-rc.0", ' \
                 '"df7620097eead916a39ee0341e04fe24dc0178b2"], "v0.2.9999-mo' \
                 'onshine": ["https://api.github.com/repos/terra-project/man' \
                 'tle/zipball/v0.2.9999-moonshine", "aadab12bc575962cf711ff5' \
                 '78496767a02274a8d"], "v0.2.7": ["https://api.github.com/re' \
                 'pos/terra-project/mantle/zipball/v0.2.7", "416243cc8fd11b9' \
                 'ba9630d8f253a01e9671f84e4"], "v0.2.6": ["https://api.githu' \
                 'b.com/repos/terra-project/mantle/zipball/v0.2.6", "59bfe67' \
                 '780f3c42e8a620de30bfd7bf7b6a48cd8"], "v0.2.4": ["https://a' \
                 'pi.github.com/repos/terra-project/mantle/zipball/v0.2.4", ' \
                 '"93eb3b8e194ea8ff790cc1702a269e0282167877"], "v0.2.3": ["h' \
                 'ttps://api.github.com/repos/terra-project/mantle/zipball/v' \
                 '0.2.3", "5f9ca094fe342de5a5040fb92bb53fa8472dcf38"], "v0.2' \
                 '.2": ["https://api.github.com/repos/terra-project/mantle/z' \
                 'ipball/v0.2.2", "87197eabcaab5a997a453323ce6384cd54d187f7"' \
                 '], "v0.2.1": ["https://api.github.com/repos/terra-project' \
                 '/mantle/zipball/v0.2.1", "2cb1a2c4f008b889641624f90696b26' \
                 '7189958fe"], "v0.2.0": ["https://api.github.com/repos/ter' \
                 'ra-project/mantle/zipball/v0.2.0", "2cb1a2c4f008b88964162' \
                 '4f90696b267189958fe"], "v0.1.9": ["https://api.github.com' \
                 '/repos/terra-project/mantle/zipball/v0.1.9", "23eeb295faa' \
                 '3e33311c4a04cfb78afbd0f4e84df"], "v0.1.8": ["https://api.' \
                 'github.com/repos/terra-project/mantle/zipball/v0.1.8", "6' \
                 '9622401d009a9554e6188f4d1ee037b1f4ba8cc"], "v0.1.7": ["ht' \
                 'tps://api.github.com/repos/terra-project/mantle/zipball/v' \
                 '0.1.7", "16fedb1b290089d323671f104e8dca09438d792b"], "v0' \
                 '.1.6": ["https://api.github.com/repos/terra-project/mant' \
                 'le/zipball/v0.1.6", "c998abf02eaf540554648eac519f2a80dc2' \
                 'b0623"], "v0.1.5": ["https://api.github.com/repos/terra-' \
                 'project/mantle/zipball/v0.1.5", "9099bf38778f2c8e79c3effb' \
                 '02a54ca779d5bed2"], "v0.1.4": ["https://api.github.com/re' \
                 'pos/terra-project/mantle/zipball/v0.1.4", "2f53144fa0f3e3' \
                 'a73a431662a22bd68ca5cb0a36"], "v0.1.3": ["https://api.git' \
                 'hub.com/repos/terra-project/mantle/zipball/v0.1.3", "2a9a' \
                 'e2d955f9da73a299db515ff41e1b23c1ed7c"], "v0.1.2": ["https' \
                 '://api.github.com/repos/terra-project/mantle/zipball/v0.1' \
                 '.2", "e40c379070d967c7b4441f133308c64da93335c8"], "v0.1.1' \
                 '": ["https://api.github.com/repos/terra-project/mantle/zi' \
                 'pball/v0.1.1", "1e51e2dc2155c2edf50e26f138eeedbb8be60dbc"' \
                 '], "v0.1.0": ["https://api.github.com/repos/terra-project' \
                 '/mantle/zipball/v0.1.0", "082f721a3125c6b882013ee27577677' \
                 'af115c93a"], "v0.1.0-rc.1": ["https://api.github.com/repo' \
                 's/terra-project/mantle/zipball/v0.1.0-rc.1", "9eb2c27fcf9' \
                 '673f6b6b6cc39d99cbad0c3836c0b"], "v0.0.2-rc.3": ["https:/' \
                 '/api.github.com/repos/terra-project/mantle/zipball/v0.0.2' \
                 '-rc.3", "caf898e66c0f40a5cd03e6433601f73a5c62d6ad"], "v0.' \
                 '0.2-rc.2": ["https://api.github.com/repos/terra-project/m' \
                 'antle/zipball/v0.0.2-rc.2", "f0e39f5ed990570d06fefeecfaaf' \
                 '6eb56a5b7aef"], "v0.0.2-rc.1": ["https://api.github.com/r' \
                 'epos/terra-project/mantle/zipball/v0.0.2-rc.1", "8960814d' \
                 '5f34723be8b971f62ccbfa4fc4aea53d"], "v0.0.1-rc.1": ["http' \
                 's://api.github.com/repos/terra-project/mantle/zipball/v0.' \
                 '0.1-rc.1", "37d54bcc51ed9e62ffc748e8c29e84033c6f792e"]}}'

        url = 'https://github.com/terra-project/mantle'
        libraries = {}
        git_library_rta = git_library(url, libraries)
        self.assertEqual(git_library_rta, result)

    def test_git_download(self):
        path = git_pkgs + os.sep
        result = f'["{path}terra-project_-_mantle_--_v0.3.1", ' \
                 f'"{path}terra-project_-_mantle_--_v0.3.0",' \
                 f' "{path}terra-project_-_mantle_--_v0.3.0-rc.4"]'

        libraries = self.library
        git_download_rta = git_download(libraries)
        self.assertEqual(git_download_rta, result)

    def test_git_metadata(self):
        pack = 'terra-project/mantle'
        path = tests + os.sep + 'terra-project_-_mantle_--_v0.3.0'
        result = '{"pkg_hashid": "ab10ad86a697a68f1e7042c467b34510299f7a85' \
                 '59e8b85faf04fc2c603fa5ab", "name": "terra-project/mantle"' \
                 ', "path_pack": "' + path + '", ' \
                 '"author": "jess", "author_email": "jesse@terra.money",' \
                 ' "version": "v0.3.0", "date": "2020-12-05T18:21:36Z"}'
        files = ''

        package_hash = get_hash_pkg(path)
        git_metadata_rta = git_metadata(path, files, pack, package_hash, False)
        self.assertEqual(git_metadata_rta, result)

    def test_git_user(self):
        result = '{"username": "terra-project", "name": "Terra", ' \
                 '"yours_repositories": {"amino-decoder": {"language": "Go",' \
                 ' "url": "https://github.com/terra-project/amino-decoder"},' \
                 ' "amino-js": {"language": "TypeScript", ' \
                 '"url": "https://github.com/terra-project/amino-js"}, ' \
                 '"apidoc-swagger": {"language": "JavaScript", ' \
                 '"url": "https://github.com/terra-project/apidoc-swagger"},' \
                 ' "app-terra": {"language": "C", ' \
                 '"url": "https://github.com/terra-project/app-terra"}, ' \
                 '"assets": {"language": null, ' \
                 '"url": "https://github.com/terra-project/assets"}, ' \
                 '"awesome-terra": {"language": null, ' \
                 '"url": "https://github.com/terra-project/awesome-terra"}, ' \
                 '"core": {"language": "Go", ' \
                 '"url": "https://github.com/terra-project/core"}, ' \
                 '"cosmwasm": {"language": "Rust", ' \
                 '"url": "https://github.com/terra-project/cosmwasm"}, ' \
                 '"cosmwasm-contracts": {"language": "Rust", ' \
                 '"url": "https://github.com/terra-project/cosmwasm-' \
                 'contracts"}, "delegations": {"language": null, ' \
                 '"url": "https://github.com/terra-project/delegations"}, ' \
                 '"deposit-tracker": {"language": "TypeScript", ' \
                 '"url": "https://github.com/terra-project/deposit-tracker"}' \
                 ', "docs": {"language": null, ' \
                 '"url": "https://github.com/terra-project/docs"}, ' \
                 '"documentation": {"language": "TeX", ' \
                 '"url": "https://github.com/terra-project/documentation"}, ' \
                 '"faucet": {"language": "JavaScript", ' \
                 '"url": "https://github.com/terra-project/faucet"}, ' \
                 '"fcd": {"language": "HTML", ' \
                 '"url": "https://github.com/terra-project/fcd"}, ' \
                 '"finder": {"language": "TypeScript", ' \
                 '"url": "https://github.com/terra-project/finder"}, ' \
                 '"gitcoin-onboarding": {"language": null, ' \
                 '"url": "https://github.com/terra-project/gitcoin-' \
                 'onboarding"}, "go-cosmwasm": {"language": "Go", ' \
                 '"url": "https://github.com/terra-project/go-cosmwasm"}, ' \
                 '"houston": {"language": "TypeScript", ' \
                 '"url": "https://github.com/terra-project/houston"}, ' \
                 '"jigu": {"language": "Python", ' \
                 '"url": "https://github.com/terra-project/jigu"}, ' \
                 '"key-utils": {"language": "TypeScript", ' \
                 '"url": "https://github.com/terra-project/key-utils"}, ' \
                 '"keyserver": {"language": "Go", ' \
                 '"url": "https://github.com/terra-project/keyserver"}, ' \
                 '"ledger-terra-go": {"language": "Go", ' \
                 '"url": "https://github.com/terra-project/ledger-terra-go"}' \
                 ', "ledger-terra-js": {"language": "TypeScript", ' \
                 '"url": "https://github.com/terra-project/ledger-terra-js"}' \
                 ', "LocalTerra": {"language": "TypeScript", ' \
                 '"url": "https://github.com/terra-project/LocalTerra"}, ' \
                 '"mainnet": {"language": null, ' \
                 '"url": "https://github.com/terra-project/mainnet"}, ' \
                 '"mantle": {"language": "Go", ' \
                 '"url": "https://github.com/terra-project/mantle"}, ' \
                 '"mantle-compatibility": {"language": "Go", ' \
                 '"url": "https://github.com/terra-project/mantle-' \
                 'compatibility"}, "mantle-sdk": {"language": "Go", ' \
                 '"url": "https://github.com/terra-project/mantle-sdk"}, ' \
                 '"my-terra-token": {"language": "Rust", ' \
                 '"url": "https://github.com/terra-project/my-terra-token"}}}'

        self.assertEqual(git_user(self.username), result)

    def test_git_dev(self):
        result = '{"0": {"username": "etienne-napoleone", "name": ' \
                 '"Etienne Napoleone", "yours_repositories": {"b64tofile": ' \
                 '{"language": "Python", "url": "https://github.com/etienne-' \
                 'napoleone/b64tofile"}, "chalk": {"language": "V", "url": ' \
                 '"https://github.com/etienne-napoleone/chalk"}, "claim-mir' \
                 '-airdrops": {"language": "HTML", "url": "https://github.' \
                 'com/etienne-napoleone/claim-mir-airdrops"}, "classic-addo' \
                 'ns": {"language": "Lua", "url": "https://github.com/etien' \
                 'ne-napoleone/classic-addons"}, "docker-python-poetry": ' \
                 '{"language": "Dockerfile", "url": "https://github.com/et' \
                 'ienne-napoleone/docker-python-poetry"}, "docs": {"langua' \
                 'ge": null, "url": "https://github.com/etienne-napoleone/' \
                 'docs"}, "dotfiles": {"language": "Shell", "url": "https:' \
                 '//github.com/etienne-napoleone/dotfiles"}, "forkedthanks":' \
                 ' {"language": "Python", "url": "https://github.com/etienne' \
                 '-napoleone/forkedthanks"}, "gnurms": {"language": "Python"' \
                 ', "url": "https://github.com/etienne-napoleone/gnurms"}, "' \
                 'goutte": {"language": "Python", "url": "https://github.com' \
                 '/etienne-napoleone/goutte"}, "maxbet-watcher": {"language"' \
                 ': "JavaScript", "url": "https://github.com/etienne-napoleo' \
                 'ne/maxbet-watcher"}, "Photon": {"language": "Python", "url' \
                 '": "https://github.com/etienne-napoleone/Photon"}, "poche' \
                 '": {"language": "Python", "url": "https://github.com/etie' \
                 'nne-napoleone/poche"}, "poetry": {"language": "Python", "' \
                 'url": "https://github.com/etienne-napoleone/poetry"}, "py' \
                 'thon-base": {"language": null, "url": "https://github.com' \
                 '/etienne-napoleone/python-base"}, "ReactJSMasterClass2018' \
                 '": {"language": "JavaScript", "url": "https://github.com/' \
                 'etienne-napoleone/ReactJSMasterClass2018"}, "restpass": {' \
                 '"language": "Python", "url": "https://github.com/etienne-' \
                 'napoleone/restpass"}, "saifu": {"language": "Python", "ur' \
                 'l": "https://github.com/etienne-napoleone/saifu"}, "scrmb' \
                 'l": {"language": "Python", "url": "https://github.com/eti' \
                 'enne-napoleone/scrmbl"}, "slack-alerts": {"language": "Py' \
                 'thon", "url": "https://github.com/etienne-napoleone/slack' \
                 '-alerts"}, "test-redeploy": {"language": "HTML", "url": "' \
                 'https://github.com/etienne-napoleone/test-redeploy"}, "th' \
                 'oughtful-investor": {"language": "Python", "url": "https:' \
                 '//github.com/etienne-napoleone/thoughtful-investor"}, "to' \
                 'mochain-box": {"language": "JavaScript", "url": "https://' \
                 'github.com/etienne-napoleone/tomochain-box"}, "validator-' \
                 'profiles": {"language": null, "url": "https://github.com/' \
                 'etienne-napoleone/validator-profiles"}, "web3-react": {"l' \
                 'anguage": null, "url": "https://github.com/etienne-napole' \
                 'one/web3-react"}, "whaleherder": {"language": "Python", "' \
                 'url": "https://github.com/etienne-napoleone/whaleherder"}' \
                 '}}, "1": {"username": "hanjukim", "name": "Paul Kim", "yo' \
                 'urs_repositories": {"array-unpivot": {"language": "JavaSc' \
                 'ript", "url": "https://github.com/hanjukim/array-unpivot"' \
                 '}, "astar-algorithm-cpp": {"language": "C++", "url": "htt' \
                 'ps://github.com/hanjukim/astar-algorithm-cpp"}, "bip32": ' \
                 '{"language": null, "url": "https://github.com/hanjukim/bi' \
                 'p32"}, "bluebird": {"language": null, "url": "https://git' \
                 'hub.com/hanjukim/bluebird"}, "camelcase-object-deep": {"l' \
                 'anguage": "JavaScript", "url": "https://github.com/hanjuk' \
                 'im/camelcase-object-deep"}, "core": {"language": null, "u' \
                 'rl": "https://github.com/hanjukim/core"}, "cosmos-sdk": {"' \
                 'language": null, "url": "https://github.com/hanjukim/cosmo' \
                 's-sdk"}, "crypto-js": {"language": "JavaScript", "url": "h' \
                 'ttps://github.com/hanjukim/crypto-js"}, "drone-now": {"lan' \
                 'guage": null, "url": "https://github.com/hanjukim/drone-no' \
                 'w"}, "effective-go": {"language": null, "url": "https://gi' \
                 'thub.com/hanjukim/effective-go"}, "extensionizer": {"langu' \
                 'age": null, "url": "https://github.com/hanjukim/extensioni' \
                 'zer"}, "hdkey": {"language": null, "url": "https://github.' \
                 'com/hanjukim/hdkey"}, "ledgerjs": {"language": null, "url"' \
                 ': "https://github.com/hanjukim/ledgerjs"}, "mantis2trac": ' \
                 '{"language": "Python", "url": "https://github.com/hanjukim' \
                 '/mantis2trac"}, "mysql-operator": {"language": null, "url"' \
                 ': "https://github.com/hanjukim/mysql-operator"}, "node-ben' \
                 'chmarks": {"language": "JavaScript", "url": "https://githu' \
                 'b.com/hanjukim/node-benchmarks"}, "node-slate": {"language' \
                 '": "JavaScript", "url": "https://github.com/hanjukim/node-' \
                 'slate"}, "react-redux-universal-hot-example": {"language":' \
                 ' "JavaScript", "url": "https://github.com/hanjukim/reac' \
                 't-redux-universal-hot-example"}, "reminders-app-for-bro' \
                 'wsers": {"language": "JavaScript", "url": "https://gith' \
                 'ub.com/hanjukim/reminders-app-for-browsers"}, "sc-jsonw' \
                 'ebtoken": {"language": "JavaScript", "url": "https://gith' \
                 'ub.com/hanjukim/sc-jsonwebtoken"}, "tendermint": {"langua' \
                 'ge": null, "url": "https://github.com/hanjukim/tendermint' \
                 '"}, "testnet": {"language": "Python", "url": "https://git' \
                 'hub.com/hanjukim/testnet"}, "TinyPNG": {"language": "Shel' \
                 'l", "url": "https://github.com/hanjukim/TinyPNG"}, "typeo' \
                 'rm": {"language": "TypeScript", "url": "https://github.co' \
                 'm/hanjukim/typeorm"}, "typeorm-encrypted-column": {"langu' \
                 'age": "TypeScript", "url": "https://github.com/hanjukim/t' \
                 'ypeorm-encrypted-column"}, "uuid-base91": {"language": "J' \
                 'avaScript", "url": "https://github.com/hanjukim/uuid-base' \
                 '91"}, "uuid-d64": {"language": "JavaScript", "url": "http' \
                 's://github.com/hanjukim/uuid-d64"}, "vault-btc": {"langua' \
                 'ge": null, "url": "https://github.com/hanjukim/vault-btc"' \
                 '}, "wasmer": {"language": null, "url": "https://github.co' \
                 'm/hanjukim/wasmer"}}}, "2": {"username": "kjessec", "name' \
                 '": "Jesse Chung", "yours_repositories": {"atom-react-play' \
                 '-now": {"language": "JavaScript", "url": "https://github.' \
                 'com/kjessec/atom-react-play-now"}, "Conseil": {"language"' \
                 ': null, "url": "https://github.com/kjessec/Conseil"}, "cr' \
                 'eate-react-app-lambda": {"language": "JavaScript", "url":' \
                 ' "https://github.com/kjessec/create-react-app-lambda"}, "' \
                 'docs": {"language": null, "url": "https://github.com/kjes' \
                 'sec/docs"}, "dope": {"language": "JavaScript", "url": "ht' \
                 'tps://github.com/kjessec/dope"}, "dotprop": {"language":' \
                 ' null, "url": "https://github.com/kjessec/dotprop"}, "gat' \
                 'sby-starter-netlify-cms": {"language": "JavaScript", "url' \
                 '": "https://github.com/kjessec/gatsby-starter-netlify-cms' \
                 '"}, "goleveldb-cli": {"language": null, "url": "https://g' \
                 'ithub.com/kjessec/goleveldb-cli"}, "gpu.js": {"language":' \
                 ' null, "url": "https://github.com/kjessec/gpu.js"}, "gran' \
                 'ary": {"language": null, "url": "https://github.com/kjess' \
                 'ec/granary"}, "hls-example": {"language": "Shell", "url":' \
                 ' "https://github.com/kjessec/hls-example"}, "iperf": {"la' \
                 'nguage": "C", "url": "https://github.com/kjessec/iperf"},' \
                 ' "kjessec.github.io": {"language": "JavaScript", "url": "' \
                 'https://github.com/kjessec/kjessec.github.io"}, "mantle-s' \
                 'dk": {"language": null, "url": "https://github.com/kjesse' \
                 'c/mantle-sdk"}, "nft.stove-labs.com": {"language": null, ' \
                 '"url": "https://github.com/kjessec/nft.stove-labs.com"}, ' \
                 '"object-array-converter": {"language": "JavaScript", "url' \
                 '": "https://github.com/kjessec/object-array-converter"}, ' \
                 '"object-path-wild": {"language": "JavaScript", "url": "ht' \
                 'tps://github.com/kjessec/object-path-wild"}, "omnimap": {' \
                 '"language": "JavaScript", "url": "https://github.com/kjes' \
                 'sec/omnimap"}, "owo": {"language": null, "url": "https://' \
                 'github.com/kjessec/owo"}, "react-ajax-props": {"language"' \
                 ': "JavaScript", "url": "https://github.com/kjessec/react-' \
                 'ajax-props"}, "react-diagrams": {"language": "JavaScript"' \
                 ', "url": "https://github.com/kjessec/react-diagrams"}, "r' \
                 'eact-formagic": {"language": "JavaScript", "url": "https:' \
                 '//github.com/kjessec/react-formagic"}, "react-jss": {"lan' \
                 'guage": "JavaScript", "url": "https://github.com/kjessec/' \
                 'react-jss"}, "react-tutorial": {"language": "JavaScript",' \
                 ' "url": "https://github.com/kjessec/react-tutorial"}, "re' \
                 'compose": {"language": "JavaScript", "url": "https://gith' \
                 'ub.com/kjessec/recompose"}, "redactor-js": {"language": "' \
                 'JavaScript", "url": "https://github.com/kjessec/redactor-' \
                 'js"}, "redux-direct-update": {"language": "JavaScript", "' \
                 'url": "https://github.com/kjessec/redux-direct-update"}, ' \
                 '"redux-schema-sanitizing-reducer": {"language": "JavaScri' \
                 'pt", "url": "https://github.com/kjessec/redux-schema-sani' \
                 'tizing-reducer"}, "seiki-no-taiketsu": {"language": "Java' \
                 'Script", "url": "https://github.com/kjessec/seiki-no-taik' \
                 'etsu"}, "simple-slider": {"language": "JavaScript", "url"' \
                 ': "https://github.com/kjessec/simple-slider"}}}}'
        self.assertEqual(git_dev(self.pack), result)"""


if __name__ == "__main__":
    unittest.main()

# %%%%%%%%%% The End %%%%%%%%%%#
