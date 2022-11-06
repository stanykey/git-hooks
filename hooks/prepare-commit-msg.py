#!/usr/bin/python3
from subprocess import check_output
from sys import argv


def run(commit_msg_filepath: str) -> None:
    branch_name = check_output(['git', 'symbolic-ref', '--short', 'HEAD']).decode('utf-8').strip()
    template_content = ('<component>: <short description>\n', '<long description>\n', branch_name)
    with open(commit_msg_filepath, 'r+', encoding='utf-8') as file:
        original_content = file.readlines()
        if original_content[0]:
            # first line isn't empty, so it's ammend or -m/-t or something like it
            return

        file.seek(0, 0)
        file.writelines(template_content)
        file.writelines(original_content)


if __name__ == '__main__':
    run(argv[1])
