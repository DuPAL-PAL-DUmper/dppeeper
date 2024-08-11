"""Frontend module"""

import argparse
import traceback
import logging

from tkinter import Tk

from enum import Enum

import serial

from dupicolib.board_commands import BoardCommands
from dupicolib.board_command_class_factory import BoardCommandClassFactory
from dupicolib.board_utilities import BoardUtilities
from dupicolib.board_fw_version import FwVersionTools, FWVersionDict

from dppeeper import __name__, __version__

from dppeeper.peeper_utilities import PeeperUtilities
from dppeeper.ic.ic_definition import ICDefinition
from dppeeper.ic.ic_loader import ICLoader

from dppeeper.ui.main_window import MainWin

MIN_SUPPORTED_MODEL: int = 3

_LOGGER: logging.Logger = logging.getLogger(__name__)

class Subcommands(Enum):
    SIM = 'sim'
    DUPICO = 'dupico'

def _build_argsparser() -> argparse.ArgumentParser:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog=__name__,
        description='A tool for interactive analysis of PLDs'
    )
   
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')

    parser.add_argument('-d', '--definition',
                             metavar='definition file',
                             help='Path to the file containing the definition of the IC to be read',
                             required=True)
    
    parser.add_argument('--skip_note',
                             action='store_true',
                             default=False,
                             help='If present, skip printing adapter notes and associated delays')

    hiz_group = parser.add_argument_group()
    hiz_group.add_argument('--check_hiz',
                             action='store_true',
                             default=False,
                             help='Check if output pins are Hi-Z or not.')    
    hiz_group.add_argument('--skip_hiz',
                        action='append',
                        metavar='pin_to_skip',
                        nargs='+',
                        type=int,
                        default=[],
                        help='List of output pins for which the Hi-Z check is skipped')

    subparsers = parser.add_subparsers(help='supported subcommands', dest='subcommand', required=True)

    parser_sim = subparsers.add_parser(Subcommands.SIM.value, help='Read data from a recorded file')
    parser_sim.add_argument('-s', '--sim_file',
                            metavar='simulation file',
                            required=True,
                            help='File with recorded transitions for simulation purposes')
    
    parser_conn = subparsers.add_parser(Subcommands.DUPICO.value, help='Read data the dupico board')
    parser_conn.add_argument('-p', '--port',
                        type=str,
                        nargs='?',
                        metavar="serial port",
                        required=True,
                        help='Serial port associated with the board')
    parser_conn.add_argument('-b', '--baudrate',
                        type=int,
                        metavar="baud rate",
                        default=115200,
                        help='Speed at which to the serial port is opened')

    return parser

def cli() -> int:
    args = _build_argsparser().parse_args()

    # Prepare the logger
    debug_level: int = logging.ERROR
    if args.verbose > 1:
        debug_level = logging.DEBUG
    elif args.verbose > 0:
        debug_level = logging.INFO
    logging.basicConfig(level=debug_level)

    if not args.port:
        PeeperUtilities.print_serial_ports()      
        return 1
    else:
        ser_port: serial.Serial | None = None

        try:
            # Load and check IC definition requirements
            ic_definition: ICDefinition
            with open(args.definition, 'rb') as def_file:
                ic_definition = ICLoader.extract_definition_from_buffered_reader(def_file)

            match args.subcommand:
                case Subcommands.SIM.value:
                    sim_command(ic_definition)
                case Subcommands.DUPICO.value:
                    connect_command(args.port, args.baudrate, ic_definition)
                case _:
                    _LOGGER.critical(f'Unsupported command {args.subcommand}')


        except Exception as ex:
            _LOGGER.critical(traceback.format_exc())
            return -1

        _LOGGER.info('Quitting.')          
    return 0

def start_ui(ic_defintion: ICDefinition) -> None:
    root: Tk = Tk()
    mw = MainWin(name='dppeeper', ic_definition=ic_defintion)
    root.resizable(False, False)
    root.mainloop()

def sim_command(ic_definition: ICDefinition) -> None:
    raise NotImplementedError('Simulation mode not currently implemented.')

def connect_command(port_name: str, baudrate: int, ic_definition: ICDefinition) -> int:
    ser_port: serial.Serial | None = None
    
    try:
        _LOGGER.debug(f'Trying to open serial port {port_name}')
        ser_port = serial.Serial(port = port_name,
                                 baudrate=baudrate,
                                 bytesize = 8,
                                 stopbits = 1,
                                 parity = 'N',
                                 timeout = 5.0)
            
        if not BoardUtilities.initialize_connection(ser_port):
            _LOGGER.critical('Serial port connected, but the board did not respond in time.')
            return -1
            
        _LOGGER.info(f'Board connected @{port_name}, speed:{baudrate} ...')
        model: int | None = BoardCommands.get_model(ser_port)
        if model is None:
            _LOGGER.critical('Unable to retrieve model number...')
            return -1
        elif model < MIN_SUPPORTED_MODEL:
            _LOGGER.critical(f'Model {model} is not supported.')
            return -1
        else:
            _LOGGER.info(f'Model {model} detected!')
            
        fw_version: str | None = BoardCommands.get_version(ser_port)
        fw_version_dict: FWVersionDict
        if fw_version is None:
            _LOGGER.critical('Unable to retrieve firmware version...')
            return -1
        else:
            fw_version_dict = FwVersionTools.parse(fw_version) # Check that the version is formatted correctly
            _LOGGER.info(f'Firmware version on board is "{fw_version}"')

        if ic_definition.hw_model > model:
            raise ValueError(f'Current hardware model {model} does not satisfy requirement {ic_definition.hw_model}')

        # Now we have enough information to obtain the class that handles commands specific for this board
        command_class: BoardCommands = BoardCommandClassFactory.get_command_class(model, fw_version_dict)

        # And finally, start the UI
        start_ui(ic_definition)
    finally:
        if ser_port and not ser_port.closed:
            _LOGGER.debug('Closing the serial port.')
            ser_port.close()