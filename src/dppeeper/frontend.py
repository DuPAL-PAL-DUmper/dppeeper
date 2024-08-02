from enum import Enum
import logging
import argparse

from dppeeper import __name__, __version__

MIN_SUPPORTED_MODEL: int = 3

_LOGGER: logging.Logger = logging.getLogger(__name__)

class Subcommands(Enum):
    SIM = 'sim'
    CONNECT = 'connect'

def _build_argsparser() -> argparse.ArgumentParser:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog=__name__,
        description='A tool for visual analysis of PLDs'
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
    
    parser_conn = subparsers.add_parser(Subcommands.CONNECT.value, help='Read data the dupico board')
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

    return 0