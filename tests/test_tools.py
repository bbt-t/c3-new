from json import load as json_load
from zipfile import ZipFile

from pathlib import Path
from pytest import mark as pytest_mark

from app.tools import (
    extract_file_by_name_from_zip, extract_all_files_from_zip,
    load_file, parse_date, get_tail_executed_data
)

BASE_DIR_DATA = f'{Path(__file__).parent}/data'


def test_extract_file_by_name_from_zip_positive():
    extract_file_by_name_from_zip('doc2.json', f'{BASE_DIR_DATA}/test_extract.zip', BASE_DIR_DATA)
    file = Path(f'{BASE_DIR_DATA}/doc2.json')
    result = file.exists()
    file.unlink()
    assert result is True


def test_extract_all_files_from_zip_positive():
    extract_all_files_from_zip(f'{BASE_DIR_DATA}/test_extract.zip', BASE_DIR_DATA)
    zf = ZipFile(f'{BASE_DIR_DATA}/test_extract.zip').namelist()

    result = False
    for f in zf:
        file = Path(f'{BASE_DIR_DATA}/{f}')
        if not file.exists:
            break
        file.unlink()
    else:
        result = True

    assert result is True


@pytest_mark.parametrize(
    'path_to_file, expected_result', [
        (f'{BASE_DIR_DATA}/test_file.json', True),
        (f'{BASE_DIR_DATA}/test_file.txt', True),
    ]
)
def test_load_file_positive(path_to_file: str, expected_result):
    assert isinstance(load_file(path_to_file), list) == expected_result


@pytest_mark.parametrize(
    'string_date, date_format', [
        ('2018-06-30T02:08:58.425572', '%d.%m.%Y'),
        ('2018-06-30', '%d.%m.%Y'),
    ]
)
def test_parse_date_positive(string_date: str, date_format: str):
    assert isinstance(parse_date(string_date, date_format), str)


@pytest_mark.parametrize('to_take', [2, 3, 4, 5])
def test_get_tail_executed_data_positive(to_take):
    with open(f'{BASE_DIR_DATA}/test_operations.json') as f:
        data = json_load(f)
    result = get_tail_executed_data(data, to_take)
    assert isinstance(result, list) is True and len(result) == to_take
