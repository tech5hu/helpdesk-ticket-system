import csv # let python read/write csv files
from pathlib import Path # helps python safely locate files on any computer

# SET UP DATA FILE

# the file whee all tickets are stored
DATA_FILE = Path("data") / "helpdesk.csv"
# SDE - single variable for file path makes code easier to maintain
# CS - avoids hardcoding file paths everywhere, safer for data access
# AI - lets AI access data file for analysis
