#!/usr/bin/env python3
from os import path
import matplotlib.pyplot as plt
import pandas as pd

from utils.context import data_processed_dir, plot_dir
from utils.utils import plot_handler, colorlist20

# comment out these lines if latex not installed
plt.rc('font', family='sans-serif', serif='cm10')
plt.rc('text', usetex=True)

############### Config ####################
SHOW_PLOT_FLAG = False
DATA_FOLDER = path.join(data_processed_dir, 'figure13-same_diff_pci')

# load data
same_pci_df = pd.read_csv(path.join(DATA_FOLDER, 'same-pci-ho-duration.csv'), low_memory=False)
diff_pci_df = pd.read_csv(path.join(DATA_FOLDER, 'diff-pci-ho-duration.csv'), low_memory=False)

#### Plot graph
if True:  # use truth value to turn on and off plotting
    plot_id = 'figure13'
    plot_name = 'nsa-same-diff-pci-ho-duration'
    plt.close('all')
    fig, ax = plt.subplots(figsize=(3, 1))
    fig.tight_layout()

    x = [0, 1]
    width = 0.4

    # Duration plot
    box1 = ax.boxplot([same_pci_df['ho_duration'], diff_pci_df['ho_duration']],
                      positions=x, autorange=True, showfliers=False, widths=width, patch_artist=True,
                      notch=True, zorder=4)
    for item in ['boxes', 'whiskers', 'fliers', 'medians', 'caps']:
        plt.setp(box1[item], color=colorlist20[6])
    plt.setp(box1["boxes"], facecolor=colorlist20[7], hatch='\\\\', linewidth=1.25)

    ax.set_xticks(x)
    ax.set_yticks([70, 110, 150])
    ax.set_xticklabels(['Same PCI for\n 4G and 5G', 'Diff. PCI for\n 4G and 5G'],
                       fontsize=14)
    ax.tick_params(axis='both', which='major', labelsize=20)
    ax.get_yaxis().set_tick_params(which='minor', size=0)
    ax.get_yaxis().set_tick_params(which='minor', width=0)
    ax.yaxis.grid(color='gainsboro', linestyle='dashed', zorder=1)
    ax.set_ylabel('Duration\n(ms)', fontsize=16)
    ax.yaxis.set_label_coords(-0.16, 0.3)
    ax.tick_params(axis='both', which='major', labelsize=12)

    plot_handler(plt, plot_id, plot_name, plot_dir, show_flag=SHOW_PLOT_FLAG, ignore_eps=True, pad_inches=0.07)

print('Complete./')
