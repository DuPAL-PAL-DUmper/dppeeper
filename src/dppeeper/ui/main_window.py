"""This module contains code for the main window"""

from tkinter import BOTH, RAISED, X, Button, Label
from tkinter.ttk import Frame

from dppeeper.ic.ic_definition import ICDefinition
from dppeeper.ui.ui_utilities import UIUtilities

class MainWin(Frame):
    _ic_definition: ICDefinition

    def __init__(self, name: str, ic_definition: ICDefinition) -> None:
        super().__init__()

        self._ic_definition = ic_definition

        self.initUI(name)

    def centerWindow(self):
        w = 400
        h = 600

        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()

        x = (sw - w)//2
        y = (sh - h)//2

        self.master.geometry(f'{w}x{h}+{x}+{y}')

    def initUI(self, name: str):
        grid_w: int; grid_h: int
        grid_w, grid_h = UIUtilities.calculateGridSize(self._ic_definition.pins_per_side)

        grid_frame = Frame(self)
        grid_frame.pack(side='top', anchor='center')
        for col in range(0, grid_w):
            grid_frame.columnconfigure(col, pad=15)
        for row in range(0, grid_h):
            grid_frame.rowconfigure(row, pad=15)
        
        for i, pin in enumerate(self._ic_definition.zif_map):
            l_x: int; l_y: int
            b_x: int; b_y: int
            l_x, l_y = UIUtilities.calculatePinPosition(i + 1, True, self._ic_definition.pins_per_side)
            b_x, b_y = UIUtilities.calculatePinPosition(i + 1, False, self._ic_definition.pins_per_side)

            if pin == 21:
                gnd_lbl = Label(grid_frame, text='GND', width = 6)
                gnd_lbl.grid(row=l_y, column=l_x)
            elif pin == 42:
                pwr_lbl = Label(grid_frame, text='PWR', width = 6)
                pwr_lbl.grid(row=l_y, column=l_x)
            else:
                gen_lbl = Label(grid_frame, text=self._ic_definition.pin_names[i], width = 6)
                gen_lbl.grid(row=l_y, column=l_x)
                gen_btn = Button(grid_frame, text='.', width = 6)
                gen_btn.grid(row=b_y, column=b_x)

        button_frame = Frame(self)
        button_frame.pack(fill=BOTH, expand=True, side='top', anchor='center')


        self.pack(fill=BOTH, expand=1)

        self.master.title(name)
        self.centerWindow()