"""Tests for UI Utilities"""

# pylint: disable=wrong-import-position,wrong-import-order

import sys
from typing import Type

from dppeeper.ui.ui_utilities import UIUtilities

sys.path.insert(0, './src') # Make VSCode happy...

def test_DIP_Grid_calculation():
    # SIP 12 pin IC
    assert UIUtilities.calculateGridSize([12]) == (4, 14)
    # DIP 20 pin IC (left and right pin count)
    assert UIUtilities.calculateGridSize([10, 10]) == (8, 12)
    # QUAD 48 pin (Left 14 + Bottom 10 + Right 14 + Top 10)
    assert UIUtilities.calculateGridSize([14, 10, 14, 10]) == (16, 20)
    