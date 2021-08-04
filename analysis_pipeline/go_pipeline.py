
import sys
import json

from tqdm import tqdm
from zipfile import ZipFile
from analyzers.typosquatting import typo_local
from analyzers.cve_git import cve_git
from analyzers.hashfiles import get_hash_pkg
from analyzers.hashfiles import hash_files
from analyzers.datafiles import extract_data
from flask_server.run_server import generate_json
from analysis_pipeline.pipelines import ProcessPipeline
from console_prints.console_prints import print_semgrep_not_installed_error

from go_analyzers.godev import go_dev
from go_analyzers.gometadata import go_metadata
from go_analyzers.godownpackage import go_download

from external_analyzers.appinspector.appinspector_data import \
    appinspector_process
from external_analyzers.virustotal.virustotal_analysis import \
    virustotal_analysis
from external_analyzers.semgrep.semgrep \
    import semgrep_process


class GoProcessPipeline(ProcessPipeline):

    def get_packs(self, libraries):
        return json.loads(go_download(libraries))

    def get_typo_rta(self, typo_combinations):
        return '{}'
        # return typo_web('go', typo_combinations)

    def get_metadata(self, pack, files, pack_name, pkg_hash_id, local):
        return go_metadata(pack, pkg_hash_id, files, local, pack_name)

    def get_dangerous_functions(self, pack, files, pkg_hash_id):
        return '[]'

    def get_code_review(self, files):
        #return ''
        try:
            return semgrep_process(files)
        except OSError:
            print_semgrep_not_installed_error()
            return ''

    def get_files(self, pack):
        return ZipFile(pack, 'r')

    def get_extra(self):
        return 'go'

    def get_extra_cve(self):
        return 'go'

    def get_devs(self, pack_name):
        return go_dev(pack_name)


class AllPackagesGoProcess(ProcessPipeline):

    def __init__(self, libraries):
        self.libraries = libraries
        packs = self.get_packs(self.libraries)
        for pack in packs:
            self.path_pack.append(pack)

    def get_packs(self, libraries):
        return json.loads(go_download(libraries))

    def get_typo_rta(self, typo_combinations):
        return '{}'
        # return typo_web('go', typo_combinations)

    def get_metadata(self, pack, files, pack_name, pkg_hash_id, local=False):
        return go_metadata(pack, pkg_hash_id, files, pack_name)

    def get_dangerous_functions(self, pack, files, pkg_hash_id):
        return '[]'

    def get_files(self, pack):
        return ZipFile(pack, 'r')

    def get_extra(self):
        return 'go'

    def get_extra_cve(self):
        return 'go'

    def get_devs(self, pack_name):
        return go_dev(pack_name)

    def start_process_pipeline(self):
        self.__set_app_inspector_path()
        self.__set_virus_total_api_key()

        for pack in tqdm(self.path_pack, desc=' Processing packages...'):
            pkg_hashid = get_hash_pkg(pack)
            files = self.get_files(pack)

            metadata = self.get_metadata(pack, files, pkg_hashid)

            self.metadata_rta.append(metadata)

            version, name = self.__get_metadata_variables(metadata)

            """self.dangerous_function_rta.append(
                self.get_dangerous_functions(pack, files, pkg_hashid))"""
            self.analysis_code_rta.append(
                self.get_code_review(files))
            self.hash_files_rta.append(hash_files(pack, pkg_hashid, files))
            self.extract_data_rta.append(extract_data(pack, files, pkg_hashid))
            if self.app_inspector_path:
                self.app_inspector_rta.append(
                    appinspector_process(pack, files, self.app_inspector_path))
            self.cve_rta.append(cve_git(name, 'go', version))
            files.close()

            if self.virus_total_key:
                """
                if self.virustotal_key exists, execute virustotal_analysis
                """
                self.virus_total_rta.append(virustotal_analysis(
                    name, self.virus_total_key))

    def print_process_pipeline(self):
        extra = json.dumps(self.get_extra())
        generate_json(
            cve_json=self.cve_rta,
            metadata_json=self.metadata_rta,
            dangerous_function_json=self.dangerous_function_rta,
            analysis_go_semgrep_json=self.analysis_code_rta,
            hash_files_json=self.hash_files_rta,
            extract_data_json=self.extract_data_rta,
            app_inspector_json=self.app_inspector_rta,
            virus_total_json=self.virus_total_rta,
            extra_json=extra,
        )
        sys.exit()
