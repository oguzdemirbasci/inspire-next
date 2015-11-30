# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2014, 2015 CERN.
#
# INSPIRE is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# INSPIRE is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with INSPIRE; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""Version number.

This file is imported by ``invenio.__init__``, and parsed by ``setup.py``.

Respect the following format: major, minor, patch, ..., "dev"?, revision?
- major, minor, patch are numbers starting at zero.
- you can put as much sub version as you need before 'dev'
- dev has to be set in development mode (non-release).
- revision can be set if you want to override the date coming from git.

See the tests.

(This is taken from Invenio repository)
"""

import datetime

import subprocess


version = (2, 0, 1, 'dev', 20141107094016)


def build_version(*args):
    """
    Build a PEP440 compatible version based on a list of arguments.

    Inspired by Django's django.utils.version
    """
    if 'dev' in args:
        pos = args.index('dev')
    else:
        pos = len(args)

    def zero_search(acc, x):
        """Increment the counter until it stops seeing zeros."""
        position, searching = acc
        if searching:
            if x != 0:
                searching = False
            else:
                position += 1

        return (position, searching)

    last_zero = pos + 1 - reduce(zero_search, reversed(args[:pos]), (1, True))[0]
    parts = max(2, last_zero)
    version = '.'.join(str(arg) for arg in args[:parts])

    if len(args) > pos:
        revision = args[pos + 1] if len(args) > pos + 1 else git_revision()
        version += '.dev{0}'.format(revision)

    return version


def git_revision():
    """Get the timestamp of the latest git revision."""
    if not hasattr(git_revision, '_cache'):
        call = subprocess.Popen(r'git log -1 --pretty=format:%ct --quiet HEAD',
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, shell=True)
        stdout, _ = call.communicate()
        try:
            timestamp = int(stdout.decode())
            ts = datetime.datetime.utcfromtimestamp(timestamp)
            revision = ts.strftime('%Y%m%d%H%M%S')
        except ValueError:
            revision = '0'

        git_revision._cache = revision

    return git_revision._cache


__version__ = build_version(*version)
