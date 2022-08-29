import json
import os
import re
import shutil
from contextlib import suppress

import pytest
from utils import SUCCESS_CODE, run_util

from codeplag.consts import UTIL_NAME, UTIL_VERSION
from codeplag.types import WorksReport

CPP_FILES = [
    'test/unit/codeplag/cplag/data/sample1.cpp',
    'test/unit/codeplag/cplag/data/sample2.cpp'
]
PY_FILES = [
    'src/codeplag/pyplag/astwalkers.py',
    'setup.py'
]
CPP_DIR = 'test/unit/codeplag/cplag/data'
PY_DIR = 'test/unit/codeplag/cplag'
REPO_URL = 'https://github.com/OSLL/code-plagiarism'
REPORTS_FOLDER = os.path.abspath('./reports')
CPP_GITHUB_FILES = [
    f'{REPO_URL}/blob/main/test/unit/codeplag/cplag/data/sample3.cpp',
    f'{REPO_URL}/blob/main/test/unit/codeplag/cplag/data/sample4.cpp'
]
PY_GITHUB_FILES = [
    f'{REPO_URL}/blob/main/src/codeplag/pyplag/utils.py',
    f'{REPO_URL}/blob/main/setup.py'
]
CPP_GITHUB_DIR = f'{REPO_URL}/tree/main/test'
PY_GITHUB_DIR = f'{REPO_URL}/blob/main/src/codeplag/pyplag'


def test_check_util_version():
    result = run_util(['--version'])

    assert result.returncode == SUCCESS_CODE
    assert f'{UTIL_NAME} {UTIL_VERSION}' in result.stdout.decode('utf-8')


@pytest.mark.parametrize(
    "cmd, out",
    [
        (['--files', *CPP_FILES], b'Getting works features from files'),
        (
            ['--directories', CPP_DIR],
            f'Getting works features from {CPP_DIR}'.encode('utf-8')
        ),
        (
            ['--github-files', *CPP_GITHUB_FILES],
            b'Getting works features from GitHub urls'
        ),
        (
            ['--github-project-folders', CPP_GITHUB_DIR],
            f'Getting works features from {CPP_GITHUB_DIR}'.encode('utf-8')
        ),
        (
            ['--github-user', 'OSLL', '--regexp', 'code-plag'],
            f'Getting works features from {REPO_URL}'.encode('utf-8')
        )
    ]
)
def test_compare_cpp_files(cmd, out):
    result = run_util(
        cmd,
        ext='cpp'
    )

    assert result.returncode == SUCCESS_CODE
    assert out in result.stdout


@pytest.mark.parametrize(
    "cmd, out",
    [
        (['--files', *PY_FILES], b'Getting works features from files'),
        (
            ['--directories', PY_DIR],
            f'Getting works features from {PY_DIR}'.encode('utf-8')
        ),
        (
            ['--github-files', *PY_GITHUB_FILES],
            b'Getting works features from GitHub urls'
        ),
        (
            ['--github-project-folders', PY_GITHUB_DIR],
            f'Getting works features from {PY_GITHUB_DIR}'.encode('utf-8')
        ),
        (
            ['--github-user', 'OSLL', '--regexp', 'code-plag'],
            f'Getting works features from {REPO_URL}'.encode('utf-8')
        )
    ]
)
def test_compare_py_files(cmd, out):
    result = run_util(cmd)

    assert result.returncode == SUCCESS_CODE
    assert out in result.stdout


def test_save_reports():
    with suppress(Exception):
        os.mkdir(REPORTS_FOLDER)
    assert os.path.exists(REPORTS_FOLDER)

    run_util(
        ['--directories', './test', '--reports_directory', REPORTS_FOLDER]
    )
    reports_files = os.listdir(REPORTS_FOLDER)

    assert len(reports_files) > 0
    for file in reports_files:
        assert re.search('.*[.]json$', file)
        filepath = f'{REPORTS_FOLDER}/{file}'
        with open(filepath, 'r') as f:
            report = json.loads(f.read())
            for key in WorksReport.__annotations__.keys():
                assert key in report

    shutil.rmtree(REPORTS_FOLDER)
