from logging import error as log_err
from pathlib import Path

from config import FILE, ZIPFILE, DATE_FORMAT, BASE_DIR
from tools import extract_file_by_name_from_zip, load_file, get_tail_executed_data, sort_data_by_date, show_info

from click import command, option


# add CLI commands
@command()
@option("--file", default=FILE, help="data load file name")
@option("--arch", default=ZIPFILE, help="data load zip-archive file name")
def main(file: str, arch: str) -> None:
    """
    Point iof entry.
    """
    file_path = f"{BASE_DIR}{file}"

    # file existence check
    if not Path(file_path).exists():
        log_err('extract zip-file')
        extract_file_by_name_from_zip(file, f"{BASE_DIR}{arch}", BASE_DIR)

    # load file
    file_data = load_file(file_path)
    # take from end
    data = get_tail_executed_data(file_data)
    # sort by date
    sorted_data = sort_data_by_date(data)
    # output of results
    show_info(sorted_data, DATE_FORMAT)


if __name__ == '__main__':
    main()
