import sys

import yaml

APP_VETTING_PATH = sys.argv[1]
MARKDOWN_OUTPUT_PATH = sys.argv[2]

MARKDOWN_START = """<div class=3D"table-wrap">
<table class=3D"confluenceTable">
<tbody>
<tr>
<th class=3D"confluenceTh">manual check</th>
<th class=3D"confluenceTh">comment</th>
</tr>
"""

CHECK_MARKDOWN_TEMPLATE = """<tr>
<td class=3D"confluenceTh">{manual_check}</th>
<td class=3D"confluenceTh">{comment}</th>
</tr>
"""

MARKDOWN_END = """</tbody>
</table>
</div>"""


class ExportToMarkdown:
    """
    Based on app vetting file generates file with markdown consisting names of validated checks and comments.
    """

    def __init__(self, manual_checks_path, markdown_output_path):
        self.manual_checks_path = manual_checks_path
        self.markdown_output_path = markdown_output_path
        self.manual_checks = None

    def __call__(self):
        self._load_manual_checks()
        self._create_output_markup()

    def _load_manual_checks(self):
        with open(self.manual_checks_path) as vetting_data:
            self.manual_checks = yaml.safe_load(vetting_data)
        if self.manual_checks is None:
            self.manual_checks = {}

    def _create_output_markup(self):
        with open(self.markdown_output_path, "w") as output:
            output.write(MARKDOWN_START)
            for manual_check, check_attributes in self.manual_checks.items():
                output.write(
                    CHECK_MARKDOWN_TEMPLATE.format(
                        manual_check=manual_check, comment=check_attributes["comment"]
                    )
                )
            output.write(MARKDOWN_END)


def main():
    ExportToMarkdown(
        manual_checks_path=APP_VETTING_PATH, markdown_output_path=MARKDOWN_OUTPUT_PATH
    )()


if __name__ == "__main__":
    main()
