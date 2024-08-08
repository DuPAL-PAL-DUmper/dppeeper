"""This module contains miscellaneous utilities for the UI"""

from typing import final, Tuple

from dppeeper.ic.ic_definition import ICDefinition

@final
class UIUtilities:
    @staticmethod
    def calculateGridSize(pins_per_side: list[int]) -> Tuple[int, int]:
        match len(pins_per_side):
            case 1:
                return (4, pins_per_side[0] + 2)
            case 2:
                return (8, max(pins_per_side) + 2)
            case 4:
                top_bottom: list[int] = [val for (idx, val) in enumerate(pins_per_side) if (idx % 2) == 1]
                left_right: list[int] = [val for (idx, val) in enumerate(pins_per_side) if (idx % 2) == 0]
                return (max(top_bottom) + 6, max(left_right) + 6)
            
        def calculatePinPosition(pin_no: int, isLabel: bool, pins_per_side: list[int], grid_size: Tuple[int, int]) -> Tuple[int, int]:
            match len(pins_per_side):
                case 1:
                    return (1 + (0 if isLabel else 1), pin_no)
                case 2:
                    height: int = grid_size[1]
                    
                    if pin_no > pins_per_side[0]: # Right side
                        pos: int = (height - 1) - (pin_no - pins_per_side[0]) 
                        return (5 + (1 if isLabel else 0), pos)
                    else: # Left side
                        return (2 - (1 if isLabel else 0), pin_no)
                case 4:
                    if pin_no > pins_per_side[0] + pins_per_side[1] + pins_per_side[2]: # Top side
                        top_pin_no: int = pin_no - pins_per_side[0] - pins_per_side[1] - pins_per_side[2]
                        return ((grid_size[0] - 3) - top_pin_no, 2 - (1 if isLabel else 0))
                    elif pin_no > pins_per_side[0] + pins_per_side[1]: # Right side
                        right_pin_no: int = pin_no - pins_per_side[0] - pins_per_side[1]
                        return (grid_size[0] - 3 + (1 if isLabel else 0), (grid_size[1] - 3) - right_pin_no)
                    elif pin_no > pins_per_side[0]: # Bottom side
                        bottom_pin_no: int = pin_no - pins_per_side[0]
                        return (3 + bottom_pin_no, pins_per_side[0] + 2 + (1 if isLabel else 0))
                    else: # Left side
                        return (1 + (0 if isLabel else 1), 3 + pin_no)
