from json import load as json_load
from zipfile import ZipFile

import pathlib
import pytest

from tools import (
    extract_file_by_name_from_zip, extract_all_files_from_zip,
    load_file, parse_date, get_tail_executed_data
)


def test_extract_file_by_name_from_zip_positive():
    extract_file_by_name_from_zip('doc2.json', 'data/test_extract.zip', 'data')
    file = pathlib.Path('data/doc2.json')
    result = file.exists()
    file.unlink()
    assert result is True


def test_extract_all_files_from_zip_positive():
    extract_all_files_from_zip('data/test_extract.zip', 'data')
    zf = ZipFile('data/test_extract.zip').namelist()

    result = False
    for f in zf:
        file = pathlib.Path(f"data/{f}")
        if not file.exists:
            break
        file.unlink()
    else:
        result = True

    assert result is True


@pytest.mark.parametrize(
    'path_to_file, expected_result', [
        ('data/test_file.json', True),
        ('data/test_file.txt', True),
    ]
)
def test_load_file_positive(path_to_file: str, expected_result):
    assert isinstance(load_file(path_to_file), list) == expected_result


@pytest.mark.parametrize(
    'string_date, date_format', [
        ('2018-06-30T02:08:58.425572', '%d.%m.%Y'),
        ('2018-06-30', '%d.%m.%Y'),
    ]
)
def test_parse_date_positive(string_date: str, date_format: str):
    assert isinstance(parse_date(string_date, date_format), str)


@pytest.mark.parametrize('to_take', [2, 3, 4, 5])
def test_get_tail_executed_data_positive(to_take):
    with open('data/test_operations.json') as f:
        data = json_load(f)
    result = get_tail_executed_data(data, to_take)
    assert isinstance(result, list) is True and len(result) == to_take