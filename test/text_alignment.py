#!/usr/bin/env python

"""Test program for MagicGrid's default text alignment rules."""

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


def set_widget_text(widget, text):
    """Set the specified widget's text after creation."""

    if hasattr(widget, "insert"):
        # Text entry widget
        widget.delete(0, "end")
        widget.insert("end", text)

    else:
        # All other widgets
        widget.configure(text=text)


def test():
    """Test MagicGrid's default text alignment rules."""

    root = Tk()
    root.title("Text Alignment Rules Test")

    for seq in "<Escape>", "<Control-w>", "<Control-q>":
        root.bind(seq, lambda event: root.destroy())

    mg = MagicGrid(root)
    mg.pack(side="top", expand=1, fill="both")

    # Format: label, value
    test_values = [
        ("Empty", ""),
        ("None", None),
        ("String", "Test"),
        ("Numeric", 8675309),
    ]
    labels = [item[0] for item in test_values]
    values = [item[1] for item in test_values]

    # Format: label, add_widget_function
    widgets = [
        ("Label", mg.add_cell),
        ("Entry", mg.add_widget_entry),
        ("Spinbox", mg.add_widget_spinbox),
        ("Checkbutton", mg.add_widget_checkbutton),
        ("Radiobutton", mg.add_widget_radiobutton),
        ("Button", mg.add_widget_button),
    ]

    # Header row identifies each type of test value
    header_cells = mg.add_header("", *labels,
                                 anchor="center",
                                 justify="center")

    for label, add_widget in widgets:
        # Label for the widget type
        mg.add_cell(label, width=12)

        for value in values:
            # Create a test widget
            widget = add_widget(value, width=20)

            # Fill Empty and None cells after a delay so we can see
            # how text added after the fact would be aligned
            if (isinstance(widget, Checkbutton)
                or isinstance(widget, Radiobutton)):
                continue

            elif value == "":
                root.after(5000, lambda widget=widget:
                           set_widget_text(widget, "Initially Empty"))

            elif value is None:
                root.after(5000, lambda widget=widget:
                           set_widget_text(widget, "Initially None"))

        mg.end_row()

    root.mainloop()


if __name__ == "__main__":
    test()
