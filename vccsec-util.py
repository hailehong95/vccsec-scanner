#!/usr/bin/env python

from utils.clean import clean_task
from utils.build import build_task
from utils.update import update_task
from utils.version import version_task
from utils.extract import extract_task
from utils.rsakey import rsa_key_task, keygen_task

import click


@click.group()
def cli():
    """A CLI Utility for VCCSEC Scanner"""
    pass


@cli.command(name='version', help='Show Utility version')
def version():
    version_task()


@cli.command(name='clean', help='Clean all temporary working files')
def clean():
    clean_task()


@cli.command(name='keygen', help='RSA keys Generator')
def keygen():
    keygen_task()


@cli.command(name='make', help='Create VCCSEC Scanner bundle')
def make():
    update_task()
    extract_task()
    rsa_key_task()


@cli.command(name='build', help='Build VCCSEC Scanner')
def build():
    update_task()
    extract_task()
    rsa_key_task()
    build_task()


if __name__ == '__main__':
    cli()
