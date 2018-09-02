#!/usr/bin/env python

"""A spreadsheet-like widget for Tkinter.

tkMagicGrid is a spreadsheet-like widget for Python + Tkinter.
It can be used to display static data, or to lay out other widgets
as an alternative to calling grid() manually, or to do a bit of both.

tkMagicGrid is designed to be simple above all else. It has no
dependencies outside the Python standard library. Its API is designed
to let you accomplish tasks with as few method calls as possible.

tkMagicGrid is not designed to be erasable. The recommended way
to clear a MagicGrid widget is to destroy it and create a new one.
"""

from .widget import MagicGrid

# The only thing we need to publicly export is the MagicGrid widget
__all__ = ["MagicGrid"]
