# tests/test_pyls.py
import pytest
from pyls.main import list_directory

# Sample JSON data for testing
sample_data = {
    "name": "root",
    "size": 4096,
    "time_modified": 1699957865,
    "permissions": "drwxr-xr-x",
    "contents": [
        {
            "name": "LICENSE",
            "size": 1071,
            "time_modified": 1699941437,
            "permissions": "rw-r--r--",
        },
        {
            "name": "README.md",
            "size": 83,
            "time_modified": 1699941437,
            "permissions": "rw-r--r--",
        },
        {
            "name": "parser",
            "size": 4096,
            "time_modified": 1700205662,
            "permissions": "drwxr-xr-x",
            "contents": [
                {
                    "name": "parser.go",
                    "size": 1622,
                    "time_modified": 1700202950,
                    "permissions": "rw-r--r--",
                },
                {
                    "name": "parser_test.go",
                    "size": 1342,
                    "time_modified": 1700205662,
                    "permissions": "rw-r--r--",
                },
            ],
        },
    ],
}


def test_list_directory_root(capfd):
    # Test listing the root directory
    list_directory(sample_data, "", detailed=False)
    out, err = capfd.readouterr()
    assert "LICENSE README.md parser" in out


def test_list_directory_parser(capfd):
    # Test listing a subdirectory
    list_directory(sample_data, "parser", detailed=False)
    out, err = capfd.readouterr()
    assert "parser.go parser_test.go" in out


def test_list_file_in_parser(capfd):
    # Test listing a specific file
    list_directory(sample_data, "parser/parser.go", detailed=True)
    out, err = capfd.readouterr()
    assert "rw-r--r--" in out
    assert "1622" in out
    assert "parser.go" in out


def test_nonexistent_path(capfd):
    # Test for a non-existent path
    list_directory(sample_data, "nonexistent", detailed=False)
    out, err = capfd.readouterr()
    assert "\"cannot access 'nonexistent': No such file or directory\"\n" in out
