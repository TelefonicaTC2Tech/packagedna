import re
import tarfile
import json

from zipfile import ZipFile
from analyzers.typosquatting import typo_local
from console_prints.console_prints import print_bandit_not_installed_error
from analysis_pipeline.pipelines import ProcessPipeline

from py_analyzers.pydev import py_dev
from py_analyzers.pymetadata import py_metadata
from py_analyzers.pydownpackage import py_download
from py_analyzers.pydangerousfunctions import py_dangerous_functions
from py_analyzers.pybandit import py_analysis_bandit


class PythonProcessPipeline(ProcessPipeline):

    def get_packs(self, libraries):
        return json.loads(py_download(libraries))

    def get_typo_rta(self, typo_combinations):
        return typo_local('py', typo_combinations)

    def get_metadata(self, pack, files, pack_name, pkg_hash_id, local):
        return py_metadata(pack, files, pack_name, pkg_hash_id, local)

    def get_dangerous_functions(self, pack, files, pkg_hash_id):
        return py_dangerous_functions(pack, files, pkg_hash_id)
    
    def get_code_review(self, files):
        try:
            return py_analysis_bandit(files)
        except OSError:
            print_bandit_not_installed_error()
            return ''

    def get_files(self, pack):
        if re.search(".whl$", pack) or re.search(".zip$", pack) \
                or re.search(".egg$", pack):
            return ZipFile(pack, 'r')
        elif re.search(".tar.gz$", pack):
            return tarfile.open(pack, 'r:gz')
        elif re.search(".tar.bz2", pack):
            return tarfile.open(pack, 'r:bz2')
        else:
            raise ValueError('No se encontraron files .whl o .tar.gz')

    def get_devs(self, pack_name):
        return py_dev(pack_name)

    def get_extra(self):
        return 'python'

    def get_extra_cve(self):
        return 'pip'
