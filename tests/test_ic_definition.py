"""Tests for IC definitions"""

# pylint: disable=wrong-import-position,wrong-import-order

import sys
from typing import Type
sys.path.insert(0, '.') # Make VSCode happy...

from src.dppeeper.ic.ic_definition import ICDefinition
import pytest

def test_16L8_pin_names(pin_list_zif_map_16L8, pin_list_in_16L8, pin_list_io_16L8, pin_list_o_16L8):
    pin_names: list[str] = ICDefinition._build_pin_names(zif_map=pin_list_zif_map_16L8, clk_pins=[], in_pins=pin_list_in_16L8, io_pins=pin_list_io_16L8, o_pins=pin_list_o_16L8)
    assert ['I1', 'I2', 'I3', 'I4',
            'I5', 'I6', 'I7', 'I8',
            'I9', 'G', 'I11', 'O12',
            'IO13', 'IO14', 'IO15', 'IO16',
            'IO17', 'IO18', 'O19', 'P'] == pin_names
