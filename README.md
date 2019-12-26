# yaml-to-sqlite

[![PyPI](https://img.shields.io/pypi/v/yaml-to-sqlite.svg)](https://pypi.org/project/yaml-to-sqlite/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/yaml-to-sqlite/blob/master/LICENSE)

```
$ yaml-to-sqlite --help
Usage: yaml-to-sqlite [OPTIONS] DB_PATH TABLE YAML_FILE

  Convert YAML files to SQLite

Options:
  --version  Show the version and exit.
  --pk TEXT
  --help     Show this message and exit.
```

For example:

    yaml-to-sqlite animals.db dogs dogs.yaml
