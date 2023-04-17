from pathlib import Path
from tools import extract_file_by_name_from_zip, load_file, get_tail_executed_data, sort_data_by_date, show_info


FILE = 'operations.json'
ZIPFILE = 'data/operations.zip'
DATE_FORMAT = '%d.%m.%Y'


def main():
    # file existence check
    if not Path('operations.json').exists():
        print('extract zip-file')
        extract_file_by_name_from_zip(FILE, ZIPFILE)

    # load file
    file_data = load_file(FILE)
    # take from end
    data = get_tail_executed_data(file_data)
    # sort by date
    sorted_data = sort_data_by_date(data)
    # output of results
    show_info(sorted_data, DATE_FORMAT)


if __name__ == '__main__':
    main()
