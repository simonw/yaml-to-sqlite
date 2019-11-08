import click
import yaml
import sqlite_utils


@click.command()
@click.version_option()
@click.argument(
    "db_path", type=click.Path(file_okay=True, dir_okay=False, allow_dash=False)
)
@click.argument("table", type=str)
@click.argument("yaml_file", type=click.File())
@click.option("--pk", type=str, help="Column to use as a primary key")
def cli(db_path, table, yaml_file, pk):
    "Covert YAML files to SQLite"
    db = sqlite_utils.Database(db_path)
    db[table].upsert_all(yaml.safe_load(yaml_file), pk=pk)
