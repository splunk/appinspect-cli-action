import sys

import yaml

APP_VETTING_PATH = sys.argv[1]
MARKDOWN_OUTPUT_PATH = sys.argv[2]

MARKDOWN_START = """<div class=3D"table-wrap">
<table class=3D"confluenceTable">
<tbody>
<tr>
<th class=3D"confluenceTh">check</th>
<th class=3D"confluenceTh">comment</th>
</tr>
"""

CHECK_MARKDOWN_TEMPLATE = """<tr>
<td class=3D"confluenceTh">{check}</th>
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

    def __init__(self, checks_path, markdown_output_path):
        self.checks_path = checks_path
        self.markdown_output_path = markdown_output_path
        self.checks = None

    def __call__(self):
        self._load_checks()
        self._create_output_markup()

    def _load_checks(self):
        with open(self.checks_path) as vetting_data:
            self.checks = yaml.safe_load(vetting_data)
        if self.checks is None:
            self.checks = {}

    def _create_output_markup(self):
        with open(self.markdown_output_path, "w") as output:
            output.write(MARKDOWN_START)
            for check, check_attributes in self.checks.items():
                output.write(
                    CHECK_MARKDOWN_TEMPLATE.format(
                        check=check, comment=check_attributes["comment"]
                    )
                )
            output.write(MARKDOWN_END)


def main():
    ExportToMarkdown(
        checks_path=APP_VETTING_PATH, markdown_output_path=MARKDOWN_OUTPUT_PATH
    )()


if __name__ == "__main__":
    main()
