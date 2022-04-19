#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for `pycdsl.shell`"""

# https://pypi.org/project/cmd2-ext-test/

import pytest
import cmd2_ext_test

from cmd2 import CommandResult

from pycdsl.shell import CDSLShell

###############################################################################


class TestShell(cmd2_ext_test.ExternalTestMixin, CDSLShell):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


@pytest.fixture(scope="package")
def sample_shell(default_path, installation_list):
    shell = TestShell(data_dir=default_path, dict_ids=installation_list)
    shell.fixture_setup()
    yield shell
    shell.fixture_teardown()

###############################################################################


def test_set(sample_shell):
    sample_shell.app_cmd("set input_scheme iast")
    assert sample_shell.input_scheme == "iast"
    sample_shell.app_cmd("set input_scheme something-invalid")
    assert sample_shell.input_scheme == "iast"
    sample_shell.app_cmd("set output_scheme itrans")
    assert sample_shell.output_scheme == "itrans"
    sample_shell.app_cmd("set output_scheme something-invalid")
    assert sample_shell.output_scheme == "itrans"
    sample_shell.app_cmd("set search_mode value")
    assert sample_shell.search_mode == "value"
    sample_shell.app_cmd("set search_mode something-invalid")
    assert sample_shell.search_mode == "value"
    sample_shell.app_cmd("set limit 10")
    assert sample_shell.limit == 10
    sample_shell.app_cmd("set limit abc")
    assert sample_shell.limit == 10
    sample_shell.app_cmd("set limit -1")
    assert sample_shell.limit is None


def test_use(sample_shell):
    output = sample_shell.app_cmd("use WIL")
    assert isinstance(output, CommandResult)
    assert str(output.stdout).strip() == "Using 1 dictionaries: ['WIL']"

    output = sample_shell.app_cmd("use --none")
    assert isinstance(output, CommandResult)
    assert str(output.stdout).strip() == "Using 0 dictionaries: []"


###############################################################################
