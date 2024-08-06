"""Fixtures for testing"""

# pylint: disable=wrong-import-position

import sys
sys.path.insert(1, '.') # Make VSCode happy...

import pytest

# Fixtures for pin mapping
@pytest.fixture
def pin_list_zif_map_16L8() -> list[int]:
    return [3, 4, 5, 6, 7, 8, 9, 10, 11, 21, 31, 32, 33, 34, 35, 36, 37, 38, 39, 42]

@pytest.fixture
def pin_list_in_16L8() -> list[int]:
    return [1, 2, 3, 4, 5, 6, 7, 8, 9, 11]

@pytest.fixture
def pin_list_io_16L8() -> list[int]:
    return [13, 14, 15, 16, 17, 18]

@pytest.fixture
def pin_list_o_16L8() -> list[int]:
    return [12, 19]