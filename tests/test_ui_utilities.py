"""Tests for UI Utilities"""

# pylint: disable=wrong-import-position,wrong-import-order

import sys
from typing import Type

from dppeeper.ui.ui_utilities import UIUtilities

sys.path.insert(0, './src') # Make VSCode happy...

def test_DIP_Grid_calculation(ic_definition_PAL16L8):
    assert UIUtilities.calculateGridSize(ic_definition_PAL16L8) == (8, 12)