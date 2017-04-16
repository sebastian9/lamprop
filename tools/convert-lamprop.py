# file: convert-lamprop.py
# vim:fileencoding=utf-8:ft=python
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2017-04-16 10:38:30 +0200
# Last modified: 2017-04-16 15:16:41 +0200

"""Script to convert lamprop files from the old style fiber parameters
(E1, E2, v12, G12, cte1, cte2, density) to the new style parameters
(E1, ν12, α1, ρ)."""

import argparse
import logging
import sys
import shutil

_lic = '''To the extent possible under law, Roland Smith has waived all copyright and
related or neighboring rights to convert-lamprop.py. This work is published from the
Netherlands. See http://creativecommons.org/publicdomain/zero/1.0/'''


class LicenseAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print(_lic)
        sys.exit()


def readlines(path):
    """Read a file into a list of lines."""
    with open(path) as f:
        return f.readlines()


def oldstyle_fibers(lines):
    flines = ((num, ln) for num, ln in enumerate(lines) if
              ln.strip().startswith('f:'))
    oldstyle = []
    for num, ln in flines:
        items = ln.split()
        try:
            item5 = float(items[5])  # noqa
            oldstyle.append(num)
        except ValueError:
            # new style, do nothing
            pass
    return oldstyle


def changeline(ln):
    f, E1, _, v12, _, alpha1, _, rho, name = ln.split(maxsplit=8)
    return ' '.join([f, E1, v12, alpha1, rho, name])


def main(argv):
    # Process the command-line arguments
    opts = argparse.ArgumentParser(prog='convert-lamprop', description=__doc__)
    opts.add_argument('-L', '--license', action=LicenseAction, nargs=0,
                      help="print the license")
    opts.add_argument('--log', default='warning',
                      choices=['debug', 'info', 'warning', 'error'],
                      help="logging level (defaults to 'warning')")
    opts.add_argument("files", metavar='file', nargs='*',
                      help="one or more files to process")
    args = opts.parse_args(argv)
    logging.basicConfig(level=getattr(logging, args.log.upper(), None),
                        format='%(levelname)s: %(message)s')
    for path in args.files:
        if path[-4:] != '.lam':
            logging.error('{} is not a lamprop file; skipping'.format(path))
            continue
        try:
            lines = readlines(path)
            if not lines:
                raise IOError('empty file')
        except (FileNotFoundError, IOError) as e:
            logging.error('could not read {}: {}'.format(path, e))
            continue
        oldidx = oldstyle_fibers(lines)
        if oldidx:
            logging.info('found {} old style lines in {}'.format(len(oldidx), path))
            # Back up the file
            shutil.copyfile(path, path+'.orig')
            # Change the f-lines
            for n in oldidx:
                lines[n] = changeline(lines[n])
            # Write the file.
            with open(path, 'w') as f:
                f.writelines(lines)
        else:
            logging.info('skipping {}; no old style lines'.format(path))


if __name__ == '__main__':
    main(sys.argv[1:])
