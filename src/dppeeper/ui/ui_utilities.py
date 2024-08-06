"""This module contains miscellaneous utilities for the UI"""

from typing import final, Tuple

from dppeeper.ic.ic_definition import ICDefinition

@final
class UIUtilities:
    @staticmethod
    def calculateGridSize(ic: ICDefinition) -> Tuple[int, int]:
        match len(ic.pins_per_side):
            case 1:
                return (4, ic.pins_per_side[0] + 2)
            case 2:
                return (8, max(ic.pins_per_side) + 2)
            case 3:
                top_bottom: list[int] = [val for (idx, val) in enumerate(ic.pins_per_side) if (idx % 2) == 0]
                left_right: list[int] = [val for (idx, val) in enumerate(ic.pins_per_side) if (idx % 2) == 1]
                return (max(top_bottom) + 6, max(left_right) + 6)