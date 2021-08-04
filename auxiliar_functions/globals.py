#!/usr/bin/env python3

# Create global variables

# %%%%%%%%%%% Libraries %%%%%%%%%%%#
import os

# %%%%%%%%%%% Constants %%%%%%%%%%%#

SEPARATOR = "[*] {0} [*]".format('-' * 110)

# Path's of directories
directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
downloads = directory + os.sep + 'download'
go_pkgs = directory + os.sep + 'download' + os.sep + 'go_pkgs'
git_pkgs = directory + os.sep + 'download' + os.sep + 'git_pkgs'
pypi_pkgs = directory + os.sep + 'download' + os.sep + 'pypi_pkgs'
ruby_pkgs = directory + os.sep + 'download' + os.sep + 'ruby_pkgs'
npm_pkgs = directory + os.sep + 'download' + os.sep + 'npm_pkgs'
sandbox = directory + os.sep + 'download' + os.sep + 'sandbox'
tmp = directory + os.sep + 'download' + os.sep + 'tmp'
tests = directory + os.sep + 'test' + os.sep + 'resources'
configurations_path = directory + os.sep + 'configurations.json'
flask_server_path = directory + os.sep + 'flask_server'
flask_server_data_folder = flask_server_path + os.sep + 'static' \
                           + os.sep + 'data'
appinspector_results = directory + os.sep + 'external_analyzers' + os.sep \
                       + 'appinspector' + os.sep + 'appinspector_results'

semgrep_results = directory + os.sep + 'external_analyzers' + os.sep \
                       + 'semgrep' + os.sep + 'semgrep_results'

# Path static files
cvepy = directory + os.sep + 'py_analyzers' + os.sep + 'insecure_full.json'
py_list = directory + os.sep + 'py_analyzers' + os.sep + 'py_packs_list.txt'
rb_list = directory + os.sep + 'rb_analyzers' + os.sep + 'rb_packs_list.txt'
npm_list = directory + os.sep + 'npm_analyzers' + os.sep + 'npm_packs_list.txt'


# Path static URL's Python
url_py = 'https://pypi.org/simple/'
url_py_dev = 'https://pypi.org/project/'
url_py_user = 'https://pypi.org/user/'
url_py_versions = 'https://pypi.org/pypi/'


# Path static URL's Ruby
url_rb = 'https://rubygems.org/gems'
url_rb_list = 'https://rubygems.org/names'
url_rb_user = 'https://api.rubygems.org/api/v1/owners/'
url_rb_dev = 'https://api.rubygems.org/api/v1/gems/'
url_rb_versions = 'https://api.rubygems.org/api/v1/versions/'
url_rb_download = 'https://rubygems.org/downloads/'


# Path static URL's NPM
url_npm = 'https://registry.npmjs.org/'
url_npm_user = 'https://www.npmjs.com/~'
url_npm_list = 'https://replicate.npmjs.com/_all_docs'


# Path static URL's GO
url_go = 'https://pkg.go.dev/'


# Path static URL's GitHub
url_git = 'https://api.github.com/repos/'
url_git_user = 'https://api.github.com/users/'

# Other statics URL's
url_cve = 'https://github.com/advisories?query=affects%3A'
libraries = 'https://libraries.io/api/github/'
url_vt_scan = "https://www.virustotal.com/vtapi/v2/file/scan"
url_vt_report = "https://www.virustotal.com/vtapi/v2/file/report"


# Statics Variables
extensions = ['.py', '.rst', '.json', '.txt', '.rb', '.yml', '.log', '.js',
              'LICENSE', 'METADATA', 'WHEEL', 'RECORD']
magics_extension_allowed = ['Python script',
                            'HTML document',
                            'ASCII text',
                            'CSV text',
                            'JSON data',
                            'ReStructuredText',
                            'UTF-8 Unicode text',
                            'very short file (no magic)',
                            'empty'
                            ]
malware_extensions = ['.exe', '.dll', '.bin']
values = ['__version__', '__author__', '', '[]', 'UNKNOWN', '__license__',
          'bout[\"__version__\"', 'bout[\"__license__\"', 'bout[\"__url__\"']
meta_pack = {"Name:": "",
             "Version:": "",
             "License:": "",
             "Home-page:": "",
             "Author:": "",
             "Author-email:": "",
             "Date:": ""
             }

select_url = {'py': url_py,
              'rb': url_rb + '/',
              'npm': url_npm,
              'go': url_go}

select_file = {'py': py_list,
               'python': py_list,
               'rb': rb_list,
               'ruby': rb_list,
               'npm': npm_list
               }

# Menus Variables
menu_start = [
              'Analyze Package (Last Version)',
              'Analyze Package (All Versions)',
              'Analyze local Package',
              'Information Gathering',
              'Upload file and analyze all Packages',
              # '[5] Download and Analyze all Packages (Very slow)',
              'List previously analyzed Packages',
              'Configurations'
              ]
menu_libraries = ['PyPI (Python Package Index)',
                  'RubyGems',
                  'Go',
                  'NPM (JavaScript)'
                  ]
menu_typo = ['Run with local database',
             'Update database local and run (slow)',
             'Run using list of websites (very slow)'
             ]

menu_information_gathering = [
    'Analyze username Packages',
    'Analyze Package for Typosquatting',
    'Search Code Extract',
]

menu_configurations = {
    'virustotal_key': 'VirusTotal API Key',
    'appinspector_path': 'AppInspector absolute Path',
    'libraries_io': 'Libraries.io API Key',
    'github_token': 'Github Token'
}


# TypoSquatting Detector
qwerty = {
    '1': '2q', '2': '3wq1', '3': '4ew2', '4': '5re3', '5': '6tr4', '6': '7yt5',
    '7': '8uy6', '8': '9iu7', '9': '0oi8', '0': 'po9',
    'q': '12wa', 'w': '3esaq2', 'e': '4rdsw3', 'r': '5tfde4', 't': '6ygfr5',
    'y': '7uhgt6', 'u': '8ijhy7', 'i': '9okju8', 'o': '0plki9', 'p': 'lo0',
    'a': 'qwsz', 's': 'edxzaw', 'd': 'rfcxse', 'f': 'tgvcdr', 'g': 'yhbvft',
    'h': 'ujnbgy', 'j': 'ikmnhu', 'k': 'olmji', 'l': 'kop',
    'z': 'asx', 'x': 'zsdc', 'c': 'xdfv', 'v': 'cfgb', 'b': 'vghn',
    'n': 'bhjm', 'm': 'njk'
}
qwertz = {
    '1': '2q', '2': '3wq1', '3': '4ew2', '4': '5re3', '5': '6tr4', '6': '7zt5',
    '7': '8uz6', '8': '9iu7', '9': '0oi8', '0': 'po9',
    'q': '12wa', 'w': '3esaq2', 'e': '4rdsw3', 'r': '5tfde4', 't': '6zgfr5',
    'z': '7uhgt6', 'u': '8ijhz7', 'i': '9okju8', 'o': '0plki9', 'p': 'lo0',
    'a': 'qwsy', 's': 'edxyaw', 'd': 'rfcxse', 'f': 'tgvcdr', 'g': 'zhbvft',
    'h': 'ujnbgz', 'j': 'ikmnhu', 'k': 'olmji', 'l': 'kop',
    'y': 'asx', 'x': 'ysdc', 'c': 'xdfv', 'v': 'cfgb', 'b': 'vghn',
    'n': 'bhjm', 'm': 'njk'
}
azerty = {
    '1': '2a', '2': '3za1', '3': '4ez2', '4': '5re3', '5': '6tr4', '6': '7yt5',
    '7': '8uy6', '8': '9iu7', '9': '0oi8', '0': 'po9',
    'a': '2zq1', 'z': '3esqa2', 'e': '4rdsz3', 'r': '5tfde4', 't': '6ygfr5',
    'y': '7uhgt6', 'u': '8ijhy7', 'i': '9okju8', 'o': '0plki9', 'p': 'lo0m',
    'q': 'zswa', 's': 'edxwqz', 'd': 'rfcxse', 'f': 'tgvcdr', 'g': 'yhbvft',
    'h': 'ujnbgy', 'j': 'iknhu', 'k': 'olji', 'l': 'kopm', 'm': 'lp',
    'w': 'sxq', 'x': 'wsdc', 'c': 'xdfv', 'v': 'cfgb', 'b': 'vghn', 'n': 'bhj'
}

replace = {
    'a': ['4'],
    'b': ['d', 'lb'],
    'c': ['e'],
    'd': ['b', 'cl', 'dl'],
    'e': ['c', '3'],
    'f': [],
    'g': ['q', '6'],
    'h': ['lh'],
    'i': ['1', 'l'],
    'j': [],
    'k': ['lk', 'ik', 'lc'],
    'l': ['1', 'i'],
    'm': ['n', 'nn', 'rn', 'rr'],
    'n': ['m', 'r'],
    'o': ['0'],
    'p': [],
    'q': ['g'],
    'r': ['2'],
    's': ['5', '$'],
    't': ['+', '7'],
    'u': [],
    'v': [],
    'w': ['vv'],
    'y': [],
    'z': [],
    '-': ['_'],
    '_': ['-']
}
keyboards = [qwerty, qwertz, azerty]
vowels = 'aeiou'
addition = ['python-', 'python_', '-python', '_python','python3-', 'python3_',
            '-python3', '_python3', 'py-', 'py_', '-py', '_py', 'py3-', 'py3_',
            '-py3', '_py3', 'ruby-', 'ruby_', '-ruby', '_ruby', 'rb-', 'rb_',
            'rb.', '-rb', '_rb', '.rb', 'npm-', 'node', 'node-', 'js-', '-js'
            '-lite', '_lite', '-plus', '-extras', '-adds', '-docs', '_1',
            '-1', '-inline']
substitution = {'python': ['python3', 'py', 'py3'],
                'python3': ['python', 'py', 'py3'],
                'py': ['python3', 'python', 'py3'],
                'py3': ['python3', 'py', 'python'],
                'ruby': ['rb'],
                'rb': ['ruby'],
                'js': ['node', 'node_', 'node-']
                }


# Comparators

gt = 'gt; '
ge = 'gt;= '
lt = 'lt; '
le = 'lt;= '
gts = '&gt; '
ges = '&gt;= '
lts = '&lt; '
les = '&lt;= '

# %%%%%%%%%% The End %%%%%%%%%%#
