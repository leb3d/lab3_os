from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / 'src'
sys.path.insert(0, str(SRC_DIR))

import task2  # noqa: E402


def test_find_empty_files_finds_only_empty_files(tmp_path):
    empty_file = tmp_path / 'empty.txt'
    nonempty_file = tmp_path / 'data.txt'

    empty_file.touch()
    nonempty_file.write_text('data', encoding='utf-8')

    result = task2.find_empty_files(str(tmp_path))

    assert str(empty_file) in result
    assert str(nonempty_file) not in result


def test_find_empty_dirs_finds_only_empty_directories(tmp_path):
    empty_dir = tmp_path / 'empty_dir'
    nonempty_dir = tmp_path / 'nonempty_dir'

    empty_dir.mkdir()
    nonempty_dir.mkdir()
    (nonempty_dir / 'file.txt').write_text('data', encoding='utf-8')

    result = task2.find_empty_dirs(str(tmp_path))

    assert str(empty_dir) in result
    assert str(nonempty_dir) not in result


def test_delete_files_removes_empty_file(tmp_path):
    empty_file = tmp_path / 'empty.txt'
    empty_file.touch()

    errors = task2.delete_files([str(empty_file)])

    assert errors == 0
    assert not empty_file.exists()


def test_delete_dirs_removes_empty_directory(tmp_path):
    empty_dir = tmp_path / 'empty_dir'
    empty_dir.mkdir()

    errors = task2.delete_dirs([str(empty_dir)], str(tmp_path))

    assert errors == 0
    assert not empty_dir.exists()