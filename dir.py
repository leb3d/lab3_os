#!/usr/bin/env python3
import argparse
import grp
import os
import pwd
import stat
import sys
from datetime import datetime


def parse_args():
    parser = argparse.ArgumentParser(
        prog='dir',
        description='Show directory contents.',
    )
    parser.add_argument(
        'wd',
        nargs='?',
        default='.',
        help='Working directory to inspect. Default: current directory.',
    )
    parser.add_argument(
        '-l', '--long',
        action='store_true',
        help='Show detailed information for each entry.',
    )
    parser.add_argument(
        '-a', '--all',
        action='store_true',
        help='Show hidden entries except . and ..',
    )
    return parser.parse_args()


def format_mtime(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%b %d %H:%M')


def get_owner_name(uid):
    try:
        return pwd.getpwuid(uid).pw_name
    except KeyError:
        return str(uid)


def get_group_name(gid):
    try:
        return grp.getgrgid(gid).gr_name
    except KeyError:
        return str(gid)


def format_long_entry(entry):
    info = entry.stat(follow_symlinks=False)
    permissions = stat.filemode(info.st_mode)
    owner = get_owner_name(info.st_uid)
    group = get_group_name(info.st_gid)
    mtime = format_mtime(info.st_mtime)
    return (
        f'{permissions} '
        f'{info.st_nlink:2} '
        f'{owner} '
        f'{group} '
        f'{info.st_size:8} '
        f'{mtime} '
        f'{entry.name}'
    )


def should_show(name, show_all):
    if not show_all and name.startswith('.'):
        return False
    return True


def list_directory(path, show_all=False, long_format=False):
    try:
        with os.scandir(path) as entries:
            items = [entry for entry in entries if should_show(entry.name, show_all)]
    except FileNotFoundError:
        print(f'Error: directory not found: {path}', file=sys.stderr)
        return 1
    except NotADirectoryError:
        print(f'Error: not a directory: {path}', file=sys.stderr)
        return 1
    except PermissionError:
        print(f'Error: permission denied: {path}', file=sys.stderr)
        return 1
    except OSError as error:
        print(f'Error: cannot read directory {path}: {error}', file=sys.stderr)
        return 1

    items.sort(key=lambda entry: entry.name)
    status = 0

    for entry in items:
        if long_format:
            try:
                print(format_long_entry(entry))
            except OSError as error:
                print(
                    f'Error: cannot access entry {entry.name}: {error}',
                    file=sys.stderr,
                )
                status = 1
        else:
            print(entry.name)

    return status


def main():
    args = parse_args()
    raise SystemExit(
        list_directory(args.wd, show_all=args.all, long_format=args.long)
    )


if __name__ == '__main__':
    main()
