import os 
import csv 
import tkinter as tk 
from tkinter import ttk, filedialog, messagebox 
from datetime import datetime
import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 

SENSOR_FILEDS = ("tempreature", "humidity", "light")

def read_csv_file(filepath): 
  rows = []
  with open(filepath, newline="") as f: 
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames or []
    norm_fieldnames = [fn.lower().strip for fn in fieldnames if fn]
    
    expected_tokens = {"timestamp", "tempreature", "temp", "humidity", "hum", 
                       "Light", "Lux", ""

    }