#!/usr/bin/env python3
from os import path
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from utils.context import data_processed_dir, plot_dir
from utils.utils import plot_handler, colorlist20, remove_nan

# comment out these lines if latex not installed
plt.rc('font', family='sans-serif', serif='cm10')
plt.rc('text', usetex=True)

############### Config ####################
SHOW_PLOT_FLAG = False
FILTER_TIME_DIFF = 2.0  # when time difference between consecutive values is > 2 sec
DATA_FOLDER = path.join(data_processed_dir, 'figure12-scg_mod_bwd_impact')

# load data
bnl_vzw_df = pd.read_csv(path.join(DATA_FOLDER, 'BNL-WLOOP-IPERF.csv'), low_memory=False)

bnl_vzw_df['TIME_STAMP'] = pd.to_datetime(bnl_vzw_df['TIME_STAMP'])
bnl_vzw_df['Event Technology'].fillna(method='ffill', inplace=True)
bnl_vzw_df['LTE KPI PCell Serving Band'].fillna(method='ffill', inplace=True)
bnl_vzw_df['5G KPI PCell RF Band'].fillna(method='ffill', inplace=True)
bnl_vzw_df.loc[bnl_vzw_df['Event Technology'].str.contains('LTE', na=False), 'Event Technology'] = 'LTE'
bnl_vzw_df.loc[bnl_vzw_df['Event Technology'].str.contains('5G-NR_NSA', na=False), 'Event Technology'] = 'NSA'

#  Separate LTE vs low-band vs mmwave and filter
vzw_nsa_mm_df = bnl_vzw_df.copy(deep=True)

# process mmwave data (scg) mobility
vzw_nsa_mm_filtered_df = vzw_nsa_mm_df[['TIME_STAMP', 'Qualcomm 5G-NR EN-DC PHY Throughput '
                                                      'PDSCH Throughput(Total PDU) [Mbps]',
                                        '5G-NR RRC NR SCG Mobility Statistics NR SCG Mobility Type']]
vzw_nsa_mm_filtered_df = vzw_nsa_mm_filtered_df[
    vzw_nsa_mm_filtered_df['Qualcomm 5G-NR EN-DC PHY Throughput PDSCH Throughput(Total PDU) [Mbps]'].notnull() |
    vzw_nsa_mm_filtered_df['5G-NR RRC NR SCG Mobility Statistics NR SCG Mobility Type'].notnull()]
vzw_mm_tput_mean = vzw_nsa_mm_filtered_df['Qualcomm 5G-NR EN-DC PHY Throughput '
                                          'PDSCH Throughput(Total PDU) [Mbps]'].mean()
vzw_nsa_mm_filtered_df['tput_past'] = vzw_nsa_mm_filtered_df[
    'Qualcomm 5G-NR EN-DC PHY Throughput PDSCH Throughput(Total PDU) [Mbps]'].shift(2)
vzw_nsa_mm_filtered_df['tput_before'] = vzw_nsa_mm_filtered_df[
    'Qualcomm 5G-NR EN-DC PHY Throughput PDSCH Throughput(Total PDU) [Mbps]'].shift(1)
vzw_nsa_mm_filtered_df['tput_after'] = vzw_nsa_mm_filtered_df[
    'Qualcomm 5G-NR EN-DC PHY Throughput PDSCH Throughput(Total PDU) [Mbps]'].shift(-1)
vzw_nsa_mm_filtered_df['tput_delta'] = (vzw_nsa_mm_filtered_df['tput_after'] -
                                        vzw_nsa_mm_filtered_df['tput_before']) * vzw_mm_tput_mean
vzw_nsa_mm_filtered_df['tput_ratio'] = vzw_nsa_mm_filtered_df['tput_after'] / vzw_nsa_mm_filtered_df['tput_before']
vzw_nsa_mm_filtered_df['time_past'] = vzw_nsa_mm_filtered_df['TIME_STAMP'].shift(2)
vzw_nsa_mm_filtered_df['time_before'] = vzw_nsa_mm_filtered_df['TIME_STAMP'].shift(1)
vzw_nsa_mm_filtered_df['time_after'] = vzw_nsa_mm_filtered_df['TIME_STAMP'].shift(-1)
vzw_nsa_mm_filtered_df['time_diff'] = (
        vzw_nsa_mm_filtered_df['time_after'] - vzw_nsa_mm_filtered_df['time_before']).dt.total_seconds()
vzw_nsa_mm_filtered_df['time_diff_past'] = (
        vzw_nsa_mm_filtered_df['time_before'] - vzw_nsa_mm_filtered_df['time_past']).dt.total_seconds()
vzw_nsa_mm_filtered_df = vzw_nsa_mm_filtered_df[
    vzw_nsa_mm_filtered_df['5G-NR RRC NR SCG Mobility Statistics NR SCG Mobility Type'].notnull() &
    (vzw_nsa_mm_filtered_df['time_diff'] < FILTER_TIME_DIFF) & (vzw_nsa_mm_filtered_df['tput_ratio'] != np.inf)]
vzw_nsa_mm_filtered_add_df = vzw_nsa_mm_filtered_df[
    (vzw_nsa_mm_filtered_df['5G-NR RRC NR SCG Mobility '
                            'Statistics NR SCG Mobility Type'] == 'NR SCG Addition[LTE to NR]') &
    (vzw_nsa_mm_filtered_df['time_diff_past'] < FILTER_TIME_DIFF)]

# process mmwave data (scg) release
vzw_nsa_mm_filtered_rls_df = vzw_nsa_mm_df[['TIME_STAMP', 'Qualcomm 5G-NR EN-DC PHY Throughput '
                                                          'PDSCH Throughput(Total PDU) [Mbps]',
                                            '5G-NR RRC NR SCG Release Statistics[NR to LTE] Result']]
vzw_nsa_mm_filtered_rls_df = vzw_nsa_mm_filtered_rls_df[
    vzw_nsa_mm_filtered_rls_df['Qualcomm 5G-NR EN-DC PHY Throughput PDSCH Throughput(Total PDU) [Mbps]'].notnull() |
    vzw_nsa_mm_filtered_rls_df['5G-NR RRC NR SCG Release Statistics[NR to LTE] Result'].notnull()]
vzw_mm_tput_mean = vzw_nsa_mm_filtered_rls_df['Qualcomm 5G-NR EN-DC PHY Throughput '
                                              'PDSCH Throughput(Total PDU) [Mbps]'].mean()
vzw_nsa_mm_filtered_rls_df['tput_past'] = vzw_nsa_mm_filtered_rls_df[
    'Qualcomm 5G-NR EN-DC PHY Throughput PDSCH Throughput(Total PDU) [Mbps]'].shift(2)
vzw_nsa_mm_filtered_rls_df['tput_before'] = vzw_nsa_mm_filtered_rls_df[
    'Qualcomm 5G-NR EN-DC PHY Throughput PDSCH Throughput(Total PDU) [Mbps]'].shift(1)
vzw_nsa_mm_filtered_rls_df['tput_after'] = vzw_nsa_mm_filtered_rls_df[
    'Qualcomm 5G-NR EN-DC PHY Throughput PDSCH Throughput(Total PDU) [Mbps]'].shift(-1)
vzw_nsa_mm_filtered_rls_df['tput_delta'] = (vzw_nsa_mm_filtered_rls_df['tput_after'] -
                                            vzw_nsa_mm_filtered_rls_df['tput_before']) * vzw_mm_tput_mean
vzw_nsa_mm_filtered_rls_df['tput_ratio'] = vzw_nsa_mm_filtered_rls_df['tput_after'] / vzw_nsa_mm_filtered_rls_df[
    'tput_before']
vzw_nsa_mm_filtered_rls_df['time_before'] = vzw_nsa_mm_filtered_rls_df['TIME_STAMP'].shift(1)
vzw_nsa_mm_filtered_rls_df['time_after'] = vzw_nsa_mm_filtered_rls_df['TIME_STAMP'].shift(-1)
vzw_nsa_mm_filtered_rls_df['time_diff'] = (
        vzw_nsa_mm_filtered_rls_df['time_after'] - vzw_nsa_mm_filtered_rls_df['time_before']).dt.total_seconds()
vzw_nsa_mm_filtered_rls_df = vzw_nsa_mm_filtered_rls_df[
    vzw_nsa_mm_filtered_rls_df['5G-NR RRC NR SCG Release Statistics[NR to LTE] Result'].notnull() &
    (vzw_nsa_mm_filtered_rls_df['time_diff'] < FILTER_TIME_DIFF) & (vzw_nsa_mm_filtered_rls_df['tput_ratio'] != np.inf)]


#### Plot graph
if True:  # use truth value to turn on and off plotting
    plot_id = 'figure12'
    plot_name = 'bnl-wloop-vzw-ho-tput-scgc'
    plt.close('all')
    fig, ax = plt.subplots(figsize=(4, 1.4))
    fig.tight_layout()

    width_box = 0.2
    margin = 0.05
    pos = [0]

    vzw_nsa_mm_chg_past = remove_nan(vzw_nsa_mm_filtered_rls_df['tput_past'].to_numpy())

    vzw_nsa_mm_chg_before = remove_nan(vzw_nsa_mm_filtered_add_df['tput_before'].to_numpy())

    vzw_nsa_mm_chg_after = remove_nan(vzw_nsa_mm_filtered_add_df['tput_after'].to_numpy())

    box1 = ax.boxplot([vzw_nsa_mm_chg_past],
                      positions=[x - margin for x in pos], autorange=True,
                      showfliers=False, widths=width_box, patch_artist=True, zorder=4)
    for item in ['boxes', 'fliers', 'medians', 'caps']:
        plt.setp(box1[item], color=colorlist20[0], linewidth=1.5)
    plt.setp(box1['whiskers'], color=colorlist20[0], linewidth=1.5, linestyle='--')
    plt.setp(box1["boxes"], facecolor=colorlist20[1], linewidth=1.5)

    box2 = ax.boxplot([vzw_nsa_mm_chg_before],
                      positions=[x + width_box for x in pos], autorange=True,
                      showfliers=False, widths=width_box, patch_artist=True, zorder=4)
    for item in ['boxes', 'fliers', 'medians', 'caps']:
        plt.setp(box2[item], color=colorlist20[2], linewidth=1.5)
    plt.setp(box2['whiskers'], color=colorlist20[2], linewidth=1.5, linestyle='--')
    plt.setp(box2["boxes"], facecolor=colorlist20[3], linewidth=1.5)

    box3 = ax.boxplot([vzw_nsa_mm_chg_after],
                      positions=[x + width_box * 2 + margin for x in pos], autorange=True,
                      showfliers=False, widths=width_box, patch_artist=True, zorder=4)
    for item in ['boxes', 'fliers', 'medians', 'caps']:
        plt.setp(box3[item], color=colorlist20[4], linewidth=1.5)
    plt.setp(box3['whiskers'], color=colorlist20[4], linewidth=1.5, linestyle='--')
    plt.setp(box3["boxes"], facecolor=colorlist20[5], linewidth=1.5)

    ax.set_ylabel('DL Tput. \n(Mbps)', fontsize=16)
    ax.set_xlim([min(pos) - 0.2, max(pos) + 0.6])
    ax.set_ylim([-100, 3100])
    ax.set_yticks([0, 1500, 3000])
    ax.set_xticks([-0.05, 0.2, 0.4+margin])
    ax.set_xticklabels([r'\textsf{HO}$_{pre}$', r'\textsf{HO}$_{exec}$', r'\textsf{HO}$_{post}$'], fontsize=16)
    ax.tick_params(axis='y', which='major', labelsize=14)
    ax.yaxis.grid(color='gainsboro', linestyle='dashed', zorder=0)

    plot_handler(plt, plot_id, plot_name, plot_dir, show_flag=SHOW_PLOT_FLAG, ignore_eps=True, pad_inches=0.07)


print('Complete./')
