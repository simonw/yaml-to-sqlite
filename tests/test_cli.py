from click.testing import CliRunner
from yaml_to_sqlite import cli
import sqlite_utils
import json
import textwrap


TEST_YAML = """
- name: datasette-cluster-map
  url: https://github.com/simonw/datasette-cluster-map
- name: datasette-vega
  url: https://github.com/simonw/datasette-vega
  nested_with_date:
  - title: Hello
    date: 2010-01-01
"""
EXPECTED = [
    {
        "name": "datasette-cluster-map",
        "url": "https://github.com/simonw/datasette-cluster-map",
        "nested_with_date": None,
    },
    {
        "name": "datasette-vega",
        "url": "https://github.com/simonw/datasette-vega",
        "nested_with_date": json.dumps([{"title": "Hello", "date": "2010-01-01"}]),
    },
]


def test_without_pk(tmpdir):
    db_path = tmpdir / "db.db"
    assert (
        0
        == CliRunner()
        .invoke(cli.cli, [str(db_path), "items", "-"], input=TEST_YAML)
        .exit_code
    )
    db = sqlite_utils.Database(str(db_path))
    assert EXPECTED == list(db["items"].rows)
    # Run it again should get double the rows
    CliRunner().invoke(cli.cli, [str(db_path), "items", "-"], input=TEST_YAML)
    assert EXPECTED + EXPECTED == list(db["items"].rows)


def test_with_pk(tmpdir):
    db_path = tmpdir / "db.db"
    assert (
        0
        == CliRunner()
        .invoke(cli.cli, [str(db_path), "items", "-", "--pk", "name"], input=TEST_YAML)
        .exit_code
    )
    db = sqlite_utils.Database(str(db_path))
    assert EXPECTED == list(db["items"].rows)
    # Run it again should get same number of rows
    CliRunner().invoke(cli.cli, [str(db_path), "items", "-"], input=TEST_YAML)
    assert EXPECTED == list(db["items"].rows)


def test_single_column(tmpdir):
    db_path = tmpdir / "db.db"
    test_yaml = "- One\n" "- Two\n" "- Three\n"
    assert (
        0
        == CliRunner()
        .invoke(
            cli.cli,
            [str(db_path), "numbers", "-", "--single-column", "name"],
            input=test_yaml,
        )
        .exit_code
    )
    db = sqlite_utils.Database(str(db_path))
    actual = list(db["numbers"].rows)
    assert actual == [{"name": "One"}, {"name": "Two"}, {"name": "Three"}]
    assert db["numbers"].pks == ["name"]


def test_alters_if_necessary(tmpdir):
    db_path = tmpdir / "db.db"
    assert (
        0
        == CliRunner()
        .invoke(cli.cli, [str(db_path), "items", "-"], input=TEST_YAML)
        .exit_code
    )
    more_input = textwrap.dedent(
        """
    - name: some-other-thing
      new_column: A new column
    """
    )
    assert (
        0
        == CliRunner()
        .invoke(cli.cli, [str(db_path), "items", "-"], input=more_input)
        .exit_code
    )
    db = sqlite_utils.Database(str(db_path))
    assert db["items"].columns_dict == {
        "name": str,
        "url": str,
        "nested_with_date": str,
        "new_column": str,
    }
