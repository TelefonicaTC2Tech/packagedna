
import json
import tarfile

from analyzers.typosquatting import typo_local
from console_prints.console_prints import print_rubocop_not_installed_error
from analysis_pipeline.pipelines import ProcessPipeline

from rb_analyzers.rbdev import rb_dev
from rb_analyzers.rbdowngems import rb_download
from rb_analyzers.rbmetadata import rb_metadata
from rb_analyzers.rbrubocop import rb_rubocop


class RubyProcessPipeline(ProcessPipeline):

    def get_packs(self, libraries):
        return json.loads(rb_download(libraries))

    def get_typo_rta(self, typo_combinations):
        return typo_local('rb', typo_combinations)

    def get_metadata(self, pack, files, pack_name, pkg_hash_id, local):
        return rb_metadata(pack, pkg_hash_id, files, local, pack_name)

    def get_dangerous_functions(self, pack, files, pkg_hash_id):
        return '[]'

    def get_code_review(self, files):
        try:
            return rb_rubocop(files)
        except OSError:
            print_rubocop_not_installed_error()
            return ''

    def get_files(self, pack):
        return tarfile.open(pack)

    def get_extra(self):
        return 'ruby'

    def get_extra_cve(self):
        return 'rubygems'

    def get_devs(self, pack_name):
        return rb_dev(pack_name)
