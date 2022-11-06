#!/usr/bin/python3
from enum import Enum
from pathlib import Path
from shutil import copy
from typing import Protocol
from platform import system


class TermColor(Enum):
    Off = "\033[0m"
    Red = "\033[1;31m"
    Green = "\033[1;32m"

    def __str__(self) -> str:
        return str(self.value)


def print_with_color(color: TermColor, message: str) -> None:
    print(f'{color}Info: {message}{TermColor.Off}')


def print_info(message: str) -> None:
    print_with_color(TermColor.Green, message)


def print_error(message: str) -> None:
    print_with_color(TermColor.Red, message)


class Platform(Protocol):
    @classmethod
    def install_hook(cls, hook: Path, destination: Path) -> None:
        """Install hook for git"""


class Windows:
    HOOK_TEMPLATE = '\n'.join([
        '#!/bin/sh',
        'COMMIT_MSG_FILE=$1',
        'python .git/hooks/prepare-commit-msg.py "$COMMIT_MSG_FILE"',
    ])

    @classmethod
    def install_hook(cls, hook: Path, destination: Path) -> None:
        copy(src=hook, dst=destination.parent / hook.name)
        cls.__create_hook_file(destination)

    @classmethod
    def __create_hook_file(cls, filename: Path) -> None:
        with open(filename, 'w', encoding='utf-8') as file:
            file.writelines(cls.HOOK_TEMPLATE)
            file.write('\n')


class Linux:
    @classmethod
    def install_hook(cls, hook: Path, destination: Path) -> None:
        copy(src=hook, dst=destination)
        destination.chmod(0o711)  # owner can do anything; others can only execute


def get_platform() -> Platform:
    print_info(f'Script is running of {system()} OS')
    return Windows() if system() == 'Windows' else Linux()


def run() -> None:
    working_dir = Path(__file__).parent.absolute()
    source_hook_dir = working_dir / 'hooks'
    if not source_hook_dir.is_dir():
        print_error(f'hooks directory is missed')
        return

    destination_hook_dir = working_dir / '.git' / 'hooks'
    if not destination_hook_dir.is_dir():
        print_error(f'.git directory is absent')
        return

    platform = get_platform()
    for hook in source_hook_dir.glob('*.py'):
        destination = destination_hook_dir / hook.stem
        print_info(f'Installing {str(hook.relative_to(working_dir))} -> {str(destination.relative_to(working_dir))}')

        platform.install_hook(hook, destination)


if __name__ == '__main__':
    run()
