import os  # Filesystem helper library used across this program to interact with the operating system's file API.
            # - Provides functions like listdir(), path.join(), path.splitext() and others.
            # -  Os is used to find CSV files in a folder, build full paths from directory + filename, and split file extensions.
            # - Keeping this import at top makes these utilities available throughout the module.

import csv  # The CSV module parses and writes comma-separated files.
           # - csv.DictReader and csv.reader is used to read CSV rows either as dictionaries (header-aware) or plain lists.
           # - csv.writer is also used to write rows back when saving inserted data.
           # - Using the csv module ensures platform-consistent parsing (commas, quoting, newlines).

import tkinter as tk  # Tkinter is Python's standard GUI toolkit. As 'tk' is conventional and shortens code.
                     # - This import gives us widgets, and event loop.
                     # - We build the application's GUI using Tk and child widgets created from this module.

from tkinter import ttk, filedialog, messagebox  # Convenience/Stylistic imports from tkinter:
                                                 # - ttk: modern themed widgets (better visuals than classic Tk widgets).
                                                 # - filedialog: dialogs for open/save file and directory selection.
                                                 # - messagebox: simple dialogs for info/warning/error prompts.
                                                 # These are used in several UI actions (load/save, popups).

from datetime import datetime  # Datetime functionality for parsing, constructing and formatting timestamps.
                              # - datetime.fromisoformat and datetime.strptime are used to parse user/file timestamps.
                              # - datetime.now is used when an inserted row has no timestamp (auto-fills the current time).
                              # - Storing timestamps as datetime objects lets us later format or convert for plotting.

import numpy as np  # NumPy is used for numeric arrays, NaN representation, and vectorized statistics.
                   # - np.nan is used to represent missing numeric values consistently.
                   # - We use numpy arrays to compute mean/std/min/max quickly on collected numeric lists.
                   # - Using NumPy keeps operations efficent. 

import matplotlib.pyplot as plt  # Matplotlib's pyplot module is used to create figures and axes for plotting.
                                # - We create Figure and Axes objects for time series, histograms, and scatter plots.
                                # - Matplotlib is the plotting backend used inside Tk windows via FigureCanvasTkAgg.

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Adapter to embed Matplotlib figures in Tkinter windows.
                                                                  # - FigureCanvasTkAgg wraps a Matplotlib Figure so it can be attached to a Tk widget.
                                                                  # - This is how plot windows are integrated into the GUI rather than opened as separate Matplotlib windows.

# Fields that summarise will be computed for:
SENSOR_FIELDS = ('temperature', 'humidity', 'light')  # A tuple of field names the rest of the program expects.
                                                     # - Used by compute_summaries to iterate over which sensor statistics to compute.
                                                     # - Used by plotting code to know what arrays to look for.
                                                     # - Keeping a single constant avoids mismatches caused by typos elsewhere in my code.


# Minimal CSV reader
def read_csv_file(filepath):  # Defines the function that reads a single CSV file and returns a list of normalized row dicts.
                              # - Parameter: filepath (string), the path to the CSV file to parse.
                              # - Returns: a list where each element is a dict with constant keys:
                              #   'timestamp' (datetime or None), 'greenhouse' (string), 'temperature' (float/NaN),
                              #   'humidity' (float/NaN), 'light' (float/NaN).
                              # - The function tries a header-aware parse first (csv.DictReader) and falls back to column-based parse.

    rows = []  # Initialises an empty list to collect parsed/normalized row dicts from the file.
               # - I append a costant dict per input row so code below can rely on consistent keys and types.

    with open(filepath, newline='') as f:  # Opens the file using a context manager "with" (which ensures the file is closed automatically).
                                           # - newline='' is used for the csv module to handle universal newlines correctly.
                                           # - 'f' is the file object visible inside this block only. Defining it as such improves efficency and readability. 
        reader = csv.DictReader(f)  # Creates a DictReader that will interpret the first non-empty row as header names.
                                    # - DictReader yields an OrderedDict per row. 
                                    # - This enables header-aware parsing so we can accept different column orders.

        fieldnames = reader.fieldnames or []  # Grabs the header names detected by DictReader; if none, use an empty list.
                                              # - Using "or []" (Empty List) avoids NoneType errors in subsequent code when there are no headers.

        norm_fieldnames = [fn.lower().strip() for fn in fieldnames if fn]
        # - This is a list comprehension that iterates over each header string (fn) in fieldnames.
        # - For each header: fn.lower() converts all letters to lowercase so matching is case-insensitive.
        # - .strip() removes leading/trailing whitespace so headers like " temperature " are handled.
        # - The "if fn" filters out falsy header values (e.g., None or empty strings) so we don't process invalid headers.
        # - The result (norm_fieldnames) is a cleaned list of header names used to decide how to parse the file.

        expected_tokens = {'timestamp', 'temperature', 'temp', 'humidity', 'hum',
                           'light', 'lux', 'greenhouse', 'gh', 'light_intensity'}
        # A set of substrings we expect to find in the headers within the CSV file that contains our sensor/timestamp data.
        # - We include common synonyms ('temp' for 'temperature', 'lux' for 'light') so small differences in CSV headers dosen't break detection.

        header_has_expected = any(any(tok in fn for tok in expected_tokens) for fn in norm_fieldnames)
        # - Outer any(...) iterates over each normalized header name (fn).
        # - For each fn, inner any(tok in fn for tok in expected_tokens) checks whether any of our expected tokens appear inside that header string.
        # - If any header contains any expected token, header_has_expected becomes True.
        # - This helps decide whether to use the header-aware DictReader parsing (if True) or a fallback positional parse (if False).

    if header_has_expected:  # If the header detection found expected tokens, parse the file in header-aware mode.
        with open(filepath, newline='') as f:  # Re-open the file so we can iterate from the beginning again with DictReader.
                                           # - Re-opening is simpler than rewinding the file object and ensures we read rows fresh.
            reader = csv.DictReader(f)  # Creates a new DictReader to iterate rows now that we've committed to header-aware parsing.
            for r in reader:  # Iterates each row produced by DictReader; r is a dictionary mapping header.
                if not any((v and str(v).strip()) for v in r.values()):
                    # - r.values() are the cell values for the row (They may be strings or None).
                    # - The generator (v and str(v).strip()) returns a truthy trimmed string if v exists and isn't just whitespace.
                    # - any(...) returns True if at least one cell contains non-whitespace content.
                    # -  The test is negated and 'continue's when the entire row is empty or contains only whitespace values.
                    # - This avoids creating meaningless rows for blank lines in CSVs.

                    continue  # Skips processing for empty rows; moves to next row in the file.

                row = {k.strip().lower(): v.strip() if isinstance(v, str) else v for k, v in r.items()}
                # - r.items() yields (header_name, cell_value) pairs with the original header strings as keys.
                # -   A new dict 'row' is created where each key is header_name.lower().strip() to make key lookup case insensitive and whitespace flexible.
                # - For values: if the value is a string we call .strip() to remove accidental spaces; non-strings are passed through unchanged.
                # - This normalized row makes downstream parsing simpler: we can get('temperature') or get('temp') without worrying about capitalization.

                timestamp = None  # Initializes the timestamp variable; where it will attempt to parse below.
                                  # - Setting to None explicitly clarifies that a missing/unparseable timestamp is represented as None.

                if 'timestamp' in row and row['timestamp']:
                    # If there is a 'timestamp' key and it has a non-empty value, try to parse it into a datetime object.
                    # - datetime.fromisoformat is perfered, which handles standard ISO formats quickly.
                    try:
                        timestamp = datetime.fromisoformat(row['timestamp'])
                        # datetime.fromisoformat parses strings in ISO-8601-like formats such as:
                        # - 'YYYY-MM-DD' and 'YYYY-MM-DDTHH:MM:SS' and variations.
                        # - Using ISO parsing first handles many automated sensor timestamp formats.
                    except Exception:
                        # If fromisoformat fails (string isn't ISO or is malformed), try a common custom format next.
                        try:
                            timestamp = datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S')
                            # strptime with format '%Y-%m-%d %H:%M:%S' matches '2020-01-31 23:59:59' which is a common export format.
                        except Exception:
                            timestamp = None  # If parsing fails completely, leave timestamp as None (treat as missing).

                greenhouse = row.get('greenhouse', row.get('gh', 'unknown'))
                # -  Tries canonical key 'greenhouse' first.
                # - If not found, fallback to a common synonym 'gh'.
                # - If neither exists, default to the string 'unknown' so the field is never None (helps later when saving/displaying).

                try:
                    temp = float(row.get('temperature', row.get('temp', 'nan')))
                    # Trying to convert temperature to a float using canonical key 'temperature' then synonym 'temp'.
                    # - If both are missing row.get(..., 'nan') returns the string 'nan', and float('nan') yields np.nan-like float nan.
                except Exception:
                    temp = np.nan  # If Conversion fails (non-numeric string, empty, etc.), set to NumPy NaN for consistent numeric missingness.

                try:
                    hum = float(row.get('humidity', row.get('hum', 'nan')))
                    # Converts humidity similarly using canonical and synonym keys.
                except Exception:
                    hum = np.nan  # Uses NumPy NaN when conversion fails.

                try:
                    light_raw = row.get('light', row.get('light_intensity', row.get('lux', 'nan')))
                    # For light we check multiple possible header names and choose the first that exists.
                    light = float(light_raw)  # Converts the selected string to a float.
                except Exception:
                    light = np.nan  # If conversion fails or value is missing, use NaN.

                rows.append({'timestamp': timestamp, 'greenhouse': greenhouse,
                             'temperature': temp, 'humidity': hum, 'light': light})
                # Appends a canonical dict to rows so every stored row has the same keys and types:
                # - 'timestamp' is either datetime or None
                # - 'greenhouse' is a string
                # - numeric fields are floats or np.nan

        return rows  # Returns the list of parsed rows when header-aware parsing was used.

    # If it reaches this point, the heuristic didn't find expected header tokens.
    # Now fall back to header-less parsing using csv.reader which returns lists of columns per row.
    with open(filepath, newline='') as f:  # Open the file again for fallback parsing mode.
        reader = csv.reader(f)  # csv.reader yields each row as a list of column strings.
        for cols in reader:  # Iterate every row list returned by csv.reader.
            if not cols or all((c is None or str(c).strip() == '') for c in cols):
                # Skip rows that are entirely empty or contain only whitespace values.
                # - 'cols' can be empty (no columns) or have values that are None/whitespace.
                # - all(...) returns True when every column is effectively empty, so we continue to the next row.
                continue

            cols = [c.strip() for c in cols]  # Strip whitespace from each column string to clean the data.
                                              # - This removes leading/trailing spaces from values like "  23.5  ".

            # pad to 5
            while len(cols) < 5:
                cols.append('')  # If a row has fewer than 5 columns, append empty strings so the unpack below won't fail.
                                # - This supports files where some rows are missing trailing values but still keep column positions stable.

            ts_raw, greenhouse, temp_raw, hum_raw, light_raw = cols[:5]
            # Unpacks the first five columns into specific variables.
            # - ts_raw: raw timestamp string (may be empty)
            # - greenhouse: greenhouse id field (may be empty)
            # - temp_raw, hum_raw, light_raw: raw numeric strings for sensors (may be empty)

            timestamp = None  # Default timestamp to None before trying to parse.

            if ts_raw:  # Only tries parsing if ts_raw is a non-empty string.
                try:
                    timestamp = datetime.fromisoformat(ts_raw)  # Tries ISO parsing first for robustness.
                except Exception:
                    try:
                        timestamp = datetime.strptime(ts_raw, '%Y-%m-%d %H:%M:%S')
                        # If ISO parsing fails, try the common 'YYYY-MM-DD HH:MM:SS' format as fallback.
                    except Exception:
                        timestamp = None  # If both attempts fail, keep timestamp as None to indicate missing/unparseable.

            try:
                temp = float(temp_raw) if temp_raw != '' else np.nan
                # Converts temperature string to float if non-empty; otherwise use NaN to represent missing numeric.
            except Exception:
                temp = np.nan  # If conversion throws, use NaN.

            try:
                hum = float(hum_raw) if hum_raw != '' else np.nan
                # Converts humidity string to float if non-empty; otherwise NaN.
            except Exception:
                hum = np.nan  # On conversion failure use NaN.

            try:
                light = float(light_raw) if light_raw != '' else np.nan
                # Converts light string to float if non-empty; otherwise NaN.
            except Exception:
                light = np.nan  # On conversion failure use NaN.

            rows.append({'timestamp': timestamp, 'greenhouse': greenhouse or 'unknown',
                         'temperature': temp, 'humidity': hum, 'light': light})
            # Appends a normalized dictionary with canonical keys to rows.
            # - greenhouse or 'unknown' ensures greenhouse is never an empty string but at least 'unknown' if missing.

    return rows  # Returns the parsed rows collected from the fallback column-based parsing.


def read_all_csv_in_dir(dirpath):  # Reads and combine rows from all CSV files in a directory.
    # - Parameter: dirpath (string) path of a directory to scan.
    # - Returns: a combined list of normalized rows from every CSV in the directory.
    combined = []  # Initializes an accumulator list to which we will extend rows from each CSV file we find.

    for fname in os.listdir(dirpath):  # Uses os.listdir to iterate every entry name in the target directory.
        # os.listdir returns filenames (not full paths), so we join them with the directory below.
        if fname.lower().endswith('.csv'):  # Processes only files whose names end with '.csv' (case-insensitive).
            full = os.path.join(dirpath, fname)  # Builds the absolute or relative path to the file by joining dirpath and filename.
            try:
                combined.extend(read_csv_file(full))  # Reads the CSV file and extend combined with its rows (list concatenation).
            except Exception as e:
                print(f"Failed to read {full}: {e}")  # If reading a file fails, print an error message and continue with others.
                # - There is no raise here so a single bad CSV won't stop the whole directory load operation.

    return combined  # Returns the combined list of rows from all CSV files that were successfully read.


# Summaries & conversion
def compute_summaries(rows):  # Computes basic statistics (count, mean, std, min, max) for each field in SENSOR_FIELDS.
    """
    For each field in SENSOR_FIELDS compute: count, mean, std, min, max.
    Non-numeric or missing values are ignored.
    """
    summaries = {}  # Dictionary to hold summary statistics per sensor field.

    for field in SENSOR_FIELDS:  # Iterates the canonical fields, e.g., 'temperature', 'humidity', 'light'.
        vals = []  # Collects numeric values for this field across all rows here.

        for r in rows:  # Iterates over each normalized row dict passed to the function.
            try:
                v = r.get(field, np.nan)  # Tries to retrieve the value for the field, default to np.nan if missing.
                vf = float(v)  # Attempts to coerce the value to a Python float.
                if np.isfinite(vf):  # Checks that the result is a finite number (not NaN or +/-inf).
                    vals.append(vf)  # Only appends finite numeric values so NaNs and infinities are excluded.
            except Exception:
                # If any error occurs (e.g., v is a non-numeric string), we silently skip that row for this metric.
                continue

        if len(vals) == 0:  # If no valid numeric values were found for this field:
            summaries[field] = {'count': 0, 'mean': np.nan, 'std': np.nan, 'min': np.nan, 'max': np.nan}
            # - Use np.nan for numeric stats to indicate 'no data' consistently with how missing numbers are represented elsewhere.
        else:
            arr = np.array(vals, dtype=float)  # Converts the collected list to a NumPy array for efficient stats.
            summaries[field] = {
                'count': int(arr.size),  # Number of valid numeric values included in calculations.
                'mean': float(np.mean(arr)),  # Arithmetic mean of the collected values.
                'std': float(np.std(arr, ddof=0)),  # Population standard deviation (ddof=0). Use ddof=1 for sample std if desired.
                'min': float(np.min(arr)),  # Minimum value observed.
                'max': float(np.max(arr))  # Maximum value observed.
            }

    return summaries  # Returns the mapping field and statistics dict so callers can display or save the results.


def rows_to_numpy(rows):  # Converts normalized row dicts into arrays suitable for plotting and numeric operations.
    """Return times (list) and numpy arrays for temperature, humidity, light."""
    # - times is a Python list preserving original order; elements are either datetime objects or None for missing timestamps.
    # - temps, hums, lights are NumPy arrays of dtype float where missing values are represented by np.nan.
    times = [r.get('timestamp') if r.get('timestamp') is not None else None for r in rows]
    # - This comprehension produces an ordered list of timestamp objects or None to preserve row alignment with numeric arrays.

    temps = np.array([r.get('temperature', np.nan) for r in rows], dtype=float)
    # - Creates a NumPy float array of temperature values; r.get('temperature', np.nan) yields numeric or np.nan for missing.

    hums = np.array([r.get('humidity', np.nan) for r in rows], dtype=float)
    # - Similar conversion for humidity.

    lights = np.array([r.get('light', np.nan) for r in rows], dtype=float)
    # - Similar conversion for light sensor values.

    return times, temps, hums, lights  # Returns tuple of times list and three numeric arrays in the canonical order expected by plots.


# GUI Application
class CowApp(tk.Tk):  # Main application class; inherits from Tk so an instance represents the main window and event loop.
    def __init__(self):  # Constructor builds the UI and initializes shared state.
        super().__init__()  # Initializes the base Tk class which creates a new main window and initializes Tk resources.

        self.title('Big Cow')
        # - Sets the title shown in the window manager and at the top of the window.
        # - This is cosmetic but helpful for the user to identify the application window.

        self.geometry('900x600')
        # - Sets a default window size (width x height in pixels).
        # - This makes the initial layout predictable; users can still resize the window.

        self.inserted_rows = []  
        # - A list stored on the app instance that will hold rows created via the InsertTab.
        # - Storing this on the app allows different tabs to access and manipulate the same dataset.

        notebook = ttk.Notebook(self)
        # - Creates a Notebook widget which provides a tabbed interface for organizing different functional parts of the app.

        notebook.pack(fill='both', expand=True)
        # - Packs the notebook into the main window and allow it to expand so the tabs take available space.

        self.insert_tab = InsertTab(notebook, self)
        # - Constructs the InsertTab (frame) and pass the notebook (parent) so it appears as a tab.
        # - Passes 'self' so the tab can read/modify shared state like inserted_rows.

        self.process_tab = ProcessTab(notebook, self)
        # - Constructs the ProcessTab for file loading and summarising.

        self.graph_tab = GraphTab(notebook, self)
        # - Constructs the GraphTab for plotting capabilities.

        notebook.add(self.insert_tab, text='Insert Data')
        # - Ads the InsertTab to the notebook UI with the tab label 'Insert Data'.

        notebook.add(self.process_tab, text='Process Data')
        # - Adds the ProcessTab to the notebook with label 'Process Data'.

        notebook.add(self.graph_tab, text='View Graphs')
        # - Adds the GraphTab with label 'View Graphs' so users can switch between app sections by clicking tabs.


# Insert Tab
class InsertTab(tk.Frame):  # Frames responsible for manual data entry (inserting rows through the GUI).
    def __init__(self, parent, app: CowApp):  # parent is the notebook tab container; app is the main application instance.
        super().__init__(parent)  # Initializes base Frame widget with the notebook as parent.
        self.app = app  # Saves reference to the main app so we can append rows to app.inserted_rows and trigger shared behavior.

        form = ttk.Frame(self)
        # - A sub-frame to neatly group form controls (labels/entries/buttons).
        # - Using a frame makes layout management clearer and easier to adjust.

        form.pack(side='top', fill='x', padx=10, pady=10)
        # - Places the form at the top of the tab and allow horizontal expansion, with padding to separate from edges.

        ttk.Label(form, text='Greenhouse:').grid(row=0, column=0, sticky='e')
        # - Label for the greenhouse entry using grid at row 0, column 0; sticky='e' aligns it to the right of the grid cell.

        self.greenhouse_var = tk.StringVar(value='GH-1')
        # - A StringVar stores the entry's text state; initializing with 'GH-1' provides a sensible default greenhouse id.

        ttk.Entry(form, textvariable=self.greenhouse_var).grid(row=0, column=1)
        # - An Entry widget bound to greenhouse_var; editing the Entry updates greenhouse_var automatically.

        ttk.Label(form, text='Timestamp (ISO or YYYY-MM-DD HH:MM:SS) leave blank:').grid(row=1, column=0, sticky='e')
        # - Label describing acceptable timestamp formats; telling the user they can leave it blank triggers auto-now behavior.

        self.timestamp_var = tk.StringVar()
        # - StringVar for the timestamp entry; left empty by default so we can use datetime.now() when blank.

        ttk.Entry(form, textvariable=self.timestamp_var, width=40).grid(row=1, column=1, columnspan=2, sticky='w')
        # - A wider Entry for timestamp input that spans multiple grid columns for readability.

        ttk.Label(form, text='Temperature (C):').grid(row=2, column=0, sticky='e')
        # - Label for temperature input indicating units (Celsius) to avoid confusion.

        self.temp_var = tk.StringVar()
        # - StringVar holds the user-entered temperature so we can attempt to convert it to float later.

        ttk.Entry(form, textvariable=self.temp_var).grid(row=2, column=1)
        # - Entry widget for temperature bound to temp_var.

        ttk.Label(form, text='Humidity (%):').grid(row=3, column=0, sticky='e')
        # - Label for humidity with percent sign to indicate units.

        self.hum_var = tk.StringVar()
        # - StringVar for humidity entry.

        ttk.Entry(form, textvariable=self.hum_var).grid(row=3, column=1)
        # - Entry widget for humidity bound to hum_var.

        ttk.Label(form, text='Light (lux):').grid(row=4, column=0, sticky='e')
        # - Label for light input specifying lux as the unit.

        self.light_var = tk.StringVar()
        # - StringVar for light entry.

        ttk.Entry(form, textvariable=self.light_var).grid(row=4, column=1)
        # - Entry widget for light bound to light_var.

        ttk.Button(form, text='Insert Row', command=self.insert_row).grid(row=5, column=0, pady=6)
        # - Button that triggers self.insert_row when clicked to convert form inputs into a normalized row and store it.

        ttk.Button(form, text='Clear Inputs', command=self.clear_inputs).grid(row=5, column=1)
        # - Button to clear the form fields via clear_inputs method.

        sort_frame = ttk.Frame(self)  # Create a frame to host sorting controls and save button.
        sort_frame.pack(side='top', fill='x', padx=10, pady=8)
        # - Packs near the top under the form so these controls are grouped visually.

        ttk.Label(sort_frame, text='Sort before saving:').pack(side='left')
        # - Explain the sort behavior: the user can request the inserted rows be sorted by specified metrics before saving.

        self.sort_options = ('Lowest Humidity', 'Highest Humidity', 'Lowest Temperature', 'Highest Temperature')
        # - A tuple of human-readable sort option labels.

        self.sort_var = tk.StringVar(value=self.sort_options[0])
        # - StringVar to hold the selected sort option; default to the first option to avoid None.

        ttk.Combobox(sort_frame, values=self.sort_options, textvariable=self.sort_var, state='readonly').pack(side='left', padx=6)
        # - Combobox shows allowed sort options; using state='readonly' prevents the user from typing arbitrary values.

        ttk.Button(sort_frame, text='Save Inserted Data', command=self.save_inserted).pack(side='left', padx=8)
        # - Button to save the inserted data to a file; applies the selected sort first.

        ttk.Button(sort_frame, text='Clear All Inserted', command=self.clear_all_inserted).pack(side='left', padx=8)
        # - Button to clear all inserted rows after user confirmation.

        bottom = ttk.Frame(self)  # Frame to hold the listbox showing inserted rows and related control(s).
        bottom.pack(fill='both', expand=True, padx=10, pady=10)
        # - This bottom area expands to fill remaining space so the listbox can grow.

        ttk.Label(bottom, text='Inserted rows (most recent at bottom):').pack(anchor='w')
        # - A short label above the listbox explaining the display order.

        self.listbox = tk.Listbox(bottom, height=10)
        # - The Listbox displays the rows inserted via the form; height sets how many lines are visible by default.

        self.listbox.pack(fill='both', expand=True)
        # - Packs the listbox so it expands to use the bottom frame.

        ttk.Button(bottom, text='Return Selected Values', command=self.return_selected).pack(pady=6)
        # - Button to open a dialog showing the currently selected listbox entries (useful for copying or inspection).

    def insert_row(self):  # Convert form entries into a canonical row and append to the app-wide inserted_rows list.
        gh = self.greenhouse_var.get().strip()
        # - Reads greenhouse text and strip whitespace to normalize user input. 
        # - Using strip ensures stored values don't contain accidental leading/trailing spaces.

        tstr = self.timestamp_var.get().strip()
        # - Reads raw timestamp string the user typed (may be empty) and strip whitespace.

        if tstr == '':
            ts = datetime.now()
            # - If no timestamp provided, use current local time so every inserted row has at least a timestamp.
        else:
            try:
                ts = datetime.fromisoformat(tstr)
                # - Tries parsing an ISO-like string first (handles many standard formats).
            except Exception:
                try:
                    ts = datetime.strptime(tstr, '%Y-%m-%d %H:%M:%S')
                    # - Fallsback to the common 'YYYY-MM-DD HH:MM:SS' format if fromisoformat fails.
                except Exception:
                    messagebox.showerror('Error', 'Unrecognized timestamp format. Use ISO or YYYY-MM-DD HH:MM:SS')
                    # - If parsing fails, notify the user with an error dialog explaining accepted formats.
                    return  # Abort insertion since the timestamp was provided but unparseable.

        try:
            temp = float(self.temp_var.get())
            # - Tries to convert the temperature string to float. This will raise if the string is invalid.
        except Exception:
            temp = np.nan  # Uses NaN to represent missing/invalid numeric input; keeps numeric semantics consistent elsewhere.

        try:
            hum = float(self.hum_var.get())
        except Exception:
            hum = np.nan  # Same rationale as temperature: prefer NaN over exceptions for invalid user input.

        try:
            light = float(self.light_var.get())
        except Exception:
            light = np.nan  # Same rationale for light sensor.

        row = {'timestamp': ts, 'greenhouse': gh, 'temperature': temp, 'humidity': hum, 'light': light}
        # - Builds a canonical dict representing the row with consistent keys expected throughout the app.
        # - Uses canonical keys avoids branching logic elsewhere when reading fields by name.

        self.app.inserted_rows.append(row)
        # - Appends the row to the shared list on the app instance so other tabs (ProcessTab/GraphTab) can access it.

        display_tuple = (ts.isoformat(sep=' '), gh, temp, hum, light)
        # - Builds a human-readable tuple for the listbox; isoformat with space produces 'YYYY-MM-DD HH:MM:SS' like text.

        self.listbox.insert('end', str(display_tuple))
        # - Inserts the string representation of the tuple into the listbox at the end so the newest item shows last.

        messagebox.showinfo('Inserted', 'Row inserted successfully.')
        # - Gives the user confirmation that their action succeeded; useful feedback for beginners.

    def clear_inputs(self):  # Resets the input StringVars in the form to empty strings.
        self.temp_var.set('')  # Clears temperature field so the form is ready for new input.
        self.hum_var.set('')  # Clears humidity field.
        self.light_var.set('')  # Clears light field.
        self.timestamp_var.set('')  # Clears timestamp field.

    def save_inserted(self):  # Saves inserted rows to a file with optional sorting specified by the user.
        rows = list(self.app.inserted_rows)
        # - Makes a shallow copy so we can sort without changing the original list ordering in-memory.
        # - This avoids surprising side effects if other parts of the code expect original insertion order.

        if not rows:
            messagebox.showwarning('No data', 'There is no inserted data to save.')
            return  # Nothing to save; inform user and abort.

        option = self.sort_var.get()  # Reads the human-readable sort option chosen by the user.

        if option == 'Lowest Humidity':
            rows.sort(key=lambda r: (np.nan if np.isnan(r['humidity']) else r['humidity']))
            # - Sorts ascending by humidity, but push NaNs to the front by converting NaN to np.nan (preserve NaN behavior).
        elif option == 'Highest Humidity':
            rows.sort(key=lambda r: (np.nan if np.isnan(r['humidity']) else -r['humidity']))
            # - Sorts by negative humidity so largest humidity values come first; NaNs handled similarly.
        elif option == 'Lowest Temperature':
            rows.sort(key=lambda r: (np.nan if np.isnan(r['temperature']) else r['temperature']))
            # - Sorst ascending by temperature.
        elif option == 'Highest Temperature':
            rows.sort(key=lambda r: (np.nan if np.isnan(r['temperature']) else -r['temperature']))
            # - Sorts descending by temperature via negation.

        fpath = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV files', '*.csv'), ('Text files', '*.txt')])
        # - Asks the user where to save the file and what name to give it.
        # - defaultextension ensures the saved file has .csv by default; user may override.

        if not fpath:
            return  # User cancelled the save dialog; do nothing.

        base, ext = os.path.splitext(fpath)
        # - Splits the returned path into base and extension so we can decide save format behavior.

        ext = ext.lower()  # Normalize extension to lowercase for reliable comparisons like '.CSV' vs '.csv'.

        if ext == '.csv':
            with open(fpath, 'w', newline='') as f:
                writer = csv.writer(f)  # Use csv.writer to produce proper CSV formatting (quoting, commas).
                writer.writerow(['timestamp', 'greenhouse', 'temperature', 'humidity', 'light'])
                # - Writes a canonical header row so the file is self-describing and can be re-loaded by our header-aware path.
                for r in rows:
                    ts = r['timestamp'].isoformat(sep=' ') if r['timestamp'] else ''
                    # - Converts datetime to human-readable string if present; use empty string when missing.

                    writer.writerow([ts, r['greenhouse'], r['temperature'], r['humidity'], r['light']])
                    # - Writes each row in the canonical column order to keep output consistent and easy to parse later.
        else:
            # If user picked a non-CSV extension (e.g., .txt) write a tab-separated file that's still human readable.
            with open(fpath, 'w') as f:
                for r in rows:
                    ts = r['timestamp'].isoformat(sep=' ') if r['timestamp'] else ''
                    f.write("{}\t{}\t{}\t{}\t{}\n".format(ts, r['greenhouse'], r['temperature'], r['humidity'], r['light']))
                    # - Use \t to separate fields; this is simple and often opened correctly by text editors and spreadsheets.

        messagebox.showinfo('Saved', f'Saved {len(rows)} rows to {fpath}')
        # - Informs how many rows were saved and where; good user feedback for verification.

    def return_selected(self):  # Shows the selected listbox items in a new read-only window.
        sel = self.listbox.curselection()
        # - curselection returns a tuple of selected indices (may be empty when nothing selected).

        if not sel:
            messagebox.showwarning('Select', 'Please select at least one row.')
            return  # If nothing is selected, prompt the user to choose something.

        values = [self.listbox.get(i) for i in sel]
        # - Builds a list of the selected items by retrieving them from the listbox by index.

        win = tk.Toplevel(self)  # Creates a new top-level window to display the values to the user.
        win.title('Returned Values')  # Title for the new window so it's clear what it contains.

        text = tk.Text(win, height=10, width=80)  # A Text widget allows multiline display and copy/paste.
        text.pack(fill='both', expand=True)

        for v in values:
            text.insert('end', v + '\n')  # Inserts each selected item followed by newline for clarity.

        text.config(state='disabled')  # Makes the Text widget read-only so the displayed values cannot be edited.

    def clear_all_inserted(self):  # Removes all inserted rows after getting explicit confirmation from the user.
        if not self.app.inserted_rows:
            messagebox.showinfo('No data', 'There are no inserted rows to clear.')
            return  # Nothing to do; inform the user.

        if not messagebox.askyesno('Confirm', 'Clear ALL inserted rows?'):
            return  # Ask for confirmation; abort if the user says No.

        self.app.inserted_rows.clear()  # Clears the list in-place so other references to this list see the change immediately.
        self.listbox.delete(0, 'end')  # Removes all entries from the visual listbox to reflect the cleared state.
        messagebox.showinfo('Cleared', 'All inserted rows have been cleared.')  # Notify the user the operation completed.


# Process Tab
class ProcessTab(tk.Frame):  # Frames for loading data files, processing rows, and displaying textual summaries.
    def __init__(self, parent, app: CowApp):
        super().__init__(parent)
        self.app = app  # Stores main app reference for access to inserted_rows if the user wants to process inserted data.

        top = ttk.Frame(self)  # Top area frame for action buttons like loading files.
        top.pack(fill='x', padx=10, pady=10)

        ttk.Button(top, text='Load CSV File', command=self.load_file).pack(side='left')
        # - Loads a single CSV file via file dialog and parse it using read_csv_file.

        ttk.Button(top, text='Load Directory (all CSVs)', command=self.load_directory).pack(side='left', padx=6)
        # - Loads all CSV files from a selected directory and combine them.

        ttk.Button(top, text='Process Inserted Data', command=self.process_inserted).pack(side='left', padx=6)
        # - Processes the rows that were manually inserted into the InsertTab (app.inserted_rows).

        self.loaded_rows = []  # Will hold rows loaded by load_file or load_directory for review/processing.

        mid = ttk.Frame(self)  # Middle area frame to display summary output text.
        mid.pack(fill='both', expand=True, padx=10, pady=10)

        ttk.Label(mid, text='Summary Output:').pack(anchor='w')  # Label above the text area.

        self.text = tk.Text(mid)  # Text widget where processed summaries and sample rows are shown.
        self.text.pack(fill='both', expand=True)

        bottom = ttk.Frame(self)  # Bottom area for saving the summary to a file.
        bottom.pack(fill='x', padx=10, pady=6)

        ttk.Button(bottom, text='Save Summary to File', command=self.save_summary).pack(side='left')
        # - Saves the content of the text widget to a .txt file via a save dialog.

    def load_file(self):  # Prompts the user to select one CSV file and load it.
        f = filedialog.askopenfilename(filetypes=[('CSV files', '*.csv'), ('All files', '*.*')])
        if not f:
            return  # User cancelled file selection.

        rows = read_csv_file(f)  # Parses the selected CSV; returns a list of normalized row dicts.
        self.loaded_rows = rows  # Save parsed rows locally for processing/display.
        messagebox.showinfo('Loaded', f'Loaded {len(rows)} rows from {f}')  # Notify how many rows were loaded.
        self.process_rows(self.loaded_rows)  # Automatically run processing to show immediate feedback.

    def load_directory(self):  # Prompts the user to select a directory and load all CSV files within it.
        d = filedialog.askdirectory()
        if not d:
            return  # User cancelled directory selection.

        rows = read_all_csv_in_dir(d)  # Reads all CSVs found in the directory and combine rows.
        self.loaded_rows = rows
        messagebox.showinfo('Loaded', f'Loaded {len(rows)} rows from CSVs in {d}')
        self.process_rows(self.loaded_rows)  # Show summaries of the combined dataset.

    def process_rows(self, rows):  # Computes summaries and display results in the text widget.
        if not rows:
            messagebox.showwarning('No data', 'No data to process.')
            return  # Nothing to process; inform the user.

        summaries = compute_summaries(rows)  # Computes numeric summaries for canonical sensor fields.

        out_lines = []  # Builds a list of strings we will insert into the text widget.
        out_lines.append(f'Rows processed: {len(rows)}')  # First line indicates the dataset size.

        for field, s in summaries.items():  # Format each field's summary into a readable line.
            out_lines.append(f"{field.title()}: count={s['count']}, mean={s['mean']:.3f}, std={s['std']:.3f}, min={s['min']}, max={s['max']}")
            # - field.title() makes 'temperature', 'Temperature' for nicer display.
            # - Numeric stats are formatted with a few decimal places for readability; min/max are printed as-is.

        out_lines.append('\nSample rows (first 15):')  # Adds a header before sample rows to show example data structure.

        for r in rows[:15]:  # Adds up to the first 5 rows; helpful to spot-check the parsed structure and values.
            out_lines.append(str(r))  # Convert the dict to a string and append so the user can visually inspect a few records.

        self.text.delete('1.0', 'end')  # Clears existing content in the summary Text widget.
        self.text.insert('end', '\n'.join(out_lines))  # Insert our assembled lines joined with newline characters.
        return summaries  # Returns the computed summaries so other code or tests can use them programmatically.

    def process_inserted(self):  # Convenience to run processing on rows manually inserted in the InsertTab.
        rows = list(self.app.inserted_rows)  # Copies current inserted rows and pass to process_rows.
        self.process_rows(rows)

    def save_summary(self):  # Saves the current content of the summary Text widget to a .txt or .csv file based off your choice.
        content = self.text.get('1.0', 'end').strip()  # Read the entire contents and strip trailing whitespace/newlines.
        if not content:
            messagebox.showwarning('No summary', 'There is no summary to save.')
            return  # Nothing to save; alert the user.

        f = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('Text File', '*.txt'), ('CSV File', '*.csv')])
        if not f:
            return  # User cancelled the save dialog.

        with open(f, 'w') as fh:
            fh.write(content)  # Writes the summary text to the selected file.
        messagebox.showinfo('Saved', f'Summary saved to {f}')  # Confirm success to the user.


# Graph Tab
class GraphTab(tk.Frame):  # Frames that offers graph selection and drawing capabilities embedded in Tk windows.
    def __init__(self, parent, app: CowApp):
        super().__init__(parent)
        self.app = app  # Saves the app reference so we can use inserted rows as a data source if requested.

        self.graph_options = [
            ('Temperature Time Series', 'temp_ts'),
            ('Humidity Time Series', 'hum_ts'),
            ('Light Time Series', 'light_ts'),
            ('Temperature Histogram', 'temp_hist'),
            ('Humidity Histogram', 'hum_hist'),
            ('Temperature vs Humidity (scatter)', 'temp_hum_scatter')
        ]
        # - Graph options are tuples of (label shown to user, internal key used by drawing functions).
        # - This pattern makes it easy to display a friendly name while mapping to program logic.

        top = ttk.Frame(self)  # Top area for load/use-inserted buttons.
        top.pack(fill='x', padx=10, pady=8)

        ttk.Button(top, text='Load CSV File', command=self.load_file).pack(side='left')
        # - Button to load CSV and set it as source for plotting.

        ttk.Button(top, text='Use Inserted Data', command=self.use_inserted).pack(side='left', padx=6)
        # - Button to use the rows manually inserted via the InsertTab.

        self.data_rows = []  # Local storage for the dataset to be plotted; can come from load_file or use_inserted.

        cb_frame = ttk.Frame(self)  # Frame to hold checkboxes for selecting which graphs to generate.
        cb_frame.pack(fill='x', padx=10)

        self.ch_vars = {}  # Dictionary mapping graph key, BooleanVar controlling each Checkbutton's state.

        for label, key in self.graph_options:
            var = tk.BooleanVar(value=False)  # Default unchecked so no accidental plotting.
            chk = ttk.Checkbutton(cb_frame, text=label, variable=var)  # Checkbutton binds to var so toggles update var.get().
            chk.pack(anchor='w')  # Packs each checkbutton on its own line, aligned left.
            self.ch_vars[key] = var  # Store the var so we can later query which graphs were selected.

        btn_frame = ttk.Frame(self)  # Frame for buttons that control generation mode (separate windows vs combined).
        btn_frame.pack(fill='x', padx=10, pady=8)

        ttk.Button(btn_frame, text='Generate Each in Separate Windows', command=self.generate_separate).pack(side='left')
        # - Creates a separate Toplevel window with its own Figure for each selected graph.

        ttk.Button(btn_frame, text='Generate All in One Window', command=self.generate_combined).pack(side='left', padx=8)
        # - Creates a single Toplevel window with subplots stacked vertically for each selected graph.

    def load_file(self):  # Use a file dialog to pick a CSV and parse it for plotting.
        f = filedialog.askopenfilename(filetypes=[('CSV files', '*.csv'), ('All files', '*.*')])
        if not f:
            return  # If user cancels, do nothing.

        self.data_rows = read_csv_file(f)  # Parse the CSV and set data_rows to the returned normalized row dicts.
        messagebox.showinfo('Loaded', f'Loaded {len(self.data_rows)} rows from {f}')
        # - Notify user how many rows will be available for plotting.

    def use_inserted(self):  # Use rows that were manually inserted via the InsertTab as the plotting dataset.
        self.data_rows = list(self.app.inserted_rows)  # Copy the inserted rows into local storage.
        messagebox.showinfo('Using Inserted', f'{len(self.data_rows)} inserted rows will be used for graphs')
        # - Inform the user how many rows will be used for graph generation.

    def _prepare_for_plot(self):  # Internal helper that turns normalized rows into x values and NumPy arrays for plotting.
        if not self.data_rows:
            messagebox.showwarning('No data', 'No data to plot.')
            return None  # Return None to signal no plotting should proceed.

        times, temps, hums, lights = rows_to_numpy(self.data_rows)
        # - Convert rows to a list of times and three numeric arrays for plotting convenience.

        if any(t is not None for t in times):  # If at least one timestamp exists, we prefer a date-based x-axis.
            try:
                import matplotlib.dates as mdates  # Import locally since date utilities are only needed when timestamps exist.
                xvals = [mdates.date2num(t) if t is not None else np.nan for t in times]
                # - Convert datetime objects to Matplotlib's internal floating point representation for dates.
                # - For missing timestamps we use np.nan to keep alignment with other arrays.

                dates_used = True  # Flag to indicate the x-axis values represent dates and should be formatted accordingly.
            except Exception:
                # If import or conversion fails for any reason fall back to integer indices for the x-axis.
                xvals = list(range(len(times)))
                dates_used = False
        else:
            # If No timestamps present in any row, use simple integer indices (row numbers) for the x-axis.
            xvals = list(range(len(times)))
            dates_used = False

        # Return a dict of prepared data to keep drawing functions simple and avoid recomputing conversions.
        return dict(x=xvals, dates_used=dates_used, times=times, temps=temps, hums=hums, lights=lights)

    def generate_separate(self):  # For each selected graph create a separate window with a single Matplotlib figure embedded.
        prepared = self._prepare_for_plot()
        if prepared is None:
            return  # If preparation failed, abort (a warning was already shown).

        selected = [k for k, v in self.ch_vars.items() if v.get()]
        # - Build a list of keys for graph types the user selected via checkboxes.

        if not selected:
            messagebox.showwarning('No graphs', 'Select at least one graph.')
            return  # If Nothing is selected warn user and abort.

        for key in selected:
            win = tk.Toplevel(self)  # Create a new top-level window for this plot so multiple can be open simultaneously.
            win.title(key)  # Use the graph key as the window title so the user can identify it.
            fig = plt.Figure(figsize=(6, 4))  # Create a Figure object sized for a single plot.
            ax = fig.add_subplot(111)  # Add one Axes to the Figure to draw on.

            self._draw_graph(ax, key, prepared)  # Draw the requested graph into the axes.

            canvas = FigureCanvasTkAgg(fig, master=win)  # Embed the Matplotlib figure into the Tk window.
            canvas.draw()  # Render the figure.
            canvas.get_tk_widget().pack(fill='both', expand=True)  # Pack the canvas widget to fill the Toplevel window.

    def generate_combined(self):  # Create one window with multiple vertically stacked subplots for all selected graphs.
        prepared = self._prepare_for_plot()
        if prepared is None:
            return

        selected = [k for k, v in self.ch_vars.items() if v.get()]
        if not selected:
            messagebox.showwarning('No graphs', 'Select at least one graph.')
            return

        win = tk.Toplevel(self)
        win.title('Combined Graphs')  # Title communicates that multiple graphs will be present.

        n = len(selected)  # Number of subplots required (one per selected graph).

        fig, axes = plt.subplots(nrows=n, ncols=1, figsize=(7, 4 * n))
        # - Create a figure with n rows and 1 column; figsize scales vertically with n.
        if n == 1:
            axes = [axes]  # When n==1 matplotlib returns a single Axes object; convert to list for uniform iteration.

        for ax, key in zip(axes, selected):
            self._draw_graph(ax, key, prepared)  # Draw each graph on its corresponding subplot.

        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)  # Embed and pack the combined figure.

    def _draw_graph(self, ax, key, prepared):  # Draw a specific graph type onto the provided Axes object.
        x = prepared['x']  # x is either date-formatted numeric values (if dates_used True) or integer indices.

        if key == 'temp_ts':
            ax.plot(x, prepared['temps'], label='Temperature (C)')  # Plot temperature time series.
            ax.set_ylabel('Temperature (C)')  # Label the y-axis to show units.
            ax.legend()  # Show a legend identifying the plotted series.

        elif key == 'hum_ts':
            ax.plot(x, prepared['hums'], label='Humidity (%)')  # Plot humidity time series.
            ax.set_ylabel('Humidity (%)')
            ax.legend()

        elif key == 'light_ts':
            ax.plot(x, prepared['lights'], label='Light (lux)')  # Plot light time series in lux.
            ax.set_ylabel('Light (lux)')
            ax.legend()

        elif key == 'temp_hist':
            # Histogram requires removing NaNs because hist() fails with NaN values.
            ax.hist(prepared['temps'][~np.isnan(prepared['temps'])], bins=20)
            ax.set_xlabel('Temperature (C)')
            ax.set_ylabel('Count')
            ax.legend(["Temperature distribution"])

        elif key == 'hum_hist':
            ax.hist(prepared['hums'][~np.isnan(prepared['hums'])], bins=20)
            ax.set_xlabel('Humidity (%)')
            ax.set_ylabel('Count')
            ax.legend(["Humidity distribution"])

        elif key == 'temp_hum_scatter':
            # Scatter plot uses temperature on x-axis and humidity on y-axis which helps visualise correlation.
            ax.scatter(prepared['temps'], prepared['hums'])
            ax.set_xlabel('Temperature (C)')
            ax.set_ylabel('Humidity (%)')
            ax.legend(["Temp vs Humidity"])

        # If date values are used we need to format the x-axis to look like readable dates.
        if prepared['dates_used']:
            import matplotlib.dates as mdates  # Local import of date formatting tools used only when needed.
            ax.xaxis_date()  # Tell Matplotlib to treat x-axis values as dates for tick placement.
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))  # Format ticks as 'YYYY-MM-DD HH:MM'.
            for label in ax.get_xticklabels():  # Rotate tick labels to avoid overlap and improve readability.
                label.set_rotation(30)
                label.set_ha('right')
        else:
            ax.set_xlabel('Index')  # If not using dates, labeling the x-axis as 'Index' clarifies what the horizontal axis represents.

        ax.grid(True)  # Turn on gridlines for better readability and value estimation on the plot.


# To Run The Code
if __name__ == '__main__':  # Run the GUI only when the script is executed directly (not when imported as a module).
    app = CowApp()  # Instantiate the application which constructs the window and UI components.
    app.mainloop()  # Start Tk's main event loop; this call blocks and drives GUI interaction until the window is closed.
