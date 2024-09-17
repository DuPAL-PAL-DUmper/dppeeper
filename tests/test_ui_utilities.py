"""Tests for UI Utilities"""

# pylint: disable=wrong-import-position,wrong-import-order

import sys

import pytest

from dppeeper.ui.ui_utilities import UIUtilities, UIPinGridType

sys.path.insert(0, './src') # Make VSCode happy...

def test_grid_size_calculation():
    # SIP 12 pin IC
    assert UIUtilities.calculateGridSize([12]) == (4, 14)
    # DIP 20 pin IC (left and right pin count)
    assert UIUtilities.calculateGridSize([10, 10]) == (8, 12)
    # QUAD 48 pin (Left 14 + Bottom 10 + Right 14 + Top 10)
    assert UIUtilities.calculateGridSize([14, 10, 14, 10]) == (16, 20)

def test_SIP_grid_position_calculation():
    assert UIUtilities.calculatePinPosition(pin_no = 1, type = UIPinGridType.CHECKBOX, pins_per_side = [10]) == (2, 1)
    assert UIUtilities.calculatePinPosition(pin_no = 1, type = UIPinGridType.LABEL, pins_per_side = [10]) == (1, 1)
    assert UIUtilities.calculatePinPosition(pin_no = 10, type = UIPinGridType.CHECKBOX, pins_per_side = [10]) == (2, 10)
    assert UIUtilities.calculatePinPosition(pin_no = 10,  type = UIPinGridType.LABEL, pins_per_side = [10]) == (1, 10)

    with pytest.raises(Exception) as e_info:
        UIUtilities.calculatePinPosition(pin_no = 11, type = UIPinGridType.LABEL, pins_per_side = [10])

    assert e_info.value.args[0] == 'Pin structure does not fit pin number 11. Max pin is 10.'

def test_DIP_grid_position_calculation():
    assert UIUtilities.calculatePinPosition(pin_no = 1, type = UIPinGridType.CHECKBOX, pins_per_side = [10, 10]) == (1, 1)
    assert UIUtilities.calculatePinPosition(pin_no = 1, type = UIPinGridType.LABEL, pins_per_side = [10, 10]) == (2, 1)
    assert UIUtilities.calculatePinPosition(pin_no = 10, type = UIPinGridType.CHECKBOX, pins_per_side = [10, 10]) == (1, 10)
    assert UIUtilities.calculatePinPosition(pin_no = 10, type = UIPinGridType.LABEL, pins_per_side = [10, 10]) == (2, 10)
    assert UIUtilities.calculatePinPosition(pin_no = 11, type = UIPinGridType.CHECKBOX, pins_per_side = [10, 10]) == (6, 10)
    assert UIUtilities.calculatePinPosition(pin_no = 11, type = UIPinGridType.LABEL, pins_per_side = [10, 10]) == (5, 10)
    assert UIUtilities.calculatePinPosition(pin_no = 20, type = UIPinGridType.CHECKBOX, pins_per_side = [10, 10]) == (6, 1)
    assert UIUtilities.calculatePinPosition(pin_no = 20, type = UIPinGridType.LABEL, pins_per_side = [10, 10]) == (5, 1)
    
    with pytest.raises(Exception) as e_info:
        UIUtilities.calculatePinPosition(pin_no = 21, type = UIPinGridType.CHECKBOX, pins_per_side = [10, 10])

    assert e_info.value.args[0] == 'Pin structure does not fit pin number 21. Max pin is 20.'

def test_QUAD_grid_position_calculation():
    # Left
    assert UIUtilities.calculatePinPosition(pin_no = 1, type = UIPinGridType.CHECKBOX, pins_per_side = [14, 10, 14, 10]) == (1, 3)
    assert UIUtilities.calculatePinPosition(pin_no = 14, type = UIPinGridType.CHECKBOX, pins_per_side = [14, 10, 14, 10]) == (1, 16)
    assert UIUtilities.calculatePinPosition(pin_no = 1, type = UIPinGridType.LABEL, pins_per_side = [14, 10, 14, 10]) == (2, 3)
    assert UIUtilities.calculatePinPosition(pin_no = 14, type = UIPinGridType.LABEL, pins_per_side = [14, 10, 14, 10]) == (2, 16)
    
    # Right
    assert UIUtilities.calculatePinPosition(pin_no = 25, type = UIPinGridType.CHECKBOX, pins_per_side = [14, 10, 14, 10]) == (14, 16)
    assert UIUtilities.calculatePinPosition(pin_no = 25, type = UIPinGridType.LABEL, pins_per_side = [14, 10, 14, 10]) == (13, 16)
    assert UIUtilities.calculatePinPosition(pin_no = 38, type = UIPinGridType.CHECKBOX, pins_per_side = [14, 10, 14, 10]) == (14, 3)
    assert UIUtilities.calculatePinPosition(pin_no = 38, type = UIPinGridType.LABEL, pins_per_side = [14, 10, 14, 10]) == (13, 3)

    # Bottom
    assert UIUtilities.calculatePinPosition(pin_no = 15, type = UIPinGridType.CHECKBOX, pins_per_side = [14, 10, 14, 10]) == (3, 18)
    assert UIUtilities.calculatePinPosition(pin_no = 15, type = UIPinGridType.LABEL, pins_per_side = [14, 10, 14, 10]) == (3, 17)
    assert UIUtilities.calculatePinPosition(pin_no = 24, type = UIPinGridType.CHECKBOX, pins_per_side = [14, 10, 14, 10]) == (12, 18)
    assert UIUtilities.calculatePinPosition(pin_no = 24, type = UIPinGridType.LABEL, pins_per_side = [14, 10, 14, 10]) == (12, 17)
    
    # Top
    assert UIUtilities.calculatePinPosition(pin_no = 39, type = UIPinGridType.CHECKBOX, pins_per_side = [14, 10, 14, 10]) == (12, 1)
    assert UIUtilities.calculatePinPosition(pin_no = 39, type = UIPinGridType.LABEL, pins_per_side = [14, 10, 14, 10]) == (12, 2)
    assert UIUtilities.calculatePinPosition(pin_no = 48, type = UIPinGridType.CHECKBOX, pins_per_side = [14, 10, 14, 10]) == (3, 1)
    assert UIUtilities.calculatePinPosition(pin_no = 48, type = UIPinGridType.LABEL, pins_per_side = [14, 10, 14, 10]) == (3, 2)

def test_grid_position_rotation_calculation():
    assert UIUtilities.calculatePinPosition(pin_no = 1, type = UIPinGridType.CHECKBOX, pins_per_side = [14, 10, 14, 10], rot_shift=1) == (1, 4)
    assert UIUtilities.calculatePinPosition(pin_no = 14, type = UIPinGridType.CHECKBOX, pins_per_side = [14, 10, 14, 10], rot_shift=1) == (3, 18)
    assert UIUtilities.calculatePinPosition(pin_no = 1, type = UIPinGridType.LABEL, pins_per_side = [14, 10, 14, 10], rot_shift=1) == (2, 4)
    assert UIUtilities.calculatePinPosition(pin_no = 14, type = UIPinGridType.LABEL, pins_per_side = [14, 10, 14, 10], rot_shift=1) == (3, 17)

    assert UIUtilities.calculatePinPosition(pin_no = 1, type = UIPinGridType.CHECKBOX, pins_per_side = [14, 10, 14, 10], rot_shift=-1) == (3, 1)
    assert UIUtilities.calculatePinPosition(pin_no = 14, type = UIPinGridType.CHECKBOX, pins_per_side = [14, 10, 14, 10], rot_shift=-1) == (1, 15)
    assert UIUtilities.calculatePinPosition(pin_no = 1, type = UIPinGridType.LABEL, pins_per_side = [14, 10, 14, 10], rot_shift=-1) == (3, 2)
    assert UIUtilities.calculatePinPosition(pin_no = 14, type = UIPinGridType.LABEL, pins_per_side = [14, 10, 14, 10], rot_shift=-1) == (2, 15)