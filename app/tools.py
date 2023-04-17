from json import load as json_load
from zipfile import ZipFile

from dateutil.parser import parse as date_parse
from more_itertools import grouper


def extract_all_files_from_zip(archive_name: str, extract_to: str = None) -> None:
    """
    Extract all files from zip-archive.
    :param archive_name: zip-archive name
    :param extract_to: path to extract
    """
    with ZipFile(archive_name) as f:
        f.extractall(extract_to)


def extract_file_by_name_from_zip(file_name: str, zip_file_name: str, extract_to: str = 'data') -> None:
    """
    Extract file from zip-archive.
    :param file_name: file name in zip-archive
    :param zip_file_name: zip-archive name
    :param extract_to: path to extract
    :return:
    """
    with ZipFile(zip_file_name) as f:
        f.extract(file_name, extract_to)


def load_file(file_path: str) -> list[dict, ...]:
    """
    Load file.
    :param file_path: file path
    :return: json loads file
    """
    with open(file_path, 'rb') as f:  # 'rb' - mode for compatibility (Win)
        return json_load(f)


def parse_date(string_date: str, date_format: str = '%d.%m.%Y') -> str:
    """
    Parse date from string and output in the correct format.
    :param string_date: date in string expression
    :param date_format: date format
    :return: datetime in the correct format
    """
    return date_parse(string_date).strftime(date_format)


def get_tail_executed_data(data: list[dict, ...], to_take: int = 5) -> list[dict, ...]:
    """
    Gets data from the end of the list.
    :param data: load data
    :param to_take: how many
    :return: part data
    """
    part_data, count = [], 0

    for item in data[::-1]:
        if count == to_take:
            break
        if item['state'] == 'EXECUTED':
            part_data.append(item)
            count += 1
    return part_data


def sort_data_by_date(data: list[dict, ...]) -> list[dict, ...]:
    """
    Sorting data by date.
    :param data: loaded data
    :return: sorted data
    """
    return sorted(data, key=lambda x: date_parse(x['date']), reverse=True)


def get_transactions_info(data: dict[int | str]) -> tuple[str, str, str, str]:
    """
    Gets information about transactions.
    :param data: load date
    :return: from whom and to whom
    """
    try:
        name_card_from, card_from = data['from'].split()
        secure_card_from = ' '.join(
            ''.join(x) for x in grouper(
                f"{card_from[:6]}{'*' * (len(card_from) - 10)}{card_from[-4:]}",
                4,
            )
        )
    except KeyError:
        name_card_from, secure_card_from = 'Информация о счете', 'отсутствует'

    name_card_to, card_to = data['to'].split()
    secure_card_to = ''.join(f"**{card_to[1][-4:]}")

    return name_card_from, secure_card_from, name_card_to, secure_card_to


def show_info(data: list[dict, ...], date_format: str) -> None:
    """
    Show information.
    :param data: loads data
    :param date_format: time format
    """
    for item in data:
        date = parse_date(item['date'], date_format)
        transactions_info = get_transactions_info(item)
        operation_amount = item['operationAmount']

        print(
            f"{date} {item['description']}",
            "{} {} -> {} {}".format(*transactions_info),
            f"{operation_amount['amount']} {operation_amount['currency']['name']}",
            sep='\n',
            end='\n\n',
        )
