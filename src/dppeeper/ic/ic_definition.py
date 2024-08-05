"""Contains the class that defines the connections of an IC"""

from typing import final

from dppeeper.ic.ic_package_types import ICPackageType

@final
class ICDefinition:
    name: str
    package: ICPackageType

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

    def __init__(self,
                 name: str, 
                 package: ICPackageType, 
                 zif_map: list[int],
                 pin_names: list[str],
                 clk_pins: list[int],
                 in_pins: list[int],
                 io_pins: list[int],
                 o_pins: list[int],
                 f_pins: list[int],
                 adapter_hi_pins: list[int],
                 hw_model: int,
                 adapter_notes: str | None = None):
        
        self.name = name
        self.package = package
        self.hw_model = hw_model
        self.adapter_notes = adapter_notes
        self.adapter_hi_pins = adapter_hi_pins

        # Remap pins on the ZIF socket
        self.clk_pins = self._remap_pin_array(zif_map, clk_pins)
        self.in_pins = self._remap_pin_array(zif_map, in_pins)
        self.io_pins = self._remap_pin_array(zif_map, io_pins)
        self.o_pins = self._remap_pin_array(zif_map, o_pins)
        self.f_pins = self._remap_pin_array(zif_map, f_pins)

