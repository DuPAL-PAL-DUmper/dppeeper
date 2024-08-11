"""Contains the class that defines the connections of an IC"""

from typing import final

@final
class ICDefinition:
    _SUPPORTED_NUM_SIDES: list[int] = [1, 2, 4]

    name: str
    pins_per_side: list[int]
    
    zif_map: list[int]

    pin_names: list[str]

    clk_pins: list[int]
    in_pins: list[int]
    io_pins: list[int]
    o_pins: list[int]
    f_pins: list[int]

    adapter_hi_pins: list[int]
    hw_model: int
    adapter_notes: str | None = None

    @staticmethod
    def _remap_pin_array(zif_map: list[int], pins: list[int]) -> list[int]:
        remapped: list[int] = []

        for pin in pins:
            remapped.append(zif_map[pin - 1]) # Remember that pin numbering is 1-based

        return remapped

    @staticmethod
    def _build_pin_names(zif_map: list[int], in_pins: list[int], io_pins: list[int], o_pins: list[int], clk_pins: list[int]) -> list[str]:
        pin_names: list[str] = [('P' if pin == 42 else ('G' if pin == 21 else '')) for pin in zif_map]

        for pin in in_pins:
            pin_names[pin-1] = f'I{pin}'

        for pin in o_pins:
            pin_names[pin-1] = f'O{pin}'
        
        for pin in io_pins:
            pin_names[pin-1] = f'IO{pin}'
        
        for pin in clk_pins:
            if len(pin_names[pin-1]) > 0:
                pin_names[pin-1] = pin_names[pin-1] + '/CLK'

        return pin_names

    def __init__(self,
                 name: str, 
                 pins_per_side: list[int], 
                 zif_map: list[int],
                 clk_pins: list[int],
                 in_pins: list[int],
                 io_pins: list[int],
                 o_pins: list[int],
                 f_pins: list[int],
                 adapter_hi_pins: list[int],
                 hw_model: int,
                 adapter_notes: str | None = None):
        
        self.name = name
        self.pins_per_side = pins_per_side
        self.zif_map = zif_map
        self.hw_model = hw_model
        self.adapter_notes = adapter_notes
        self.adapter_hi_pins = adapter_hi_pins

        self.pin_names = self._build_pin_names(zif_map, in_pins, io_pins, o_pins, clk_pins)

        # Check the package
        tot_pins: int = sum(self.pins_per_side)
        if tot_pins != len(self.pin_names):
            raise ValueError(f'Number of pins in name list {len(self.pin_names)} does not match pins in package ({tot_pins})')
        if len(self.pins_per_side) not in self._SUPPORTED_NUM_SIDES:
            raise ValueError(f'Number of sides {len(self.pins_per_side)} is not supported.')

        self.clk_pins = clk_pins
        self.in_pins = in_pins
        self.io_pins = io_pins
        self.o_pins = o_pins
        self.f_pins = f_pins

