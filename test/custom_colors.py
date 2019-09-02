#!/usr/bin/env python3

"""Test program for custom row colors."""

import sys

# Look for tkmagicgrid in the parent directory
sys.path.insert(0, "..")

try:
    # Python 3
    from tkinter import *
except (ImportError):
    # Python 2
    from Tkinter import *

from tkmagicgrid import MagicGrid


def test():
    """Test MagicGrid's support for custom row colors."""

    root = Tk()
    root.title("Custom Row Colors Test")

    for seq in "<Escape>", "<Control-w>", "<Control-q>":
        root.bind(seq, lambda event: root.destroy())

    mg = MagicGrid(root,
                   bg_color="antique white",
                   fg_color="dark goldenrod",
                   bg_header="forest green",
                   fg_header="white",
                   bg_shade="light goldenrod",
                   fg_shade="maroon")
    mg.pack(side="top", expand=1, fill="both")

    # Add a bunch of cells
    num_rows = 16
    num_columns = 16
    header = range(num_columns)

    for column in range(num_columns):
        mg.configure_column(column, weight=1)

    mg.add_header(*header)
    for row in range(0, num_rows):
        for column in range(num_columns):
            # Increment each successive cell's value by one
            value = row * num_columns + column

            # Read-only cell
            mg.add_cell(value)

        mg.end_row()

    # Make all columns equal width
    for column in range(num_columns):
        mg.configure_column(column, width=4, weight=1)

    root.mainloop()


if __name__ == "__main__":
    test()
