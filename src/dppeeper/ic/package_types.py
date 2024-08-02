"""This file contains the enum with supported package types"""

from enum import Enum

class PackageType(Enum):
    SIP = 'SIP'
    DIP = 'DIP'
    QUAD = 'QUAD'