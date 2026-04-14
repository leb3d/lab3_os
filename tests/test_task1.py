from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / 'src'
sys.path.insert(0, str(SRC_DIR))

import task1  # noqa: E402


def test_should_show_hidden_rules():
    assert task1.should_show('file.txt', False) is True
    assert task1.should_show('.hidden', False) is False
    assert task1.should_show('.hidden', True) is True


def test_list_directory_hides_hidden_files(tmp_path, capsys):
    (tmp_path / 'visible.txt').write_text('data', encoding='utf-8')
    (tmp_path / '.hidden.txt').write_text('secret', encoding='utf-8')

    result = task1.list_directory(
        str(tmp_path),
        show_all=False,
        long_format=False,
    )
    captured = capsys.readouterr()

    assert result == 0
    assert 'visible.txt' in captured.out
    assert '.hidden.txt' not in captured.out


def test_list_directory_shows_hidden_files(tmp_path, capsys):
    (tmp_path / 'visible.txt').write_text('data', encoding='utf-8')
    (tmp_path / '.hidden.txt').write_text('secret', encoding='utf-8')

    result = task1.list_directory(
        str(tmp_path),
        show_all=True,
        long_format=False,
    )
    captured = capsys.readouterr()

    assert result == 0
    assert 'visible.txt' in captured.out
    assert '.hidden.txt' in captured.out


def test_list_directory_returns_error_for_missing_path(capsys):
    result = task1.list_directory('missing_directory_for_test')
    captured = capsys.readouterr()

    assert result == 1
    assert 'directory not found' in captured.err
