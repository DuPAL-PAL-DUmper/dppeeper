"""This class contains code to extract an IC definition from a properly formatted TOML file read from a BufferedReader"""

from io import BufferedReader
from typing import Any, final
from dppeeper.ic.ic_definition import ICDefinition
from dppeeper.ic.ic_package_types import ICPackageType

import tomllib

@final
class ICLoader:
    _KEY_NAME: str = 'name'
    _KEY_PACKAGE: str = 'package'
    _KEY_PINOUT: str = 'pinout'
    _KEY_PINOUT_ZIFMAP:str = 'ZIF_map'
    _KEY_PINOUT_CLKP:str = 'clk_pins'
    _KEY_PINOUT_INP:str = 'in_pins'
    _KEY_PINOUT_IOP: str = 'io_pins'
    _KEY_PINOUT_OP: str = 'o_pins'
    _KEY_PINOUT_FP: str = 'f_pins'
    _KEY_ADAPTER: str = 'adapter'
    _KEY_ADAPTER_HI_PINS: str = 'hi_pins'
    _KEY_ADAPTER_NOTES: str = 'notes'
    _KEY_REQUIREMENTS: str = 'requirements'
    _KEY_REQUIREMENTS_HARDWARE: str = 'hardware'

    @classmethod
    def extract_definition_from_buffered_reader(cls, filebuf: BufferedReader) -> ICDefinition:
        toml_data: dict[str, Any] = tomllib.load(filebuf)

        ic_package: ICPackageType = ICPackageType(toml_data[cls._KEY_PACKAGE])
        
        return ICDefinition(name=toml_data[cls._KEY_NAME],
                                package=ic_package,
                                zif_map=toml_data[cls._KEY_PINOUT][cls._KEY_PINOUT_ZIFMAP],
                                clk_pins=toml_data[cls._KEY_PINOUT][cls._KEY_PINOUT_CLKP],
                                in_pins=toml_data[cls._KEY_PINOUT][cls._KEY_PINOUT_INP],
                                io_pins=toml_data[cls._KEY_PINOUT][cls._KEY_PINOUT_IOP],
                                o_pins=toml_data[cls._KEY_PINOUT][cls._KEY_PINOUT_OP],
                                f_pins=toml_data[cls._KEY_PINOUT][cls._KEY_PINOUT_FP],
                                hw_model=toml_data[cls._KEY_REQUIREMENTS][cls._KEY_REQUIREMENTS_HARDWARE],
                                adapter_hi_pins=toml_data[cls._KEY_ADAPTER][cls._KEY_ADAPTER_HI_PINS],
                                adapter_notes=toml_data[cls._KEY_ADAPTER].get(cls._KEY_ADAPTER_NOTES, None))
