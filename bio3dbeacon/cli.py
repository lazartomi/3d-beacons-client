#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is the entry point for the command-line interface (CLI) application.

It can be used as a handy facility for running the task from a command line.

.. note::

    To learn more about Click visit the
    `project website <http://click.pocoo.org/5/>`_.  There is also a very
    helpful `tutorial video <https://www.youtube.com/watch?v=kNke39OZ2k0>`_.

    To learn more about running Luigi, visit the Luigi project's
    `Read-The-Docs <http://luigi.readthedocs.io/en/stable/>`_ page.

.. currentmodule:: bio3dbeacon.cli
.. moduleauthor:: Ian Sillitoe <i.sillitoe@ucl.ac.uk>
"""
import logging
import os
import pathlib
import uuid
import subprocess
import tempfile
import types

# pip
import click
import luigi
import requests

# local
from bio3dbeacon import __version__
from bio3dbeacon.app import flask_cli
from .tasks import ProcessModelPdb, get_uid_from_file
from .database import get_db
from .data_loader import swissmodel

from .tasks import ProcessModelPdb

LOGGING_LEVELS = {
    0: logging.NOTSET,
    1: logging.ERROR,
    2: logging.WARN,
    3: logging.INFO,
    4: logging.DEBUG,
}  #: a mapping of `verbose` option counts to logging levels

LOG = logging.getLogger(__name__)


class Info(object):
    """An information object to pass data between CLI functions."""

    def __init__(self):  # Note: This object must have an empty constructor.
        """Create a new instance."""
        self.verbose: int = 0
        self.root_dir: str = Path(__file__).parent.parent.resolve()
        self.molstar_github_url = 'https://github.com/molstar/molstar.git'
        self.molstar_dir = self.root_dir / 'molstar'
        self.app = create_app()


# pass_info is a decorator for functions that pass 'Info' objects.
#: pylint: disable=invalid-name
pass_info = click.make_pass_decorator(Info, ensure=True)


@click.group()
@click.option("--verbose", "-v", count=True, help="Enable verbose output.")
@pass_info
def cli(info: Info, verbose: int):
    """Run bio3d-beacon-cli."""
    # Use the verbosity count to determine the logging level...
    if verbose > 0:
        logging.basicConfig(
            level=LOGGING_LEVELS[verbose]
            if verbose in LOGGING_LEVELS
            else logging.DEBUG,
            format='%(message)s'
        )
        click.echo(
            click.style(
                f"Verbose logging is enabled. "
                f"(LEVEL={logging.getLogger().getEffectiveLevel()})",
                fg="yellow",
            )
        )
    info.verbose = verbose


@cli.group()
@pass_info
def db(_: Info):
    """Functions relating to the local database"""


@db.command()
@click.option('--commit', 'commit_flag', is_flag=True, default=False,
              help="Confirm that you want to make changes")
@pass_info
def init(info: Info, commit_flag):
    """Initialise the local database"""

    app = info.app
    with app.app_context():
        db = get_db()

        click.echo(f"Database: {db}")
        if commit_flag:
            click.echo(f"Initialising database ... ")
            init_db()
            click.echo("  ... done")
        else:
            click.echo("THIS COMMAND WILL DELETE ALL DATA IN YOUR DATABASE")
            click.echo(
                f"Run this command again with the '--commit' flag to go ahead and initialise this database")


@db.command()
@pass_info
def info(info: Info):
    """Provide information about the local database"""

    app = info.app
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']

    try:
        with app.app_context():
            db = get_db()
            click.echo(f"Database: {db}")
            model_count = ModelStructure.query.count()
            click.echo(f"MODELS: {model_count}")

    except Exception as err:
        click.echo(
            f"Failed to connect to database '{db_uri}': {err}")
        exit(1)


@cli.group()
@pass_info
def model(_: Info):
    """Functions relating to model files."""


@model.command('add')
@click.option('--type', 'loader_classname', type=str, default='swissmodel', required=True,
              help='type of loader to use')
@click.option('--jsonfile', required=True,
              help='input model JSON file')
@click.option('--workers', default=5,
              help='number of workers')
@pass_info
def add(info: Info, loader_classname, jsonfile, workers):
    """Add local models"""

    loader_module = __import__(
        f"bio3dbeacon.data_loader.{loader_classname}", fromlist=[''])

    if not isinstance(loader_module, types.ModuleType):
        raise ValueError(
            f"failed to find data_loader module called '{loader_classname}'")

    with app.app_context():
        db = get_db()

        click.echo(f'Working on JSON file: {jsonfile} ... ')
        structures = loader_module.create_model_structures(json_file=jsonfile)
        click.echo(f' ... found {len(structures)} structures')

        for str_count, structure in enumerate(structures, 1):
            db.session.add(structure)

            click.echo(
                f'Working on {pathlib.Path(jsonfile).name}, structure {str_count} ... ')

            coordinate_uri = structure.original_path
            structure.uid = uuid.uuid4()

            click.echo('Downloading coordinates: {}'.format(coordinate_uri))

            r = requests.get(coordinate_uri)

            tmp_pdb_file = tempfile.NamedTemporaryFile('wt', suffix='.pdb')
            tmp_pdb_file.write(r.text)
            tmp_pdb_file.flush()

            click.echo('Working on file: {}'.format(tmp_pdb_file.name))
            task = ProcessModelPdb(pdb_file=str(
                tmp_pdb_file.name), uid=structure.uid)
            try:
                luigi.build([task], workers=workers)
            except Exception as err:
                LOG.error('caught error: %s', err)
                raise

        LOG.info('Committing DB changes')
        db.session.commit()


@cli.command()
def version():
    """Get the library version."""
    click.echo(click.style(f"{__version__}", bold=True))
