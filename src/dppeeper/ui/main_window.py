"""This module contains code for the main window"""

import logging
from tkinter import BOTH, CENTER, LEFT, RAISED, TOP, X, IntVar, ttk
from tkinter.ttk import Frame, Checkbutton, Label, Button
from typing import Tuple
import time

import serial

from dppeeper.ic.ic_definition import ICDefinition
from dppeeper.ui.ui_utilities import UIUtilities, UIPinGridType
from dupicolib.board_commands import BoardCommands

class MainWin(Frame):
    _ic_definition: ICDefinition
    _board_commands: BoardCommands

    _hiz_check_list: list[int]

    _always_high_mask: int

    _ser = serial.Serial | None
    
    _checkb_states: dict[int, IntVar]
    _pin_state_labels: dict[int, Label]

    _LOGGER = logging.getLogger(__name__)

    _IC_NAME_LABEL_STYLE = 'ICNAME.TLabel'

    _PINNUM_LABEL_STYLE = 'PINN.TLabel'
    _POWER_LABEL_STYLE = 'PWR.TLabel'
    _HI_LABEL_STYLE = 'HI.TLabel'
    _LO_LABEL_STYLE = 'LO.TLabel'
    _Z_LABEL_STYLE = 'Z.TLabel'

    _RESET_BUTTON_STYLE = 'RESET.TButton'

    def __init__(self, name: str, ic_definition: ICDefinition, board_commands: BoardCommands, check_hiz: bool = False, skip_hiz: list[int] = [],  ser: serial.Serial | None = None) -> None:
        super().__init__()

        self._ic_definition = ic_definition
        self._board_commands = board_commands
        self._ser = ser

        self._hiz_check_list = self._generate_hiz_check_list(ic_definition, skip_hiz) if check_hiz else []

        self._checkb_states = {}
        self._pin_state_labels = {}

        self._always_high_mask = self._board_commands.map_value_to_pins(self._ic_definition.adapter_hi_pins, 0xFFFFFFFFFFFFFFFF)

        self.buildStyles()
        self.initUI(name)

        # Send the first command to read the state
        self._cmd_set()

    def buildStyles(self) -> None:
        style = ttk.Style()

        style.configure(self._IC_NAME_LABEL_STYLE, font=('Arial', '16', 'bold'))
        style.configure(self._PINNUM_LABEL_STYLE)
        style.configure(self._POWER_LABEL_STYLE, background='#AAAAAA')
        style.configure(self._HI_LABEL_STYLE, background='#B7FFB7')
        style.configure(self._LO_LABEL_STYLE, background='#FFB7B7')
        style.configure(self._Z_LABEL_STYLE, background='#FFF4B7')

        style.configure(self._RESET_BUTTON_STYLE, font=('Sans','10','bold'), foreground='red')        

    def initUI(self, name: str) -> None:
        name_label = Label(self, text=self._ic_definition.name, anchor=CENTER, style=self._IC_NAME_LABEL_STYLE)
        name_label.pack(side=TOP, anchor=CENTER, fill=X)

        grid_w: int; grid_h: int
        grid_w, grid_h = UIUtilities.calculateGridSize(self._ic_definition.pins_per_side)

        grid_frame = Frame(self)
        grid_frame.pack(side=TOP, anchor=CENTER)
        for col in range(0, grid_w):
            grid_frame.columnconfigure(col, pad=15)
        for row in range(0, grid_h):
            grid_frame.rowconfigure(row, pad=10)
        
        for i, pin in enumerate(self._ic_definition.zif_map):
            l_x: int; l_y: int
            c_x: int; c_y: int
            n_x: int; n_y: int
            l_x, l_y = UIUtilities.calculatePinPosition(i + 1, UIPinGridType.LABEL, self._ic_definition.pins_per_side)
            c_x, c_y = UIUtilities.calculatePinPosition(i + 1, UIPinGridType.CHECKBOX, self._ic_definition.pins_per_side)
            n_x, n_y = UIUtilities.calculatePinPosition(i + 1, UIPinGridType.PIN_NUM, self._ic_definition.pins_per_side)

            pn_lbl = Label(grid_frame, text=f'{i+1}', width = 6, anchor=CENTER, style=self._PINNUM_LABEL_STYLE)
            pn_lbl.grid(row=n_y, column=n_x)

            if pin == 21: # GND pins
                gnd_lbl = Label(grid_frame, text='GND', width = 6, anchor=CENTER, style=self._POWER_LABEL_STYLE)
                gnd_lbl.grid(row=l_y, column=l_x)
            elif pin == 42: # Power pins
                pwr_lbl = Label(grid_frame, text='PWR', width = 6, anchor=CENTER, style=self._POWER_LABEL_STYLE)
                pwr_lbl.grid(row=l_y, column=l_x)
            else:
                gen_lbl = Label(grid_frame, text=self._ic_definition.pin_names[i], width = 6, anchor=CENTER, style=self._LO_LABEL_STYLE)
                gen_lbl.grid(row=l_y, column=l_x)
                # Save the labels that represent the state of pins, we're also saving GND and power pins, to make sure
                # the index value for the label matches the pin number
                self._pin_state_labels[i] = gen_lbl
                
                # Save the variables that store the state for checkboxes
                chkb_var: IntVar = IntVar(value=0)
                self._checkb_states[i] = chkb_var
                gen_chk = Checkbutton(grid_frame, text=None, takefocus=False, variable=chkb_var)
                gen_chk.grid(row=c_y, column=c_x)

        button_frame = Frame(self, relief=RAISED, borderwidth=1, padding=5)
        button_frame.pack(fill=BOTH, expand=True, side=TOP, anchor=CENTER)

        inner_button_frame = Frame(button_frame)
        inner_button_frame.pack(side=TOP, anchor=CENTER)

        set_button = Button(inner_button_frame, text='SET', command=self._cmd_set)
        set_button.pack(anchor=CENTER, side=LEFT, padx=5, pady=5)

        clear_button = Button(inner_button_frame, text='CLEAR', command=self._cmd_clear)
        clear_button.pack(anchor=CENTER, side=LEFT, padx=5, pady=5)

        pcycle_button = Button(inner_button_frame, text='P.CYCLE', style=self._RESET_BUTTON_STYLE, command=self._cmd_powercycle)
        pcycle_button.pack(anchor=CENTER, side=LEFT, padx=5, pady=5)

        clock_button_frame = Frame(button_frame)
        clock_button_frame.pack(side=TOP, anchor=CENTER)
        
        for i, clk_pin in enumerate(self._ic_definition.clk_pins):
            clk_button = Button(clock_button_frame, text=f'Clock {clk_pin}', command=lambda: self._cmd_clock(clk_pin))
            clk_button.pack(anchor=CENTER, side=LEFT, padx=5, pady=5)

        self.pack(fill=BOTH, expand=1)

        self.master.title(name)

    def _set_and_check_pins(self, val: int) -> Tuple[int, int]:
        hiz_pins: int = 0
        hiz_pins_to_remove: list[int] = []

        hiz_mask: int = self._build_hiz_mask(self._hiz_check_list)
        ret: int = self._write_val(val)

        # The pins we are currently setting between those we need to check for hiz
        toggled_hiz_pins: int = val & hiz_mask

        # The inverse of the same pins, we will use this to check if they follow our pulls or not
        rev_toggled_hiz_pins: int = (~toggled_hiz_pins) & hiz_mask

        for pin in self._hiz_check_list:
            pin_mask: int = 1 << (pin - 1)
            # Invert the corresponding pin
            wr_val: int = (val & ~pin_mask) | (rev_toggled_hiz_pins & pin_mask)
            ret_chk = self._write_val(wr_val)
            self._write_val(val)
            
            changed_pins: int = ret ^ ret_chk
            if changed_pins == pin_mask: # The only pin that changed is the one we are checking. It's hi-z
                hiz_pins = hiz_pins | pin_mask
            elif changed_pins != 0: # One or more pins have changed, but it is not our checked pin, means we might have toggled an input!!!
                hiz_pins_to_remove.append(pin)

        # Purge the pins that we detected being inputs, we don't want to check them again!!!
        for pin in hiz_pins_to_remove:
            self._LOGGER.warning(f'Removing pin {pin} from list of potential hi-z pins: triggered changes in other pins, probably an input!')
            self._hiz_check_list.remove(pin)

        return (ret, hiz_pins)

    @staticmethod
    def _build_hiz_mask(hiz_pins: list[int]) -> int:
        mask: int = 0

        for i in hiz_pins:
            mask = mask | (1 << (i-1))

        return mask

    def _write_val(self, val: int) -> int | None:
        map_val: int = self._board_commands.map_value_to_pins(self._ic_definition.zif_map, val)
        map_val = map_val | self._always_high_mask

        res_wr: int | None = self._board_commands.write_pins(self._ser, map_val)
        if res_wr is None:
            raise SystemError('Read from the dupico failed')

        return self._board_commands.map_pins_to_value(self._ic_definition.zif_map, res_wr)

    def _update_labels(self, read_val: int, hiz_val: int) -> None:
        """
        Update the state labels of each pin according to the value read

        Args:
            read_val (int): value read from the dupico, already remapped (e.g. bit 0 corresponds to pin 1 of the IC)
            hiz_val (int): if a bit is 1 in this map, it means the pin is hi-z
        """        
        for k,v in self._pin_state_labels.items():
            state: bool = ((read_val >> k) & 0x01) == 1
            hiz: bool = ((hiz_val >> k) & 0x01) == 1

            if hiz:
                v.configure(style=self._Z_LABEL_STYLE)
            elif state:
                v.configure(style=self._HI_LABEL_STYLE)
            else:
                v.configure(style=self._LO_LABEL_STYLE)
            
    def _build_set_value(self) -> int:
        val: int = 0

        for k,v in self._checkb_states.items():
            if bool(v.get()):
                val = val | (1 << k)

        return val

    def _cmd_set(self) -> None:
        read: int; hiz: int

        set_val: int = self._build_set_value()
        read, hiz = self._set_and_check_pins(set_val)
        self._update_labels(read, hiz)

    def _cmd_powercycle(self) -> None:
        self._board_commands.set_power(self._ser, False)
        time.sleep(0.5)
        self._board_commands.set_power(self._ser, True)
        time.sleep(0.5)
        self._cmd_set()

    def _cmd_clear(self) -> None:
        for k,v in self._checkb_states.items():
            v.set(0)

        self._cmd_set()

    def _cmd_clock(self, pin: int) -> None:
        pass

    @staticmethod
    def _generate_hiz_check_list(ic_definition: ICDefinition, skip_hiz: list[int] = []) -> list[int]:
        check_list: list[int] = []

        check_list.extend(ic_definition.o_pins)
        check_list.extend(ic_definition.io_pins)
        check_list.sort()

        return [i for i in check_list if i not in skip_hiz]