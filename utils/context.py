import os
from os import path
import sys

proj_dir = path.abspath(path.join(path.dirname(__file__), os.pardir))
data_dir = path.join(proj_dir, 'data')
data_processed_dir = path.join(proj_dir, 'data-processed')
plot_dir = path.join(proj_dir, 'plots')
utils_dir = path.join(proj_dir, 'utils')
clutter_dir = path.join(proj_dir, 'clutter')
sys.path.append(proj_dir)
