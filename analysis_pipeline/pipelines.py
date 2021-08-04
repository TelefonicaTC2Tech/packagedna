
import abc
import json

from tqdm import tqdm
from pathlib import Path

from analyzers.cve_git import cve_git
from analyzers.hashfiles import hash_files
from analyzers.hashfiles import get_hash_pkg
from analyzers.datafiles import extract_data
from analyzers.typosquatting import typos_create
from flask_server.run_server import generate_json
from analyzers.code_analysis import extract_data_code_extract
from auxiliar_functions.auxiliar_functions import (
    get_app_inspector_path,
    get_virus_total_api_key
)
from console_prints.console_prints import (
    print_library, print_cves_json,
    print_metadata_json,
    print_dangerous_functions_json,
    print_hashfiles_json,
    print_extract_data_json,
    print_appinspector_json,
    print_typosquatting,
    print_appinspector_path_error,
    print_virustotal_api_key_error, print_user_dev_json
)
from external_analyzers.appinspector.appinspector_data \
    import appinspector_process
from external_analyzers.virustotal.virustotal_analysis \
    import virustotal_analysis


class ProcessPipeline(abc.ABC):

    def __init__(self, libraries, local=False, package_input_name=None):
        self.path_pack = []

        self.cve_rta = set()
        self.metadata_rta = set()
        self.dangerous_function_rta = set()
        self.analysis_code_rta = []
        self.hash_files_rta = []
        self.extract_data_rta = []
        self.app_inspector_rta = []
        self.app_inspector_path = ''
        self.virus_total_rta = []
        self.packages_versions = []
        self.packages_names = []
        self.typo_combinations = []
        self.typo_rta = []
        self.package_input_name = package_input_name
        self.local = local
        self.libraries = libraries
        self.path_pack = []
        self.user_dev_rta = set()
        if self.local:
            self.pkg_hash_id = get_hash_pkg(libraries)
            self.path_pack.append(libraries)
        else:
            packs = self.get_packs(self.libraries)
            for pack in packs:
                pack_name = Path(pack).resolve().stem
                pack = pack.replace(pack_name, pack_name.lower())
                self.path_pack.append(pack)

    @abc.abstractmethod
    def get_packs(self, libraries):
        pass

    @abc.abstractmethod
    def get_typo_rta(self, typo_combinations):
        pass

    @abc.abstractmethod
    def get_metadata(self, pack, files, pack_name, pkg_hash_id, local):
        pass

    @abc.abstractmethod
    def get_dangerous_functions(self, pack, files, pkg_hash_id):
        pass

    @abc.abstractmethod
    def get_code_review(self, files):
        pass

    @abc.abstractmethod
    def get_files(self, pack):
        pass

    @abc.abstractmethod
    def get_devs(self, pack):
        pass

    @abc.abstractmethod
    def get_extra(self):
        pass

    @abc.abstractmethod
    def get_extra_cve(self):
        pass

    def get_code_analysis(self, code_extract):
        full_analysis = []
        for pack in tqdm(self.path_pack, desc=' Processing packages...'):
            files = self.get_files(pack)
            pkg_hash_id = get_hash_pkg(pack)
            full_analysis.append(extract_data_code_extract(
                pack, files, pkg_hash_id, code_extract))
        return full_analysis

    def __get_metadata_variables(self, metadata):
        """
        takes the last metadata collected in self.metadata_rta, extract
        the version key and append to self.packages_versions attribute
        """
        try:
            packages_versions = json.loads(metadata)['version']
        except:
            packages_versions = -1
        try:
            packages_names = json.loads(metadata)['name']
        except:
            packages_names = 'None'

        return packages_versions, packages_names

    def __set_app_inspector_path(self):
        try:
            self.app_inspector_path = get_app_inspector_path()
            if not self.app_inspector_path:
                raise ValueError('Path is missing.')
        except ValueError:
            print_appinspector_path_error()

    def __set_virus_total_api_key(self):
        try:
            self.virus_total_key = get_virus_total_api_key()
            if not self.virus_total_key:
                raise ValueError('Key is missing.')
        except ValueError:
            print_virustotal_api_key_error()

    def _set_typos_create(self, package_input_name):
        try:
            self.typo_combinations = typos_create(
                package_input_name, self.get_extra())
        except:
            self.typo_combinations = []

    def __start_typo_process(self):
        self._set_typos_create(self.package_input_name)
        self.typo_rta = self.get_typo_rta(self.typo_combinations)

    def __start_app_inspector_process(self, pack, files):
        if self.app_inspector_path:
            self.app_inspector_rta.append(appinspector_process(
                pack, files, self.app_inspector_path))

    def __start_virus_total_process(self, name):
        if self.virus_total_key:
            """
            if self.virustotal_key exists, execute virustotal_analysis
            """
            self.virus_total_rta.append(virustotal_analysis(
                name, self.virus_total_key))

    def __start_cve_process(self, name, language, version):
        if not self.local:
            """
            if the package is not a local one, then execute cve_git
            """
            try:
                self.cve_rta.add(cve_git(name, language, version))
            except:
                pass

    def start_process_pipeline(self):
        self.__start_typo_process()
        self.__set_app_inspector_path()
        self.__set_virus_total_api_key()
        for pack in tqdm(self.path_pack, desc=' Processing packages...'):
            pkg_hash_id = get_hash_pkg(pack)
            files = self.get_files(pack)
            metadata = self.get_metadata(pack=pack, files=files,
                                         pack_name=self.package_input_name,
                                         pkg_hash_id=pkg_hash_id,
                                         local=self.local)
            self.metadata_rta.add(metadata)
            version, name = self.__get_metadata_variables(metadata)
            self.dangerous_function_rta.add(
                self.get_dangerous_functions(pack, files, pkg_hash_id))
            self.analysis_code_rta.append(
                self.get_code_review(files))
            self.hash_files_rta.append(hash_files(pack, pkg_hash_id, files))
            self.extract_data_rta.append(extract_data(
                pack, files, pkg_hash_id))
            self.__start_app_inspector_process(pack=pack, files=files)
            self.__start_cve_process(
                name=name, language=self.get_extra_cve(), version=version)
            self.__start_virus_total_process(name=name)
            self.user_dev_rta.add(self.get_devs(name))
            files.close()
        self.export_json()

    def print_process_pipeline(self):
        print_library(self.libraries)
        print_cves_json(self.cve_rta, self.package_input_name)
        print_metadata_json(self.metadata_rta, self.package_input_name)
        print_dangerous_functions_json(self.dangerous_function_rta,
                                       self.package_input_name)
        print_hashfiles_json(self.hash_files_rta, self.package_input_name)
        print_extract_data_json(self.extract_data_rta, self.package_input_name)
        print_appinspector_json(
            self.app_inspector_rta, self.package_input_name)
        print_typosquatting(self.typo_rta, self.package_input_name)
        print_user_dev_json(self.user_dev_rta, self.package_input_name)

    def export_json(self):
        extra = json.dumps(self.get_extra())
        generate_json(
            cve_json=self.cve_rta,
            metadata_json=list(self.metadata_rta),
            dangerous_function_json=list(self.dangerous_function_rta),
            analysis_bandit_json=self.analysis_code_rta,
            analysis_rubocop_json=self.analysis_code_rta,
            analysis_njsscan_json=self.analysis_code_rta,
            analysis_go_semgrep_json=self.analysis_code_rta,
            hash_files_json=self.hash_files_rta,
            extract_data_json=self.extract_data_rta,
            app_inspector_json=self.app_inspector_rta,
            typo_json=self.typo_rta,
            virus_total_json=self.virus_total_rta,
            user_dev_json=list(self.user_dev_rta),
            extra_json=extra,
        )
