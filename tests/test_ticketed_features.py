"""A growing set of tests designed to ensure when isort implements a feature described in a ticket
it fully works as defined in the associated ticket.
"""
from io import StringIO

import pytest

import isort
from isort import Config


def test_semicolon_ignored_for_dynamic_lines_after_import_issue_1178():
    """Test to ensure even if a semicolon is in the decorator in the line following an import
    the correct line spacing detrmination will be made.
    See: https://github.com/timothycrosley/isort/issues/1178.
    """
    assert isort.check_code(
        """
import pytest


@pytest.mark.skip(';')
def test_thing(): pass
""",
        show_diff=True,
    )


def test_isort_automatically_removes_duplicate_aliases_issue_1193():
    """Test to ensure isort can automatically remove duplicate aliases.
    See: https://github.com/timothycrosley/isort/issues/1281
    """
    assert isort.check_code("from urllib import parse as parse\n", show_diff=True)
    assert (
        isort.code("from urllib import parse as parse", remove_redundant_aliases=True)
        == "from urllib import parse\n"
    )
    assert isort.check_code("import os as os\n", show_diff=True)
    assert isort.code("import os as os", remove_redundant_aliases=True) == "import os\n"


def test_isort_enables_floating_imports_to_top_of_module_issue_1228():
    """Test to ensure isort will allow floating all non-indented imports to the top of a file.
    See: https://github.com/timothycrosley/isort/issues/1228.
    """
    assert (
        isort.code(
            """
import os


def my_function_1():
    pass

import sys

def my_function_2():
    pass
""",
            float_to_top=True,
        )
        == """
import os
import sys


def my_function_1():
    pass


def my_function_2():
    pass
"""
    )

    assert (
        isort.code(
            """
import os


def my_function_1():
    pass

# isort: split
import sys

def my_function_2():
    pass
""",
            float_to_top=True,
        )
        == """
import os


def my_function_1():
    pass

# isort: split
import sys


def my_function_2():
    pass
"""
    )


assert (
    isort.code(
        """
import os


def my_function_1():
    pass

# isort: off
import b
import a
def y():
    pass

# isort: on
import b

def my_function_2():
    pass

import a
""",
        float_to_top=True,
    )
    == """
import os


def my_function_1():
    pass

# isort: off
import b
import a
def y():
    pass

# isort: on
import a
import b


def my_function_2():
    pass
"""
)


def test_isort_provides_official_api_for_diff_output_issue_1335():
    """Test to ensure isort API for diff capturing allows capturing diff without sys.stdout.
    See: https://github.com/timothycrosley/isort/issues/1335.
    """
    diff_output = StringIO()
    isort.code("import b\nimport a\n", show_diff=diff_output)
    diff_output.seek(0)
    assert "+import a" in diff_output.read()


def test_isort_warns_when_known_sections_dont_match_issue_1331():
    """Test to ensure that isort warns if there is a mismatch between sections and known_sections.
    See: https://github.com/timothycrosley/isort/issues/1331.
    """
    assert (
        isort.place_module(
            "bot_core",
            config=Config(
                known_robotlocomotion_upstream=["bot_core"],
                sections=["ROBOTLOCOMOTION_UPSTREAM", "THIRDPARTY"],
            ),
        )
        == "ROBOTLOCOMOTION_UPSTREAM"
    )
    with pytest.warns(UserWarning):
        assert (
            isort.place_module(
                "bot_core",
                config=Config(
                    known_robotlocomotion_upstream=["bot_core"],
                    sections=["ROBOTLOOMOTION_UPSTREAM", "THIRDPARTY"],
                ),
            )
            == "THIRDPARTY"
        )
    with pytest.warns(UserWarning):
        assert (
            isort.place_module(
                "bot_core", config=Config(known_robotlocomotion_upstream=["bot_core"])
            )
            == "THIRDPARTY"
        )
