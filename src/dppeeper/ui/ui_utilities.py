"""This module contains miscellaneous utilities for the UI"""

from enum import Enum
from typing import final, Tuple

class UIPinGridType(Enum):
    PIN_NUM = 0
    CHECKBOX = 1
    LABEL = 2


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
            case _:
                raise ValueError(f'Number of sides {len(pins_per_side)} is not supported')

    @staticmethod    
    def calculatePinPosition(pin_no: int, type: UIPinGridType, pins_per_side: list[int], rot_shift: int = 0) -> Tuple[int, int]:
        grid_size: Tuple[int, int] = UIUtilities.calculateGridSize(pins_per_side)
        tot_pins: int = sum(pins_per_side)

        if pin_no < 1:
            raise ValueError('Pin numbering begins at 1')

        if pin_no > tot_pins:
            raise ValueError(f'Pin structure does not fit pin number {pin_no}. Max pin is {tot_pins}.')

        # We implement the rotation by simply subtracting or adding to the original pin number
        pin_no = pin_no + rot_shift
        if pin_no < 1:
            pin_no = tot_pins + pin_no
        elif pin_no > tot_pins:
            pin_no = pin_no - tot_pins

        shift: int = 0 if type == UIPinGridType.LABEL else (1 if type == UIPinGridType.CHECKBOX else 2)
        match len(pins_per_side):
            case 1:
                    return (1 + shift, pin_no)
            case 2:
                height: int = grid_size[1]
                if pin_no > pins_per_side[0]: # Right side
                    pos: int = (height - 1) - (pin_no - pins_per_side[0])
                    return (5 + shift, pos)
                else: # Left side
                    return (2 - shift, pin_no)
            case 4:
                if pin_no > pins_per_side[0] + pins_per_side[1] + pins_per_side[2]: # Top side
                    top_pin_no: int = pin_no - pins_per_side[0] - pins_per_side[1] - pins_per_side[2]
                    return ((grid_size[0] - 3) - top_pin_no, 2 - shift)
                elif pin_no > pins_per_side[0] + pins_per_side[1]: # Right side
                    right_pin_no: int = pin_no - pins_per_side[0] - pins_per_side[1]
                    return (grid_size[0] - 3 + shift, (grid_size[1] - 3) - right_pin_no)
                elif pin_no > pins_per_side[0]: # Bottom side
                    bottom_pin_no: int = pin_no - pins_per_side[0]
                    return (2 + bottom_pin_no, pins_per_side[0] + 3 + shift)
                else: # Left side
                    return (2 - shift, 2 + pin_no)
            case _:
                raise ValueError(f'Unsupported number of sides {len(pins_per_side)}')
