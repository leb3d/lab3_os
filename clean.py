#!/usr/bin/env python3
import argparse
import os
import sys


def parse_args():
    parser = argparse.ArgumentParser(
        prog='clean',
        description='Find and optionally delete empty files and directories.',
    )
    parser.add_argument(
        'wd',
        nargs='?',
        default='.',
        help='Working directory to inspect. Default: current directory.',
    )
    parser.add_argument(
        '--files',
        action='store_true',
        help='Show empty files only.',
    )
    parser.add_argument(
        '--dirs',
        action='store_true',
        help='Show empty directories only.',
    )
    parser.add_argument(
        '--delete-files',
        action='store_true',
        help='Delete found empty files.',
    )
    parser.add_argument(
        '--delete-dirs',
        action='store_true',
        help='Delete found empty directories.',
    )
    return parser.parse_args()


def find_empty_files(root_path):
    empty_files = []
    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            path = os.path.join(dirpath, filename)
            try:
                if os.path.islink(path):
                    continue
                if os.path.isfile(path) and os.path.getsize(path) == 0:
                    empty_files.append(path)
            except OSError:
                continue
    empty_files.sort()
    return empty_files


def find_empty_dirs(root_path):
    empty_dirs = []
    for dirpath, dirnames, filenames in os.walk(root_path, topdown=False):
        if dirpath == root_path:
            if not dirnames and not filenames:
                empty_dirs.append(dirpath)
            continue
        try:
            if not os.listdir(dirpath):
                empty_dirs.append(dirpath)
        except OSError:
            continue
    empty_dirs.sort()
    return empty_dirs


def delete_files(paths):
    errors = 0
    for path in paths:
        try:
            os.remove(path)
            print(f'Removed file: {path}')
        except OSError as error:
            print(f'Cannot remove file {path}: {error}', file=sys.stderr)
            errors += 1
    return errors


def delete_dirs(paths, root_path):
    errors = 0
    root_path = os.path.normpath(os.path.abspath(root_path))

    for path in sorted(paths, key=lambda value: value.count(os.sep), reverse=True):
        normalized_path = os.path.normpath(os.path.abspath(path))
        if normalized_path == root_path:
            print(
                f'Cannot remove starting directory: {path}',
                file=sys.stderr,
            )
            errors += 1
            continue
        try:
            os.rmdir(path)
            print(f'Removed directory: {path}')
        except OSError as error:
            print(f'Cannot remove directory {path}: {error}', file=sys.stderr)
            errors += 1
    return errors


def print_section(title, paths):
    print(title)
    if paths:
        for path in paths:
            print(path)
    else:
        print('Not found')


def resolve_actions(args):
    show_files = args.files
    show_dirs = args.dirs
    delete_files_flag = args.delete_files
    delete_dirs_flag = args.delete_dirs

    if not any((show_files, show_dirs, delete_files_flag, delete_dirs_flag)):
        show_files = True
        show_dirs = True

    return show_files, show_dirs, delete_files_flag, delete_dirs_flag


def main():
    args = parse_args()

    if not os.path.exists(args.wd):
        print(f'Error: path not found: {args.wd}', file=sys.stderr)
        raise SystemExit(1)
    if not os.path.isdir(args.wd):
        print(f'Error: not a directory: {args.wd}', file=sys.stderr)
        raise SystemExit(1)

    show_files, show_dirs, delete_files_flag, delete_dirs_flag = resolve_actions(args)

    empty_files = find_empty_files(args.wd)
    empty_dirs = find_empty_dirs(args.wd)
    status = 0

    if show_files:
        print_section('Empty files:', empty_files)
    if show_dirs:
        print_section('Empty directories:', empty_dirs)

    if delete_files_flag:
        status = 1 if delete_files(empty_files) else status
    if delete_dirs_flag:
        status = 1 if delete_dirs(empty_dirs, args.wd) else status

    raise SystemExit(status)


if __name__ == '__main__':
    main()
