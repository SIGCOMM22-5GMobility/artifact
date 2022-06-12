#!/usr/bin/env python3
from os import path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from utils.context import data_processed_dir, plot_dir
from utils.utils import plot_handler, colorlist20, remove_nan

# comment out these lines if latex not installed
plt.rc('font', family='sans-serif', serif='cm10')
plt.rc('text', usetex=True)


def check_if_range_lies(col, interval_list):
    for idx, interval_set in enumerate(interval_list):
        if interval_set[0] <= col <= interval_set[1]:
            return idx + 1
    return np.nan


############### Config ####################
SHOW_PLOT_FLAG = False
EXPR_TYPE = 'figure6-volumetric_video'
DATA_FOLDER = path.join(data_processed_dir, EXPR_TYPE)
HO_INTERVAL_START = 10  # in ms
HO_INTERVAL_END = 10

# read data
df = pd.read_csv(path.join(DATA_FOLDER, f'HANDOFF-VOLUMETRIC_combined.csv'), low_memory=False)

# preprocess data
df['bitrate'] = (df['bytes'] / df['receive']) / (1000000 / 8)
df['tech'] = np.nan
df.loc[(df['Event Technology'] == 'LTE'), 'tech'] = 'LTE'
df.loc[(df['Event Technology'] == 'NSA') & (df['5G KPI PCell RF Band'] == 'Low-Band'), 'tech'] = 'NSA-LOW'
df.loc[(df['Event Technology'] == 'NSA') & (df['5G KPI PCell RF Band'] == 'mmWave'), 'tech'] = 'NSA-MM'
df.sort_values(by=['run_number', 'TIME_STAMP'], inplace=True)
df['TIME_STAMP'] = df['TIME_STAMP'].cumsum()
df['bitrate'].fillna(method='ffill', inplace=True)
df['receive'].fillna(method='ffill', inplace=True)
ho_time = df[(df['nr_ho_category'].notna()) | (df['lte_ho_category'].notna())]['TIME_STAMP'].to_list()
ho_interval = [(x - HO_INTERVAL_START, x + HO_INTERVAL_END) for x in ho_time]
df['ho_row'] = df.apply(lambda x: check_if_range_lies(x['TIME_STAMP'], ho_interval), axis=1)
ho_df = df[df['ho_row'].notna()]
no_ho_df = df[df['ho_row'].isna()]
low_ho_df = ho_df[ho_df['tech'] == 'NSA-LOW'].copy(deep=True)
mm_ho_df = ho_df[ho_df['tech'] == 'NSA-MM'].copy(deep=True)
low_no_ho_df = no_ho_df[no_ho_df['tech'] == 'NSA-LOW'].copy(deep=True)
mm_no_ho_df = no_ho_df[no_ho_df['tech'] == 'NSA-MM'].copy(deep=True)

#### Plot graph
if True:  # use truth value to turn on and off plotting
    plot_id = 'figure6'
    plot_name = 'volumetric-ho-band-comparison'
    plt.close('all')
    fig, ax = plt.subplots(figsize=(4.75, 1.85))
    fig.tight_layout()
    axr = ax.twinx()

    pos = [0, 1, 2, 3]
    x_lim = -0.4, 3.8
    width_box = 0.3
    pad = 0.05
    lc_idx = 2
    rc_idx = 4

    bitrate_low_ho = remove_nan(low_ho_df['bitrate'])
    bitrate_mm_ho = remove_nan(mm_ho_df['bitrate'])
    receive_low_ho = remove_nan(low_ho_df['receive']) * 1000
    receive_mm_ho = remove_nan(mm_ho_df['receive']) * 1000
    bitrate_low_no_ho = remove_nan(low_no_ho_df['bitrate'])
    bitrate_mm_no_ho = remove_nan(mm_no_ho_df['bitrate'])
    receive_low_no_ho = remove_nan(low_no_ho_df['receive']) * 1000
    receive_mm_no_ho = remove_nan(mm_no_ho_df['receive']) * 1000

    box1 = ax.boxplot([bitrate_low_no_ho, bitrate_low_ho, bitrate_mm_no_ho, bitrate_mm_ho],
                      positions=pos, autorange=True, showfliers=False, zorder=4,
                      widths=width_box, patch_artist=True)
    for item in ['boxes', 'fliers', 'medians', 'caps']:
        plt.setp(box1[item], color=colorlist20[lc_idx], linewidth=1.5)
    plt.setp(box1['whiskers'], color=colorlist20[lc_idx], linewidth=1.5, linestyle=':')
    plt.setp(box1["boxes"], facecolor=colorlist20[lc_idx+1], linewidth=1.5)
    plt.setp(box1['means'], markerfacecolor=colorlist20[lc_idx], markeredgecolor=colorlist20[lc_idx])

    box2 = axr.boxplot([receive_low_no_ho, receive_low_ho, receive_mm_no_ho, receive_mm_ho],
                       zorder=4,
                       positions=[x + width_box + pad for x in pos],
                       autorange=True, showfliers=False, widths=width_box, patch_artist=True)
    for item in ['boxes', 'fliers', 'medians', 'caps']:
        plt.setp(box2[item], color=colorlist20[rc_idx], linewidth=1.5)
    plt.setp(box2['whiskers'], color=colorlist20[rc_idx], linewidth=1.5, linestyle=':')
    plt.setp(box2["boxes"], facecolor=colorlist20[rc_idx+1], linewidth=1.5)
    plt.setp(box2['means'], markerfacecolor=colorlist20[rc_idx], markeredgecolor=colorlist20[rc_idx])

    # mark stationary and driving results
    ax.axvspan(-0.4, 1.65, alpha=0.15, color='orange', zorder=1)
    ax.axvspan(1.65, 4, alpha=1.0, color='mistyrose', zorder=1)
    ax.text(0.5, 160, 'Low-Band', ha="center", va="center", fontsize=17,
            bbox=dict(facecolor='lightgray', edgecolor='lightgray', boxstyle='round,pad=.2'), zorder=8)
    ax.text(2.65, 140, 'mmWave', ha="center", va="center", fontsize=16.5,
            bbox=dict(facecolor='lightgray', edgecolor='lightgray', boxstyle='round,pad=.2'), zorder=8)

    # set y-labels and limits
    ax.set_ylim([-10, 200])
    axr.set_ylim([-20, 800])
    axr.set_yticks([0, 250, 500, 750])
    ax.set_ylabel('video\nbitrate (Mbps)', fontsize=20, color=colorlist20[lc_idx])
    axr.set_ylabel('network\nlatency (ms)', fontsize=20, color=colorlist20[rc_idx])
    ax.tick_params(axis='y', which='major', labelsize=15, colors=colorlist20[lc_idx])
    axr.tick_params(axis='y', which='major', labelsize=15, colors=colorlist20[rc_idx])

    # set x-labels and limits
    ax.set_xlim([x_lim[0], x_lim[1]])
    ax.set_xticks([x + (width_box + pad) / 2 for x in pos])
    ax.set_xticklabels(['w/o HO', 'w/ HO', 'w/o HO', 'w/ HO'], fontsize=16)

    ax.yaxis.grid(color='gainsboro', linestyle='dashed', zorder=1)

    plot_handler(plt, plot_id, plot_name, plot_dir, show_flag=SHOW_PLOT_FLAG, ignore_eps=True, pad_inches=0.07)

print('Complete./')
