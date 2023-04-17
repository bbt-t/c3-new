from pathlib import Path

from config import FILE, ZIPFILE, DATE_FORMAT
from tools import extract_file_by_name_from_zip, load_file, get_tail_executed_data, sort_data_by_date, show_info

from click import command, option


@command()
@option("--file", default=FILE, help="data load file path")
@option("--arch", default=ZIPFILE, help="data load zip-archive file path")
def main(file: str, arch: str) -> None:
    """
    Point iof entry.
    """
    # file existence check
    if not Path(file).exists():
        print('extract zip-file')
        extract_file_by_name_from_zip(file, arch)

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
