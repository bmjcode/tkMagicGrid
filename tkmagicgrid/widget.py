"""Implementation of the MagicGrid widget."""

import copy
import numbers

# MagicGrid does not use ttk because its widgets do not allow direct styling.
try:
    # Python 3
    import tkinter as tk
except (ImportError):
    # Python 2
    import Tkinter as tk


class MagicGrid(tk.Frame):
    """Table layout widget.

    The constructor accepts the usual Tkinter keyword arguments, plus
    a handful of its own:

      bg_color (str)
        Default background color for ordinary rows.

      bg_header (str)
        Default background color for header rows.

      bg_shade (str)
        Default background color for shading alternate rows.

      enable_arrow_keys (bool; default: True)
        Enables keyboard navigation between cells using the arrow keys.

      fg_color (str)
        Default foreground color for ordinary rows.

      fg_header (str)
        Default foreground color for header rows.

      fg_shade (str)
        Default foreground color for shading alternate rows.

      shade_rows (bool; default: True)
        Enables shading alternate rows for readability.
    """

    def __init__(self, master=None, **kw):
        """Return a new MagicGrid widget."""

        tk.Frame.__init__(self, master)

        # Process MagicGrid's custom keywords.
        # Note we have to remove our custom keywords after processing them,
        # since unknown options cause Frame.configure() to raise a TclError.

        # Whether to enable arrow key navigation
        if "enable_arrow_keys" in kw:
            self._enable_arrow_keys = kw["enable_arrow_keys"]
            del kw["enable_arrow_keys"]
        else:
            # Enable arrow keys by default
            self._enable_arrow_keys = True

        # Whether to shade alternate rows
        if "shade_rows" in kw:
            self._shade_rows = kw["shade_rows"]
            del kw["shade_rows"]
        else:
            # Shade rows by default
            self._shade_rows = True

        # Default row colors
        # Note: Releases prior to v1.0.3 exposed these attributes as
        # public class variables, but this was not a documented feature
        # and is no longer supported.
        for attr in ("bg_color", "bg_header", "bg_shade",
                     "fg_color", "fg_header", "fg_shade"):
            attr_name = "_{0}".format(attr)
            default_name = "_DEFAULT_{0}".format(attr.upper())
            if attr in kw:
                setattr(self, attr_name, kw[attr])
                del kw[attr]
            else:
                setattr(self, attr_name, getattr(self, default_name))

        # Pass remaining configuration options to the Frame class
        tk.Frame.configure(self, **kw)

        # The row and column where we should add our next cell
        self._row = 0
        self._col = 0

        # Length of the largest row we've added
        self._row_max = 0

        # List of lists of widgets representing table cells
        # To access a particular widget, use self._cells[row][column]
        self._cells = [ [] ]

        if self._shade_rows:
            # Set the frame background to the default cell background
            self.configure(background=self._bg_color)

    # ------------------------------------------------------------------------

    def add_cell(self, contents="", **kw):
        """Add a cell with the specified contents to the current row.

        See add_widget() for information on supported keyword arguments.

        If the "anchor" and "justify" keyword arguments are not specified,
        the default text alignment is right for numeric values, or left
        otherwise. This only applies when creating a new cell; changing a
        cell's contents later will not affect text alignment.

        Returns a Tk Label widget corresponding to the new cell.
        """

        return self._add_standard_widget(tk.Label, contents, **kw)

    def add_header(self, *cells, **kw):
        """Add a header row to the grid.

        See add_widget() for information on supported keyword arguments.
        These will be applied to all cells in this row. Default text
        alignment rules are the same as for add_cell().

        The next cell added to the grid will start a new row.

        Returns a list of widgets corresponding to the new cells.
        """

        return self.add_row(*cells,
                            background=self._bg_header,
                            foreground=self._fg_header,
                            **kw)

    def add_row(self, *cells, **kw):
        """Add an entire row of cells to the grid.

        See add_widget() for information on supported keyword arguments.
        These will be applied to all cells in this row. Default text
        alignment rules are the same as for add_cell().

        The next cell added to the grid will start a new row.

        Returns a list of widgets corresponding to the new cells.
        """

        header_widgets = []

        for cell in cells:
            widget = self.add_cell(cell, **kw)
            header_widgets.append(widget)

        self.end_row()

        return header_widgets

    def add_widget(self, widget_class, **kw):
        """Create a widget of the specified class and add it to the grid.

        This method accepts keyword arguments for both the widget_class
        constructor, to configure the widget itself, and Tk's grid()
        method, to configure its placement in the grid.

        Returns the new widget.
        """

        # Widgets spanning multiple rows are not currently supported
        # because of how self._cells is implemented
        if "rowspan" in kw:
            raise tk.TclError('the "rowspan" keyword '
                              'is not currently supported')

        # Don't pass grid()'s keywords to the widget constructor
        # Note _add_widget() will process widget keywords further
        widget_kw = copy.copy(kw)
        for key in self._GRID_KEYS:
            if key in widget_kw:
                del widget_kw[key]

        # Create the widget and add it to the grid
        widget = widget_class(self, **widget_kw)
        return self._add_widget(widget, **kw)

    def add_widget_button(self, text="", **kw):
        """Create a Button widget and add it to the grid.

        See add_widget() for information on supported keyword arguments.
        Button widgets always follow standard Tk text alignment rules.

        Returns the new widget.
        """

        return self._add_standard_widget(tk.Button, text, **kw)

    def add_widget_checkbutton(self, text="", **kw):
        """Create a Checkbutton widget and add it to the grid.

        See add_widget() for information on supported keyword arguments.

        If the "anchor" and "justify" keyword arguments are not specified,
        the widget will be left-aligned if its label text was specified,
        or centered otherwise. This only applies when creating a new
        widget; changing its text later will not change its alignment.

        Returns the new widget.
        """

        return self._add_standard_widget(tk.Checkbutton, text, **kw)

    def add_widget_entry(self, initial_value="", **kw):
        """Create an Entry widget and add it to the grid.

        See add_widget() for information on supported keyword arguments.
        Default text alignment rules are the same as for add_cell().

        If the "width" keyword argument is not specified, the widget will
        be sized to fit its initial value.

        Returns the new widget.
        """

        return self._add_entry_widget(tk.Entry, initial_value, **kw)

    def add_widget_radiobutton(self, text="", **kw):
        """Create a Radiobutton widget and add it to the grid.

        See add_widget() for information on supported keyword arguments.

        If the "anchor" and "justify" keyword arguments are not specified,
        the widget will be left-aligned if its label text was specified,
        or centered otherwise. This only applies when creating a new
        widget; changing its text later will not change its alignment.

        Returns the new widget.
        """

        return self._add_standard_widget(tk.Radiobutton, text, **kw)

    def add_widget_spinbox(self, initial_value="", **kw):
        """Create a Spinbox widget and add it to the grid.

        See add_widget() for information on supported keyword arguments.
        Default text alignment rules are the same as for add_cell().

        If the "width" keyword argument is not specified, the widget will
        be sized to fit its initial value.

        Returns the new widget.
        """

        return self._add_entry_widget(tk.Spinbox, initial_value, **kw)

    def configure_cell(self, row, column, **kw):
        """Configure the widget corresponding to the specified cell."""

        self._cells[row][column].configure(**kw)

    def configure_column(self, column, **kw):
        """Configure all cell widgets in the specified column.

        This method accepts keyword arguments for both the widgets'
        configure() methods, to configure the widgets themselves, and
        Tk's grid_columnconfigure() method, to configure the grid layout.

        If called with ignore_errors=True, TclError will be silently
        ignored. This is useful if not all widgets in the column support
        a particular configuration option. For example, ttk widgets
        don't support plain Tk's "background" and "foreground" options.
        """

        if "ignore_errors" in kw:
            ignore_errors = kw["ignore_errors"]
            del kw["ignore_errors"]
        else:
            ignore_errors = False

        # Separate keywords for grid_columnconfigure()
        grid_kw = {}
        for key in self._GRID_COLUMN_ROW_KEYS:
            if key in kw:
                grid_kw[key] = kw[key]
                del kw[key]

        # Configure grid layout
        if grid_kw:
            self.grid_columnconfigure(column, **grid_kw)

        # Configure widgets
        for row in self._cells:
            # The last row may have fewer than (self._row_max - 1) cells
            # if we are still adding data, or just called self.end_row()
            if row:
                cell = row[column]
                if cell:
                    try:
                        cell.configure(kw)

                    except (tk.TclError):
                        if ignore_errors: continue
                        else: raise

    def configure_row(self, row, **kw):
        """Configure all cell widgets in the specified row.

        This method accepts keyword arguments for both the widgets'
        configure() methods, to configure the widgets themselves, and
        Tk's grid_rowconfigure() method, to configure the grid layout.

        If called with ignore_errors=True, TclError will be silently
        ignored. This is useful if not all widgets in the row support
        a particular configuration option. For example, ttk widgets
        don't support plain Tk's "background" and "foreground" options.
        """

        if "ignore_errors" in kw:
            ignore_errors = kw["ignore_errors"]
            del kw["ignore_errors"]
        else:
            ignore_errors = False

        # Separate keywords for grid_rowconfigure()
        grid_kw = {}
        for key in self._GRID_COLUMN_ROW_KEYS:
            if key in kw:
                grid_kw[key] = kw[key]
                del kw[key]

        # Configure grid layout
        if grid_kw:
            self.grid_rowconfigure(row, **grid_kw)

        # Configure widgets
        for cell in self._cells[row]:
            if cell:
                try:
                    cell.configure(kw)

                except (tk.TclError):
                    if ignore_errors: continue
                    else: raise

    def end_row(self):
        """End the current row.

        The next cell added to the grid will start a new row.
        """

        self._col = 0
        self._row += 1
        self._cells.append([])

    # ------------------------------------------------------------------------

    def _add_entry_widget(self, widget_class, initial_value, **kw):
        """Create a new text entry widget and add it to the grid.

        This is an internal function to preset some defaults particular
        to widgets that accept text entry (Entry and Spinbox).

        Returns the new widget.
        """

        if initial_value is None:
            # Replace None with an empty string
            # This matches the behavior of add_cell() and its ilk.
            initial_value = ""

        if not "relief" in kw:
            # Use flat relief by default
            kw["relief"] = "flat"

        if initial_value and not "width" in kw:
            # Fit the specified initial value
            kw["width"] = len(str(initial_value))

        if not "justify" in kw:
            if isinstance(initial_value, numbers.Number):
                # Right-align if the initial value is numeric
                kw["justify"] = "right"

            elif "from_" in kw or "to" in kw or "increment" in kw:
                # The "from_", "to", and "increment" keyword arguments
                # cause a Spinbox to accept a range of numeric values,
                # so also right-align if any of them was specified
                kw["justify"] = "right"

            else:
                # Left-align all other values
                kw["justify"] = "left"

        widget = self.add_widget(widget_class, **kw)

        if initial_value or isinstance(initial_value, numbers.Number):
            # The delete() call is necessary for Spinbox widgets if
            # the "from_", "to_", and/or "increment" keywords are set
            widget.delete(0, "end")
            widget.insert("end", str(initial_value))

        return widget

    def _add_standard_widget(self, widget_class, text, **kw):
        """Create a new non-entry widget and add it to the grid.

        This is an internal function to preset some defaults particular
        to widgets that don't accept text entry, including Label.

        Returns the new widget.
        """

        if text or isinstance(text, numbers.Number):
            # Preset the widget text
            kw["text"] = str(text)

        if widget_class == tk.Button:
            # Don't change the text alignment for Button widgets
            # because most people are used to the default
            pass

        elif widget_class in (tk.Checkbutton, tk.Radiobutton):
            if text:
                # Left-align by default if a label was specified
                if not "anchor" in kw:
                    kw["anchor"] = "w"
                if not "justify" in kw:
                    kw["justify"] = "left"

            else:
                # Center-align by default if no label was specified
                if not "anchor" in kw:
                    kw["anchor"] = "center"
                if not "justify" in kw:
                    kw["justify"] = "center"

        else:
            if isinstance(text, numbers.Number):
                # Right-align numeric values by default
                if not "anchor" in kw:
                    kw["anchor"] = "e"
                if not "justify" in kw:
                    kw["justify"] = "right"

            else:
                # Left-align all other values by default
                if not "anchor" in kw:
                    kw["anchor"] = "w"
                if not "justify" in kw:
                    kw["justify"] = "left"

        return self.add_widget(widget_class, **kw)

    def _add_widget(self, widget, **kw):
        """Add the specified (existing) widget to the grid.

        This is an internal method to handle the behind-the-scenes
        aspects of styling, placement, and interaction with other
        widgets. Your application should use the public add_widget()
        method to create new widgets, which has a simpler interface
        and ensures they are created with the correct master.

        This method accepts keyword arguments for Tk's grid() method
        to configure the widget's placement in the grid.

        Returns the new widget.
        """

        # Widgets spanning multiple rows are not currently supported.
        # Normally add_widget() will catch this before the widget is
        # created, but this is here as a failsafe in case some naughty
        # application is using our internal methods directly.
        if "rowspan" in kw:
            raise tk.TclError('the "rowspan" keyword '
                              'is not currently supported')

        # Whether to colorize the widget
        if ("bg" in kw
            or "background" in kw
            or "fg" in kw
            or "foreground" in kw):
            # Don't colorize the widget if the user specified colors
            do_colorize = False

        else:
            # Assume we need to colorize the widget
            do_colorize = True

        # Separate keywords for grid()
        grid_kw = {}
        for key in self._GRID_KEYS:
            if key in kw:
                grid_kw[key] = kw[key]

        # Default to 1px horizontal padding
        if not "ipadx" in grid_kw:
            grid_kw["ipadx"] = 1

        # Default to making all corners sticky
        if not "sticky" in grid_kw:
            grid_kw["sticky"] = "nsew"

        # Add the widget to the grid
        widget.grid(row=self._row, column=self._col, **grid_kw)

        # Store a reference to the widget
        self._cells[self._row].append(widget)

        # Pad self._cells if the widget spans multiple columns
        if "columnspan" in grid_kw:
            for _ in range(1, kw["columnspan"]):
                self._cells[self._row].append(None)

        # Bind the up and down arrow keys
        if self._enable_arrow_keys and self._row >= 1:
            try:
                # Identify the widget above this one
                upper = self._cells[self._row - 1][self._col]

                if upper:
                    # Up arrow navigates from widget to upper
                    widget.bind("<Up>",
                                lambda event, upper=upper, lower=widget:
                                self._navigate_up(upper, lower, event))

                    # Down arrow navigates from upper to widget
                    upper.bind("<Down>",
                               lambda event, upper=upper, lower=widget:
                               self._navigate_down(upper, lower, event))

            except (IndexError, tk.TclError):
                # Couldn't bind the arrow keys
                pass

        # Bind the left and right arrow keys
        if self._enable_arrow_keys and self._col >= 1:
            try:
                # Identify the widget left of this one
                left = self._cells[self._row][self._col - 1]

                if left:
                    # Left arrow navigates from widget to left
                    widget.bind("<Left>",
                                lambda event, left=left, right=widget:
                                self._navigate_left(left, right, event))

                    # Right arrow navigates from left to widget
                    left.bind("<Right>",
                              lambda event, left=left, right=widget:
                              self._navigate_right(left, right, event))

            except (IndexError, tk.TclError):
                # Couldn't bind the arrow keys
                pass

        # Increment the grid column
        if "columnspan" in grid_kw:
            self._col += grid_kw["columnspan"]
        else:
            self._col += 1

        # Check if this is the longest row we've added, and if it is,
        # store its length for later reference
        if self._col > self._row_max:
            self._row_max = self._col

        # Set the default foreground/background colors
        if do_colorize:
            self._colorize(widget)

        # Return the new widget
        return widget

    def _colorize(self, widget, **kw):
        """Colorize the specified widget.

        This function is used to implement shading alternate rows.
        The "fg"/"foreground" and "bg"/"background" keyword arguments
        will override the MagicGrid's default colors.
        """

        if not self._shade_rows:
            return

        try:
            if not ("fg" in kw or "foreground" in kw):
                if self._row % 2 == 0:
                    widget.configure(foreground=self._fg_shade)
                else:
                    widget.configure(foreground=self._fg_color)

            if not ("bg" in kw or "background" in kw):
                if self._row % 2 == 0:
                    widget.configure(background=self._bg_shade)
                else:
                    widget.configure(background=self._bg_color)

        except (tk.TclError):
            # Silently ignore Tcl/Tk errors. This is mostly to avoid
            # trouble when adding ttk widgets, which don't support changing
            # colors this way (and will raise an exception if you try).
            pass

    # ------------------------------------------------------------------------

    def _navigate_up(self, upper, lower, event=None):
        """Move keyboard focus to the cell above."""

        # Spinbox widgets already use the up and down arrow keys
        if not isinstance(lower, tk.Spinbox):
            upper.focus_set()

        # Sync the insert position for text entry widgets
        if hasattr(lower, "index") and hasattr(upper, "icursor"):
            if lower.index("insert") == lower.index("end"):
                upper.icursor("end")
            else:
                upper.icursor(lower.index("insert"))

    def _navigate_down(self, upper, lower, event=None):
        """Move keyboard focus to the cell below."""

        # Spinbox widgets already use the up and down arrow keys
        if not isinstance(upper, tk.Spinbox):
            lower.focus_set()

        # Sync the insert position for text entry widgets
        if hasattr(upper, "index") and hasattr(lower, "icursor"):
            if upper.index("insert") == upper.index("end"):
                lower.icursor("end")
            else:
                lower.icursor(upper.index("insert"))

    def _navigate_left(self, left, right, event=None):
        """Move keyboard focus to the cell to the left."""

        should_move = False
        if hasattr(right, "index"):
            # Only move if the cursor is at the far left of the textbox
            if right.index("insert") == right.index(0):
                should_move = True

        else:
            # Presume it's safe to move from other widgets
            should_move = True

        if should_move:
            # Move to the left
            left.focus_set()

            # If the left-hand widget accepts text entry, move the
            # insertion point to its far right
            if hasattr(left, "icursor"):
                left.icursor("end")

    def _navigate_right(self, left, right, event=None):
        """Move keyboard focus to the cell to the right."""

        should_move = False
        if hasattr(left, "index"):
            # Only move if the cursor is at the far right of the textbox
            if left.index("insert") == left.index("end"):
                should_move = True

        else:
            # Presume it's safe to move from other widgets
            should_move = True

        if should_move:
            # Move to the right
            right.focus_set()

            # If the right-hand widget accepts text entry, move the
            # insertion point to its far left
            if hasattr(right, "icursor"):
                right.icursor(0)

    # ------------------------------------------------------------------------

    # Default colors for ordinary rows
    _DEFAULT_BG_COLOR = "white"
    _DEFAULT_FG_COLOR = "black"

    # Default colors for header rows
    _DEFAULT_BG_HEADER = "SteelBlue"
    _DEFAULT_FG_HEADER = "white"

    # Default colors for shading alternate rows
    _DEFAULT_BG_SHADE = "LightSteelBlue"
    _DEFAULT_FG_SHADE = "black"

    # Keyword arguments used by grid()
    _GRID_KEYS = ("column", "columnspan", "in_",
                  "ipadx", "ipady", "padx", "pady",
                  "row", "rowspan", "sticky")

    # Keyword arguments used by grid_columnconfigure() and grid_rowconfigure()
    _GRID_COLUMN_ROW_KEYS = "minsize", "pad", "weight"
