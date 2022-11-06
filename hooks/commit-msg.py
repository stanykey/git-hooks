#!/usr/bin/python3
from re import match as regex_match
from subprocess import check_output
from sys import argv, exit

COMMIT_MESSAGE_PATTERN = r'^(?P<component>\w+): (?P<short>\w+)\n\n(?P<long>(.*\s)+)(?P<task>[A-Z]{2,}-[0-9]+)$'
ERROR_MESSAGE = '\n'.join([
    'Commit message format must match pattern:',
    '<component>: <short description>\n',
    '<long description>\n',
    '<BRANCH NAME (JIRA TASK ID)>'
])

RED_COLOR = "\033[1;31m"
BLUE_COLOR = "\033[1;34m"
YELLOW_COLOR = "\033[1;33m"


def run(commit_msg_filepath: str) -> None:
    with open(commit_msg_filepath, 'r', encoding='utf-8') as file:
        commit_message = ''.join(filter(lambda line: not line.startswith('#'), file.readlines())).strip()

    match = regex_match(COMMIT_MESSAGE_PATTERN, commit_message)
    if not match:
        print(RED_COLOR + "Bad commit: " + BLUE_COLOR + commit_message)
        print(YELLOW_COLOR + ERROR_MESSAGE)
        print("commit-msg hook failed (add --no-verify to bypass)")
        exit(1)
    print(match.groupdict())

    branch_name = check_output(['git', 'symbolic-ref', '--short', 'HEAD']).decode('utf-8').strip()
    if not commit_message.endswith(branch_name.upper()):
        print(RED_COLOR + "Branch name doesn't match with JIRA TASK ID")
        exit(1)


if __name__ == '__main__':
    run(argv[1])
