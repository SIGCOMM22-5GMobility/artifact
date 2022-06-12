#!/usr/bin/env python3
from os import path
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.patches import Patch

from utils.context import data_processed_dir, plot_dir
from utils.utils import plot_handler, colorlist20, remove_nan

# comment out these lines if latex not installed
plt.rc('font', family='sans-serif', serif='cm10')
plt.rc('text', usetex=True)


def check_if_range_lies(col, interval_list):
    for i, interval_set in enumerate(interval_list):
        if interval_set[0] <= col <= interval_set[1]:
            return i + 1
    return np.nan


## Config
SHOW_PLOT_FLAG = False
DATA_FOLDER = path.join(data_processed_dir, 'figure7-nsa_modes')
COMBINED_FILE = path.join(DATA_FOLDER, "TCP-EXPERIMENTS.csv")
HO_INTERVAL_START = 100  # in ms
HO_INTERVAL_END = 1000

## read data
bbr_df = pd.read_csv(COMBINED_FILE, low_memory=False)

bbr_lte_df = bbr_df[bbr_df['mode'] == 'lte_mode'].copy(deep=True)
bbr_dual_df = bbr_df[bbr_df['mode'] == 'dual_mode'].copy(deep=True)
bbr_5gonly_df = bbr_df[bbr_df['mode'] == '5gonly_mode'].copy(deep=True)

# process 5gonly mode
bbr_5gonly_scgr_ho_time = bbr_5gonly_df[bbr_5gonly_df['nr_ho_category'] == 'nsa_scgr']['time_since_start'].to_list()
bbr_5gonly_scgr_ho_interval = [(x - HO_INTERVAL_START, x + HO_INTERVAL_END) for x in bbr_5gonly_scgr_ho_time]
bbr_df['5gonly_scgr_row'] = bbr_df.apply(
    lambda x: check_if_range_lies(x['time_since_start'], bbr_5gonly_scgr_ho_interval),
    axis=1)
bbr_5gonly_scgr_df = bbr_df[bbr_df['5gonly_scgr_row'].notna()].copy(deep=True)

bbr_5gonly_scga_ho_time = bbr_5gonly_df[bbr_5gonly_df['nr_ho_category'] == 'nsa_scga']['time_since_start'].to_list()
bbr_5gonly_scga_ho_interval = [(x - HO_INTERVAL_START, x + HO_INTERVAL_END) for x in bbr_5gonly_scga_ho_time]
bbr_df['5gonly_scga_row'] = bbr_df.apply(
    lambda x: check_if_range_lies(x['time_since_start'], bbr_5gonly_scga_ho_interval),
    axis=1)
bbr_5gonly_scga_df = bbr_df[bbr_df['5gonly_scga_row'].notna()].copy(deep=True)

bbr_5gonly_scgm_ho_time = bbr_5gonly_df[bbr_5gonly_df['nr_ho_category'] == 'nsa_scgm']['time_since_start'].to_list()
bbr_5gonly_scgm_ho_interval = [(x - HO_INTERVAL_START, x + HO_INTERVAL_END) for x in bbr_5gonly_scgm_ho_time]
bbr_df['5gonly_scgm_row'] = bbr_df.apply(
    lambda x: check_if_range_lies(x['time_since_start'], bbr_5gonly_scgm_ho_interval),
    axis=1)
bbr_5gonly_scgm_df = bbr_df[bbr_df['5gonly_scgm_row'].notna()].copy(deep=True)

# process dual mode
bbr_dual_scgr_ho_time = bbr_dual_df[bbr_dual_df['nr_ho_category'] == 'nsa_scgr']['time_since_start'].to_list()
bbr_dual_scgr_ho_interval = [(x - HO_INTERVAL_START, x + HO_INTERVAL_END) for x in bbr_dual_scgr_ho_time]
bbr_df['dual_scgr_row'] = bbr_df.apply(lambda x: check_if_range_lies(x['time_since_start'], bbr_dual_scgr_ho_interval),
                                       axis=1)
bbr_dual_scgr_df = bbr_df[bbr_df['dual_scgr_row'].notna()].copy(deep=True)

bbr_dual_scga_ho_time = bbr_dual_df[bbr_dual_df['nr_ho_category'] == 'nsa_scga']['time_since_start'].to_list()
bbr_dual_scga_ho_interval = [(x - HO_INTERVAL_START, x + HO_INTERVAL_END) for x in bbr_dual_scga_ho_time]
bbr_df['dual_scga_row'] = bbr_df.apply(lambda x: check_if_range_lies(x['time_since_start'], bbr_dual_scga_ho_interval),
                                       axis=1)
bbr_dual_scga_df = bbr_df[bbr_df['dual_scga_row'].notna()].copy(deep=True)

bbr_dual_scgm_ho_time = bbr_dual_df[bbr_dual_df['nr_ho_category'] == 'nsa_scgm']['time_since_start'].to_list()
bbr_dual_scgm_ho_interval = [(x - HO_INTERVAL_START, x + HO_INTERVAL_END) for x in bbr_dual_scgm_ho_time]
bbr_df['dual_scgm_row'] = bbr_df.apply(lambda x: check_if_range_lies(x['time_since_start'], bbr_dual_scgm_ho_interval),
                                       axis=1)
bbr_dual_scgm_df = bbr_df[bbr_df['dual_scgm_row'].notna()].copy(deep=True)

feature = 'SS_RTT_AVG'
bbr_5gonly_ho_no = bbr_5gonly_df[feature].to_list()
bbr_5gonly_scgr = bbr_5gonly_scgr_df[feature].to_list()
bbr_5gonly_scga = bbr_5gonly_scga_df[feature].to_list()
bbr_5gonly_scgm = bbr_5gonly_scgm_df[feature].to_list()

bbr_dual_ho_no = bbr_dual_df[feature].to_list()
bbr_dual_scgr = bbr_dual_scgr_df[feature].to_list()
bbr_dual_scga = bbr_dual_scga_df[feature].to_list()
bbr_dual_scgm = bbr_dual_scgm_df[feature].to_list()

#### Plot graph
if True:  # use truth value to turn on and off plotting
    plot_id = 'figure7'
    plot_name = feature
    plt.close('all')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5, 1.75), sharey='all')
    fig.tight_layout()
    fig.subplots_adjust(wspace=0.025)

    pos = [0, 1, 2, 3]
    width_box = 0.3
    pad = 0.08
    no_ho_idx = 4
    scgr_idx = 6
    scga_idx = 2
    scgm_idx = 0

    ec_idx_list = [no_ho_idx, scgr_idx, scga_idx, scgm_idx]
    fc_list = [colorlist20[x + 1] for x in ec_idx_list]
    ec_list = [colorlist20[x] for x in ec_idx_list]

    bbr_dual_list = [bbr_dual_ho_no, bbr_dual_scgr, bbr_dual_scga, bbr_dual_scgm]
    bbr_dual_list = [np.array(x) for x in bbr_dual_list]
    bbr_dual_list = [remove_nan(x) for x in bbr_dual_list]

    for idx in range(pos.__len__()):
        box1 = ax1.boxplot([bbr_dual_list[idx]],
                           positions=[pos[idx]], autorange=True, showfliers=False, zorder=4,
                           widths=width_box, patch_artist=True)
        for item in ['boxes', 'fliers', 'medians', 'caps']:
            plt.setp(box1[item], color=ec_list[idx], linewidth=1.5)
        plt.setp(box1['whiskers'], color=ec_list[idx], linewidth=1.5, linestyle=':')
        plt.setp(box1["boxes"], facecolor=fc_list[idx], linewidth=1.5)

    ax1.axhline(y=93, linewidth=2, color='darkgrey', linestyle=':', zorder=2)

    bbr_5gonly_list = [bbr_5gonly_ho_no, bbr_5gonly_scgr, bbr_5gonly_scga, bbr_5gonly_scgm]
    bbr_5gonly_list = [np.array(x) for x in bbr_5gonly_list]
    bbr_5gonly_list = [remove_nan(x) for x in bbr_5gonly_list]

    for idx in range(pos.__len__()):
        box2 = ax2.boxplot([bbr_5gonly_list[idx]],
                           positions=[pos[idx]], autorange=True, showfliers=False, zorder=4,
                           widths=width_box, patch_artist=True)
        for item in ['boxes', 'fliers', 'medians', 'caps']:
            plt.setp(box2[item], color=ec_list[idx], linewidth=1.5)
        plt.setp(box2['whiskers'], color=ec_list[idx], linewidth=1.5, linestyle=':')
        plt.setp(box2["boxes"], facecolor=fc_list[idx], linewidth=1.5)

    # set y-labels and limits
    ax1.set_ylabel('RTT (ms)', fontsize=16)
    ax1.set_ylim([0, 320])
    ax1.set_yticks([0, 100, 200, 300])
    ax1.tick_params(axis='both', which='major', bottom=False, labelsize=13)
    ax2.tick_params(axis='both', which='major', bottom=False, left=False, labelsize=13)

    ax1.text(0.75, 260, r'\textit{dual mode}', ha="center", va="center", fontsize=14,
             bbox=dict(facecolor='lightgray', edgecolor='lightgray', boxstyle='round,pad=.2'), zorder=8)
    ax2.text(2.275, 270, r'\textit{5G-only mode}', ha="center", va="center", fontsize=14,
             bbox=dict(facecolor='lightgray', edgecolor='lightgray', boxstyle='round,pad=.1'), zorder=8)

    ax1.set_xticklabels([])
    ax2.set_xticklabels([])

    ax1.yaxis.grid(color='gainsboro', linestyle='dashed', zorder=1)
    ax2.yaxis.grid(color='gainsboro', linestyle='dashed', zorder=1)

    labels = ['w/o HO', 'SCGR', 'SCGA', 'SCGM']
    patches = [Patch(facecolor=fc_list[i], edgecolor=ec_list[i], label=labels[i]) for i in range(pos.__len__())]

    ax1.legend(handles=patches, loc='upper right',
               ncol=4, bbox_to_anchor=(2.0, 1.3), facecolor='#dddddd', columnspacing=0.4,
               handlelength=2, framealpha=.8, fontsize=13, borderpad=0.1, labelspacing=.2, handletextpad=0.5)

    plot_handler(plt, plot_id, plot_name, plot_dir, show_flag=SHOW_PLOT_FLAG, ignore_eps=True, pad_inches=0.07)

print('Complete./')
