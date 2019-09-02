"""Demonstration of the MagicGrid widget."""

import os
import sys

try:
    # Python 3
    from tkinter import *
    from tkinter.messagebox import showinfo, showwarning
except (ImportError):
    # Python 2
    from Tkinter import *
    from tkMessageBox import showinfo, showwarning

from .widget import MagicGrid


__all__ = ["demo"]


BEATLES = [
    # Name                  Founding    Fab Four    5th Beatle  Solo Albums
    ("John Lennon",         True,       True,       False,      11          ),
    ("Paul McCartney",      True,       True,       False,      18          ),
    ("George Harrison",     True,       True,       False,      12          ),
    ("Ringo Starr",         False,      True,       False,      19          ),
    ("Stuart Sutcliffe",    True,       False,      False,      0           ),
    ("Pete Best",           True,       False,      False,      11          ),
    ("George Martin",       False,      False,      True,       15          ),
    ("Billy Preston",       False,      False,      True,       22          ),
    ("Eric Clapton",        False,      False,      True,       22          ),
]


class MagicGridDemo(Frame):
    """A demonstration of the MagicGrid widget."""

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        mg = self.mg = MagicGrid(self)
        mg.pack(side="top", expand=1, fill="both")

        # Variable for Radiobuttons
        selection = self.selection = StringVar()
        selection.set("Paul McCartney")

        # Add a header row
        header_cells = mg.add_header("", "Beatle",
                                     "Founding?", "Fab Four?", "5th Beatle?",
                                     "Solo Albums", "Notes", "Action")

        # Set reasonable column widths
        mg.configure_column(0, width=4)
        for col in range(1, 5):
            mg.configure_column(col, width=12)
        for col in range(2, 5):
            header_cells[col].configure(anchor="center", justify="center")

        # The Notes column is stretchy
        mg.configure_column(6, weight=1)

        row_num = 1
        for beatle, founding, fab_four, fifth_beatle, solo_albums in BEATLES:
            # Row Number
            mg.add_cell(row_num)

            # Beatle
            mg.add_widget_radiobutton(beatle,
                                      value=beatle, variable=selection)

            # Founding
            c = mg.add_widget_checkbutton()
            if founding: c.select()

            # Fab Four
            c = mg.add_widget_checkbutton()
            if fab_four: c.select()

            # 5th Beatle
            c = mg.add_widget_checkbutton()
            if fifth_beatle: c.select()

            # Solo Albums
            mg.add_widget_spinbox(solo_albums,
                                  width=12, from_=0, to=100, increment=1)

            # Notes
            mg.add_widget_entry(width=48)

            # Action
            button_command = lambda beatle=beatle: self.spam(beatle)
            mg.add_widget_button("Spam", command=button_command)

            # End the current row
            mg.end_row()
            row_num += 1

        # Provide plenty of ways to close the demo window
        for seq in "<Escape>", "<Control-w>", "<Control-q>":
            self.master.bind(seq, self.close)

    def close(self, event=None):
        """Close the window."""

        # Destroy the window
        self.master.destroy()

    def spam(self, beatle):
        """Display a silly pop-up message."""

        if beatle == self.selection.get():
            showinfo("Spam",
                     "You spammed {0}!".format(beatle),
                     parent=self)

        else:
            showwarning("Spam",
                        "You want to spam {0}, but {1} is selected!"
                        .format(beatle, self.selection.get()),
                        parent=self)


def demo():
    """Display a demonstration of the MagicGrid widget."""

    root = Tk()
    root.title("tkMagicGrid")

    m = MagicGridDemo(root)
    m.pack(side="top", expand=1, fill="both")

    root.mainloop()


if __name__ == "__main__":
    demo()
