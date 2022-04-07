import click
import yaml
import sqlite_utils
import json


@click.command()
@click.version_option()
@click.argument(
    "db_path", type=click.Path(file_okay=True, dir_okay=False, allow_dash=False)
)
@click.argument("table", type=str)
@click.argument("yaml_file", type=click.File())
@click.option("--pk", type=str, help="Column to use as a primary key")
@click.option(
    "--single-column",
    type=str,
    help="If YAML file is a list of values, populate this column",
)
@click.option("--loaddata", type=bool, help="Restore from a dump data file YAML Django")
def cli(db_path, table, yaml_file, pk, single_column, loaddata):
    "Convert YAML files to SQLite"
    db = sqlite_utils.Database(db_path)
    docs = yaml.safe_load(yaml_file)
    if single_column:
        if not isinstance(docs, list):
            raise click.ClickException(
                "If --single-column is provided input must be a YAML list"
            )
        docs = [{single_column: value} for value in docs]
        pk = single_column
    # We round-trip the docs to JSON to ensure anything unexpected
    # like date objects is converted to valid JSON values
    docs = json.loads(json.dumps(docs, default=str))
    if loaddata:
        # its recomendate for djanto test when you need data, but you use pipeline and need create new database
        for table in docs:
            table['fields'][pk if pk else 'id'] = table['pk']
            for field in table['fields']:
                try:
                    table['fields'][field] = float(table['fields'][field])
                except:
                    continue
            db[table['model'].split('.')[-1]].upsert(table['fields'], pk=pk if pk else 'id')
    elif pk:
        db[table].upsert_all(docs, pk=pk, alter=True)
    else:
        db[table].insert_all(docs, alter=True)
