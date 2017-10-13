# __init__.py

import tkinter as tk
from tkinter import ttk

import os
import re
import sys

from _log import logger

# Fonts
LARGE_FONT = ("Verdana", 25)
MEDIUM_FONT = ("Verdana", 12)
SMALL_FONT = ("Verdana", 8)

# Data Files
options_file = 'options.txt'
current_user_file = 'current_user.txt'
user_data_file = 'user_data.txt'
user_names_file = 'user_names.txt'
COFFEE_DATA_F = 'coffee_data.txt'
TECH_DATA_F = 'tech_data.txt'
PIZZA_DATA_F = 'pizza_data.txt'
