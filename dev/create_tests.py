import pathlib
import re

from os import mkdir
from argparse import ArgumentParser


MODULE_NAME = 'storage'
FILE_SRC_DIR = pathlib.Path(__file__).parent
DEFAULT_TEST_DIR_PATH = FILE_SRC_DIR.parent.joinpath('tests')

METHOD_PATTERN = r'^\s*def\s[^_]+\w+\s*\(.*\)'


def create_test_directory(path):
    mkdir(path)

    init_py_path = pathlib.Path(path).joinpath('__init__.py')
    with open(init_py_path, 'x') as f:
        f.write('')


def test_dir_path_exists(test_dir_path) -> bool:
    path = pathlib.Path(test_dir_path)
    return path.exists() + path.is_dir()


def create_test_file(test_path, file_name, file_contents) -> pathlib.Path:
    path = pathlib.Path(file_name)
    test_path = pathlib.Path(test_path)
    test_path = test_path.joinpath(pathlib.Path(f"test_{path.name}.py"))

    with open(test_path, 'x') as f:
        f.write(file_contents)

    return test_path


def create_test_file_content_from_method_list(method_names: list[str]) -> str:
    content = ""

    for method in method_names:
        content += create_test_case_for_method(method)

    return content


def add_import_statement(class_name: str, class_file_path):
    content = f"from {MODULE_NAME}.{class_name.lower()} import {class_name}\n\n"
    return content


def create_test_case_for_method(method_name: str) -> str:
    header = f"\ndef test_{method_name}():\n"
    footer = "    raise Exception\n"
    return header + footer + "\n"


def find_methods_inside_class(filepath, class_name: str) -> list[str]:
    with open(filepath, 'r') as f:
        file_contents = f.readlines()

    methods: list[str] = []
    start_line_index = 0
    prev_line: str = ""

    # Find start of the class
    for index, line in enumerate(file_contents):
        if class_name:
            if f"class {class_name}" in line:
                start_line_index = index+1

    # Find public methods of this class
    for index, line in enumerate(file_contents[start_line_index::]):
        func_match = re.search(METHOD_PATTERN, line)
        if func_match:
            if "@" not in line and "@" not in prev_line:  # ignore property methods
                func_match = func_match.string
                func_name = get_method_name(func_match)
                methods.append(func_name)

        # Stop loop upon reaching end of the class
        if index == len(file_contents)-start_line_index-1:
            break
        if 'class' in line and prev_line == "\n":
            break

        prev_line = line

    methods = [method.strip() for method in methods]
    return methods


def get_method_name(func_str_match: str) -> str:
    func_name = func_str_match.replace('def', '')
    parenthesis_start = func_str_match.find('(')
    return func_name[:parenthesis_start-3:]


def parse_console_args(args: list[str]) -> dict:
    arg_parser = ArgumentParser(prog="Create tests",
                                description="Automatically create test file and test cases for each public method in "
                                            "selected class in target file.")
    arg_parser.add_argument('filepath',
                            metavar="Class File Path",
                            type=str)

    arg_parser.add_argument('class',
                            metavar="Class Name",
                            type=str)

    arg_parser.add_argument('--output',
                            metavar="Test Directory Path",
                            default=DEFAULT_TEST_DIR_PATH,
                            type=str)

    arg_parser.add_argument('--print',
                            help="Print info to the console.",
                            action='store_true',
                            default=False)

    parsed_args = arg_parser.parse_args(args).__dict__

    return parsed_args


def main(args: list[str] | None = None) -> int:
    parsed_args = parse_console_args(args)
    print_out_allowed: bool = parsed_args.get('print')

    class_file_path = parsed_args.get('filepath')
    class_name = parsed_args.get('class')
    test_dir_path = parsed_args.get('output')

    if not test_dir_path_exists(test_dir_path):
        create_test_directory(test_dir_path)
        if print_out_allowed:
            print("CREATE_TESTS: Test directory at target path does not exist")
            print(f"CREATE_TESTS: New test directory has been created at: {test_dir_path}")

    methods = find_methods_inside_class(class_file_path, class_name)
    test_file_contents = add_import_statement(class_name, class_file_path)
    test_file_contents += create_test_file_content_from_method_list(methods)
    out = create_test_file(test_dir_path, class_name.lower(), test_file_contents)

    if print_out_allowed:
        print(f"CREATE_TESTS: {out} created with {len(methods)} test methods")

    return 0


if __name__ == '__main__':
    SystemExit(main())
