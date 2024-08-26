"""Tests for IC definitions"""

# pylint: disable=wrong-import-position,wrong-import-order

import sys
from typing import Type
sys.path.insert(0, './src') # Make VSCode happy...

from dppeeper.ic.ic_definition import ICDefinition
import pytest

def test_16L8_pin_names(pin_list_zif_map_16L8, pin_list_in_16L8, pin_list_io_16L8, pin_list_o_16L8):
    pin_names: list[str] = ICDefinition._build_pin_names(zif_map=pin_list_zif_map_16L8, clk_pins=[], in_pins=pin_list_in_16L8, io_pins=pin_list_io_16L8, o_pins=pin_list_o_16L8, q_pins=[], oe_h_pins=[], oe_l_pins=[])
    assert ['I1', 'I2', 'I3', 'I4',
            'I5', 'I6', 'I7', 'I8',
            'I9', 'G', 'I11', 'O12',
            'IO13', 'IO14', 'IO15', 'IO16',
            'IO17', 'IO18', 'O19', 'P'] == pin_names
    
def test_16L8_pin_names_override(pin_list_zif_map_16L8, pin_list_in_16L8, pin_list_io_16L8, pin_list_o_16L8):
    pin_names: list[str] = ICDefinition._build_pin_names(zif_map=pin_list_zif_map_16L8, clk_pins=[], in_pins=pin_list_in_16L8, io_pins=pin_list_io_16L8, o_pins=pin_list_o_16L8, q_pins=[], oe_h_pins=[], oe_l_pins=[], pin_names_override=['', '', 'test', 'blargh', '', 'bofh'])
    assert ['I1', 'I2', 'test', 'blargh',
            'I5', 'bofh', 'I7', 'I8',
            'I9', 'G', 'I11', 'O12',
            'IO13', 'IO14', 'IO15', 'IO16',
            'IO17', 'IO18', 'O19', 'P'] == pin_names

def test_PAL16L8_Definition(ic_definition_PAL16L8):
    assert len(ic_definition_PAL16L8.pin_names) == 20
    assert len(ic_definition_PAL16L8.zif_map) == len(ic_definition_PAL16L8.pin_names)
    assert ic_definition_PAL16L8.in_pins == [1, 2, 3, 4, 5, 6, 7, 8, 9, 11]
    assert ic_definition_PAL16L8.o_pins == [12, 19]
    assert ic_definition_PAL16L8.io_pins == [13, 14, 15, 16, 17, 18]
    assert ic_definition_PAL16L8.clk_pins == []
    assert ic_definition_PAL16L8.hw_model == 3
