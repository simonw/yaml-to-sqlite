import sqlite3

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
@click.option("--pk-legacy", type=str, help="Column to use as a primary key legacy tables")
@click.option(
    "--single-column",
    type=str,
    help="If YAML file is a list of values, populate this column",
)
@click.option("--loaddata", type=bool, help="Restore from a dump data file YAML Django")
@click.option("--exclude", type=str, help="Prevents specific models, you can use name1, name2, name3")
@click.option(
    "--legacy-table",
    type=str,
    help="Set legacy table name, for not created tables with name app_table, you can use name1, name2, name3"
)
def cli(db_path, table, yaml_file, pk, pk_legacy, single_column, loaddata, legacy_table, exclude):
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
            if exclude:
                if table['model'].split('.')[-1] in exclude.split(","):
                    continue
            for field in table['fields']:
                try:
                    if table['fields'][field].replace('.', '').isdigit():
                        table['fields'][field] = float(table['fields'][field])
                except:
                    continue
            if legacy_table:
                for legacy in legacy_table.split(','):
                    if legacy == table['model'].split('.')[0]:
                        table['fields'][pk_legacy if pk_legacy else 'id'] = table['pk']
                        db[table['model'].split('.')[-1]].upsert(table['fields'], pk=pk_legacy if pk_legacy else 'id')
                    else:
                        table['fields'][pk if pk else 'id'] = table['pk']
                        while True:
                            try:
                                db[table['model'].replace('.', '_')].insert(table['fields'], pk=pk if pk else 'id')
                                break
                            except sqlite3.OperationalError as e:
                                column = str(e).split()[-1].strip()
                                if type(table['fields'][column]) == list:
                                    table['fields'].pop(column)
                                else:
                                    table['fields'][f"{column}_id"] = table['fields'][column]
                                    table['fields'].pop(column)
                                try:
                                    db[table['model'].replace('.', '_')].insert(table['fields'], pk=pk if pk else 'id')
                                    break
                                except sqlite3.OperationalError:
                                    pass
            else:
                db[table['model'].replace('.', '_')].upsert(table['fields'], pk=pk if pk else 'id')
    elif pk:
        db[table].upsert_all(docs, pk=pk, alter=True)
    else:
        db[table].insert_all(docs, alter=True)
