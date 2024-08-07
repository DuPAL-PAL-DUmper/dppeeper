"""This module contains code for the main window"""

from tkinter import Misc, Tk, BOTH
from tkinter.ttk import Frame
from typing import Callable, Literal

class MainWin(Frame):
    def __init__(self, master: Misc | None = None, *, border: str | float = ..., borderwidth: str | float = ..., class_: str = "", cursor: str | tuple[str] | tuple[str, str] | tuple[str, str, str] | tuple[str, str, str, str] = "", height: str | float = 0, name: str = ..., padding: str | float | tuple[str | float] | tuple[str | float, str | float] | tuple[str | float, str | float, str | float] | tuple[str | float, str | float, str | float, str | float] = ..., relief: Literal['raised'] | Literal['sunken'] | Literal['flat'] | Literal['ridge'] | Literal['solid'] | Literal['groove'] = ..., style: str = "", takefocus: bool | Callable[[str], bool | None] | Literal[0] | Literal[1] | Literal[''] = "", width: str | float = 0) -> None:
        super().__init__(master, border=border, borderwidth=borderwidth, class_=class_, cursor=cursor, height=height, name=name, padding=padding, relief=relief, style=style, takefocus=takefocus, width=width)

        self.initUI(name)

    def initUI(self, name: str):
        self.master.title(name)
        self.pack(fill=BOTH, expand=1)