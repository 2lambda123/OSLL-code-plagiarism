import subprocess
from pathlib import Path
from typing import List, Literal, Optional, Union

from codeplag.consts import UTIL_NAME
from codeplag.types import Flag

SUCCESS_CODE = 0


def run_cmd(cmd: List[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, stdout=subprocess.PIPE)


def run_util(
    cmd: List[str],
    root: Optional[Literal["check", "settings"]] = None
) -> subprocess.CompletedProcess:
    command = [] if root is None else [root]
    return run_cmd([UTIL_NAME] + command + cmd)


def run_check(cmd: List[str], extension: str = 'py') -> subprocess.CompletedProcess:
    return run_util(['--extension', extension] + cmd, root="check")


def modify_settings(
    reports: Optional[Union[Path, str]] = None,
    environment: Optional[Union[Path, str]] = None,
    threshold: Optional[int] = None,
    show_progress: Optional[Flag] = None
) -> subprocess.CompletedProcess:
    reports_opt = ['--reports', str(reports)] if reports else []
    environment_opt = ['--environment', str(environment)] if environment else []
    threshold_opt = ['--threshold', str(threshold)] if threshold else []
    show_progress_opt = ['--show_progress', str(show_progress)] if show_progress is not None else []

    return run_util(
        ['modify'] + reports_opt + environment_opt + threshold_opt + show_progress_opt,
        root='settings'
    )


def show_settings() -> subprocess.CompletedProcess:
    return run_util(['show'], root='settings')
