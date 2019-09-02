#!/usr/bin/env python

"""Test program for displaying numeric values in cells.

If the "-e" argument is present, the values will be displayed in editable
Entry widgets. Otherwise, the values will be displayed read-only.
"""

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
    """Test MagicGrid's display of numeric values."""

    root = Tk()
    root.title("Numeric Values Display Test")

    for seq in "<Escape>", "<Control-w>", "<Control-q>":
        root.bind(seq, lambda event: root.destroy())

    mg = MagicGrid(root)
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

            if "-e" in sys.argv[1:]:
                # Make this an Entry widget
                mg.add_widget_entry(value)

            else:
                # Read-only cell
                mg.add_cell(value)

        mg.end_row()

    # Test Boolean values too, while we're at it
    mg.add_cell("Boolean values:", columnspan=3)
    mg.add_cell(True)
    mg.add_cell(False)

    # Pad out the rest of the row
    for column in range(5, num_columns):
        mg.add_cell()
    mg.end_row()

    # Highlight the last row
    mg.configure_row(num_rows + 1, bg="yellow")

    # Highlight the last column, too
    mg.configure_column(num_columns - 1, bg="orange")

    # Make all columns equal width
    for column in range(num_columns):
        mg.configure_column(column, width=4, weight=1)

    root.mainloop()


if __name__ == "__main__":
    test()
