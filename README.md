# PackageDNA

This tool gives developers, researchers and companies the ability to analyze software packages of different programming languages
that are being or will be used in their codes, providing information that allows them to know in advance if this library complies 
with processes. secure development, if currently supported, possible backdoors (malicious embedded code), typosquatting analysis, 
the history of versions and reported vulnerabilities (CVEs) of the package.

---

## Installation

Clone this repository with:
```bash
git clone https://github.com/ElevenPaths/packagedna
```

**PackageDNA uses python-magic** which is a simple wrapper around the libmagic C library, and that **MUST** be installed as well:
```bash

Debian/Ubuntu
$ sudo apt-get install libmagic1

Windows
You will need DLLs for libmagic. @julian-r has uploaded a version of this project that includes binaries 
to PyPI: https://pypi.python.org/pypi/python-magic-bin/0.4.14
Other sources of the libraries in the past have been File for Windows. 
You will need to copy the file magic out of [binary-zip]\share\misc, and pass its location to Magic(magic_file=...).

If you are using a 64-bit build of python, you will need 64-bit libmagic binaries which can be found here: https://github.com/pidydx/libmagicwin64.
Newer version can be found here: https://github.com/nscaife/file-windows.

OSX
When using Homebrew: brew install libmagic
When using macports: port install file


More details: https://pypi.org/project/python-magic/
```

Run setup for installation:

```bash
python3 setup.py install --user
```

---

## External Modules

PackageDNA uses external modules for its analysis that you should install previously:

Microsoft AppInpsector
```bash
https://github.com/microsoft/ApplicationInspector
```

Virus Total API

```bash
https://www.virustotal.com/
```

LibrariesIO API

```bash
https://libraries.io/
```

Rubocop

```bash
https://github.com/rubocop/rubocop
```

After installation you should configure the external modules, in the option [7] Configuration 
of the main menu.

```bash
[1] VirusTotal API Key: Your API KEY
[2] AppInspector absolute path: /Local/Path/MSAppInpsectorInstallation
[3] Libraries.io API Key: Your API KEY
[4] Github Token: Your Token
[B] Back
[X] Exit
```

**NOTE:** External modules are not mandatory. PackageDNA will continue its execution, however we recommend making 
all the configurations of these modules so that the tool performs a complete analysis


### Running PackageDNA

Inside the PackageDNA directory:

```bash
./packagedna.py
```

```bash
_____              _                          ____     __     _  _______ 
|  __ \            | |                        |  __ \  |   \  | ||  ___  |
| |__) |__ __ ____ | | __   __ __  ____   ___ | |  \ \ | |\ \ | || |___| |
|  ___// _` |/  __)| |/ /  / _` | / _  | / _ \| |   | || | \ \| ||  ___  |
| |   | (_| || (__ | |\ \ | (_| || (_| ||  __/| |__/ / | |  \   || |   | |
|_|    \__,_|\____)|_| \_\ \__,_| \__  | \___||_____/  |_|   \__||_|   |_|
                                   __| |
                                  (____|

Modular Packages Analyzer Framework
By ElevenPaths https://www.elevenpaths.com/
Usage: python3 ./packagedna.py

[*] -------------------------------------------------------------------------------------------------------------- [*]
[!] Select from the menu:
[*] -------------------------------------------------------------------------------------------------------------- [*]
	[1] Analyze Package (Last Version)
	[2] Analyze Package (All Versions)
	[3] Analyze local package
	[4] Information gathering
	[5] Upload file and analyze all Packages
	[6] List previously analyzed packages
	[7] Configurations
	[X] Exit
[*] -------------------------------------------------------------------------------------------------------------- [*]
[!] Enter your selection: 
```

### More info

**Wiki:** [https://innovation-gitlab.e-paths.com/private/packagedna/-/wikis/PackageDNA](https://innovation-gitlab.e-paths.com/private/packagedna/-/wikis/PackageDNA)