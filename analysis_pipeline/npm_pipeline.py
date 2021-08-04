
import json
import tarfile

from analyzers.typosquatting import typo_local
from console_prints.console_prints import print_njsscan_not_installed_error
from analysis_pipeline.pipelines import ProcessPipeline

from npm_analyzers.npmdev import npm_dev
from npm_analyzers.npmdownjs import npm_download
from npm_analyzers.npmmetadata import npm_metadata
from npm_analyzers.npmjsscan import npm_njsscan

class NpmProcessPipeline(ProcessPipeline):

    def get_packs(self, libraries):
        return json.loads(npm_download(libraries))

    def get_typo_rta(self, typo_combinations):
        return typo_local('npm', typo_combinations)

    def get_metadata(self, pack, files, pack_name, pkg_hash_id, local):
        return npm_metadata(pack, pkg_hash_id, files, pack_name)

    def get_dangerous_functions(self, pack, files, pkg_hash_id):
        return '[]'

    def get_files(self, pack):
        return tarfile.open(pack)

    def get_devs(self, pack_name):
        return npm_dev(pack_name)

    def get_extra(self):
        return 'npm'

    def get_extra_cve(self):
        return 'npm'

    def get_code_review(self, files):
        try:
            return npm_njsscan(files)
        except OSError:
            print_njsscan_not_installed_error()
            return ''