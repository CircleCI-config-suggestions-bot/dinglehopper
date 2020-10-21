import json
import os

import click
from ocrd import Processor
from ocrd.decorators import ocrd_cli_options, ocrd_cli_wrap_processor
from ocrd_utils import getLogger, make_file_id, assert_file_grp_cardinality
from pkg_resources import resource_string

from .cli import process as cli_process
from .edit_distance import levenshtein_matrix_cache_clear

OCRD_TOOL = json.loads(resource_string(__name__, 'ocrd-tool.json').decode('utf8'))


@click.command()
@ocrd_cli_options
def ocrd_dinglehopper(*args, **kwargs):
    return ocrd_cli_wrap_processor(OcrdDinglehopperEvaluate, *args, **kwargs)


class OcrdDinglehopperEvaluate(Processor):

    def __init__(self, *args, **kwargs):
        kwargs['ocrd_tool'] = OCRD_TOOL['tools']['ocrd-dinglehopper']
        super(OcrdDinglehopperEvaluate, self).__init__(*args, **kwargs)

    def process(self):
        assert_file_grp_cardinality(self.input_file_grp, 2, 'GT and OCR')
        assert_file_grp_cardinality(self.output_file_grp, 1)

        log = getLogger('processor.OcrdDinglehopperEvaluate')

        metrics = self.parameter['metrics']
        textequiv_level = self.parameter['textequiv_level']
        gt_grp, ocr_grp = self.input_file_grp.split(',')
        for n, page_id in enumerate(self.workspace.mets.physical_pages):
            gt_file = next(self.workspace.mets.find_files(fileGrp=gt_grp, pageId=page_id))
            ocr_file = next(self.workspace.mets.find_files(fileGrp=ocr_grp, pageId=page_id))
            gt_file = self.workspace.download_file(gt_file)
            ocr_file = self.workspace.download_file(ocr_file)
            log.info("INPUT FILES %i / %s↔ %s", n, gt_file, ocr_file)

            file_id = make_file_id(ocr_file, self.output_file_grp)
            report_prefix = os.path.join(self.output_file_grp, file_id)

            # Process the files
            try:
                os.mkdir(self.output_file_grp)
            except FileExistsError:
                pass
            cli_process(
                    gt_file.local_filename,
                    ocr_file.local_filename,
                    report_prefix,
                    metrics=metrics,
                    textequiv_level=textequiv_level
            )

            # Add reports to the workspace
            for report_suffix, mimetype in \
                    [
                        ['.html', 'text/html'],
                        ['.json', 'application/json']
                    ]:
                self.workspace.add_file(
                     ID=file_id + report_suffix,
                     file_grp=self.output_file_grp,
                     pageId=page_id,
                     mimetype=mimetype,
                     local_filename=report_prefix + report_suffix)

            # Clear cache between files
            levenshtein_matrix_cache_clear()


if __name__ == '__main__':
    ocrd_dinglehopper()
