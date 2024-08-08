"""Tests for UI Utilities"""

# pylint: disable=wrong-import-position,wrong-import-order

import sys
from typing import Type

import pytest

from dppeeper.ui.ui_utilities import UIUtilities

sys.path.insert(0, './src') # Make VSCode happy...

def test_grid_size_calculation():
    # SIP 12 pin IC
    assert UIUtilities.calculateGridSize([12]) == (4, 14)
    # DIP 20 pin IC (left and right pin count)
    assert UIUtilities.calculateGridSize([10, 10]) == (8, 12)
    # QUAD 48 pin (Left 14 + Bottom 10 + Right 14 + Top 10)
    assert UIUtilities.calculateGridSize([14, 10, 14, 10]) == (16, 20)

def test_SIP_grid_position_calculation():
    assert UIUtilities.calculatePinPosition(pin_no = 1, isLabel = False, pins_per_side = [10]) == (1, 1)
    assert UIUtilities.calculatePinPosition(pin_no = 1, isLabel = True, pins_per_side = [10]) == (2, 1)
    assert UIUtilities.calculatePinPosition(pin_no = 10, isLabel = False, pins_per_side = [10]) == (1, 10)
    assert UIUtilities.calculatePinPosition(pin_no = 10, isLabel = True, pins_per_side = [10]) == (2, 10)

    with pytest.raises(Exception) as e_info:
        UIUtilities.calculatePinPosition(pin_no = 11, isLabel = True, pins_per_side = [10])

    assert e_info.value.args[0] == 'Pin structure does not fit pin number 11. Max pin is 10.'

def test_DIP_grid_position_calculation():
    assert UIUtilities.calculatePinPosition(pin_no = 1, isLabel = False, pins_per_side = [10, 10]) == (1, 1)
    assert UIUtilities.calculatePinPosition(pin_no = 1, isLabel = True, pins_per_side = [10, 10]) == (2, 1)
    assert UIUtilities.calculatePinPosition(pin_no = 10, isLabel = False, pins_per_side = [10, 10]) == (1, 10)
    assert UIUtilities.calculatePinPosition(pin_no = 10, isLabel = True, pins_per_side = [10, 10]) == (2, 10)
    assert UIUtilities.calculatePinPosition(pin_no = 11, isLabel = False, pins_per_side = [10, 10]) == (6, 10)
    assert UIUtilities.calculatePinPosition(pin_no = 11, isLabel = True, pins_per_side = [10, 10]) == (5, 10)
    assert UIUtilities.calculatePinPosition(pin_no = 20, isLabel = False, pins_per_side = [10, 10]) == (6, 1)
    assert UIUtilities.calculatePinPosition(pin_no = 20, isLabel = True, pins_per_side = [10, 10]) == (5, 1)
    
    with pytest.raises(Exception) as e_info:
        UIUtilities.calculatePinPosition(pin_no = 21, isLabel = False, pins_per_side = [10, 10])

    assert e_info.value.args[0] == 'Pin structure does not fit pin number 21. Max pin is 20.'


                                        
    