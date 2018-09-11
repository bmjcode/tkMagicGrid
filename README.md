**tkMagicGrid** is a spreadsheet-like widget for Python + Tkinter. It can be used to display static data, or to lay out other widgets as an alternative to calling `grid()` manually, or to do a bit of both.

tkMagicGrid is designed to be simple above all else. It has no dependencies outside the Python standard library. Its API is designed to let you accomplish tasks with as few method calls as possible.

tkMagicGrid is not designed to be erasable. The recommended way to clear a MagicGrid widget is to destroy it and create a new one.

Both Python 2 and 3 are supported, on Windows and Unix platforms.


## Usage

tkMagicGrid consists of a single module, `tkmagicgrid` (note the module
name is lowercase), which exports a single class, `MagicGrid`.

A brief example program:

```python
# This assumes Python 3
from tkinter import *
from tkmagicgrid import *
import io
import csv

# Create a root window
root = Tk()

# Create a MagicGrid widget
grid = MagicGrid(root)
grid.pack(side="top", expand=1, fill="both")

# Display the contents of some CSV file
# (note this is not a particularly efficient viewer)
with io.open("test.csv", "r", newline="") as csv_file:
    reader = csv.reader(csv_file)
    parsed_rows = 0
    for row in reader:
        if parsed_rows == 0:
    	    # Display the first row as a header
    	    grid.add_header(*row)
        else:
    	    grid.add_row(*row)
        parsed_rows += 1

# Start Tk's event loop
root.mainloop()
```

For detailed documentation, try `python -m pydoc tkmagicgrid`.


## Related Modules

[tkScrolledFrame](https://github.com/bmjcode/tkScrolledFrame) provides an easy way to make a `MagicGrid` (and other large widgets) scrollable.
