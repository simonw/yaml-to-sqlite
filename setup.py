from setuptools import setup, find_packages
import io
import os

VERSION = "1.0"


def get_long_description():
    with io.open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="yaml-to-sqlite",
    description="Utility for converting YAML files to SQLite",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    version=VERSION,
    license="Apache License, Version 2.0",
    packages=find_packages(),
    install_requires=["click", "PyYAML", "sqlite-utils>=3.9.1"],
    setup_requires=["pytest-runner"],
    extras_require={"test": ["pytest"]},
    entry_points="""
        [console_scripts]
        yaml-to-sqlite=yaml_to_sqlite.cli:cli
    """,
    tests_require=["yaml-to-sqlite[test]"],
    url="https://github.com/simonw/yaml-to-sqlite",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
