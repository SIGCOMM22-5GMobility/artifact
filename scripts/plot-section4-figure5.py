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
TRACE_LEN = 480  # in secs
DATA_FOLDER = path.join(data_processed_dir, 'figure5-cloud_gaming')
FILENAME = 'DLOOP-STDVLG-CLOUD-GAMING.csv'

# load all files
df = pd.read_csv(path.join(DATA_FOLDER, FILENAME), low_memory=False)

# do preprocessing
df['other_latency'] = df['capture_latency'] + df['convert_latency'] + df['encode_latency'] + \
                      df['decode_latency'] + df['display_latency']
grp_df = df.groupby('time_since_start').agg(
    dropped_frames=('dropped', 'count'),
    network_latency=('network_latency', 'mean'),
    lte_ho_category=('lte_ho_category', 'first'),
    nr_ho_category=('nr_ho_category', 'first'),
    other_latency=('other_latency', 'mean')
)
grp_df.dropna(inplace=True, how='all', subset=['lte_ho_category', 'nr_ho_category', 'network_latency'])
grp_df.reset_index(inplace=True)
grp_df.loc[(grp_df['lte_ho_category'] == 'nsa_menb_intra') &
           (grp_df['nr_ho_category'] == 'nsa_scgm'), 'nr_ho_category'] = None
grp_df = grp_df[grp_df['time_since_start'] < TRACE_LEN]
hos_scga = grp_df[grp_df['nr_ho_category'] == 'nsa_scga']['time_since_start']
hos_scgm = grp_df[grp_df['nr_ho_category'] == 'nsa_scgm']['time_since_start']
hos_scgr = grp_df[grp_df['nr_ho_category'] == 'nsa_scgr']['time_since_start']
menb = grp_df[grp_df['lte_ho_category'].isin(['nsa_menb_intra'])]['time_since_start']
lte_ho = grp_df[grp_df['lte_ho_category'].isin(['lte_pcell_intra', 'lte_pcell_inter',
                                                'nsa_pcell_intra'])]['time_since_start']
grp_df['ho_latency'] = (grp_df['network_latency'].shift(1) + grp_df['network_latency'].shift(-1)) / 2
grp_df['ho_frames'] = (grp_df['dropped_frames'].shift(1) + grp_df['dropped_frames'].shift(-1)) / 2

#### Plot graph
if True:  # use truth value to turn on and off plotting
    plot_id = 'figure5'
    plot_name = 'cloud-gaming-timeline'
    plt.close('all')
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 3), sharex='all', gridspec_kw={'height_ratios': [2.75, 2.25]})
    fig.tight_layout()
    plt.subplots_adjust(hspace=0.15)
    fig.subplots_adjust(hspace=0.1)
    ax1r = ax1.twinx()

    lte_ho_height = 265
    nr_ho_height = 225

    latency_df = grp_df[grp_df['network_latency'].notna()]

    ## plot latency and dropped fps
    ax1.plot(latency_df['time_since_start'], latency_df['network_latency'], color=colorlist20[0], zorder=4)
    ax1r.plot(latency_df['time_since_start'], latency_df['other_latency'], color=colorlist20[2], zorder=2)
    ax2.plot(grp_df['time_since_start'], grp_df['dropped_frames'],
             label='dropped frames', color=colorlist20[10], alpha=1.0, lw=1, zorder=5)

    ## plot handovers
    ax1.scatter(hos_scgm, [nr_ho_height] * hos_scgm.shape[0], marker='v', s=36,
                c=['forestgreen'] * hos_scgm.shape[0], label='SCGM', zorder=6)
    ax1.scatter(menb, [lte_ho_height] * menb.shape[0], marker='v', s=36,
                c=[colorlist20[6]] * menb.shape[0], label='MNBH', zorder=7)

    ax1.set_ylim([-10, 290])
    ax1r.set_ylim([-10, 290])
    ax2.set_ylim([-1, 11])
    ax2.set_xlim([-2, TRACE_LEN+2])

    ax1.set_ylabel('network \nlatency (ms)', fontsize=18, color=colorlist20[0])
    ax1r.set_ylabel('other \nlatency (ms)', fontsize=18, color=colorlist20[2])
    ax2.set_ylabel('dropped \nframes (\%)', fontsize=18, color=colorlist20[10])
    ax2.set_xlabel('8 minutes timeline (sec)', fontsize=20)

    ax1.tick_params(axis='y', colors=colorlist20[0])
    ax1r.tick_params(axis='y', colors=colorlist20[2])
    ax2.tick_params(axis='y', colors=colorlist20[10])
    ax1.set_yticks([0, 100, 200])
    ax1r.set_yticks([0, 100, 200])
    ax2.set_yticks([0, 5, 10])
    ax2.set_xticks([0, 120, 240, 360, 480])
    ax1.tick_params(axis='both', which='major', labelsize=14, bottom=False)
    ax1r.tick_params(axis='both', which='major', labelsize=14, bottom=False)
    ax2.tick_params(axis='both', which='major', labelsize=14)
    ax2.tick_params(axis='x', which='major', labelsize=16)

    ax1.yaxis.grid(color='gainsboro', linestyle='dashed', zorder=1)
    ax2.yaxis.grid(color='gainsboro', linestyle='dashed', zorder=1)

    ax1.legend(loc='upper center', ncol=4, bbox_to_anchor=(0.5, 0.775), facecolor='#dddddd', columnspacing=0.5,
               handlelength=2, framealpha=.5, fontsize=18, borderpad=0.15, labelspacing=.2, handletextpad=.3)

    plot_handler(plt, plot_id, plot_name, plot_dir, show_flag=SHOW_PLOT_FLAG, ignore_eps=True, pad_inches=0.07)

print('Complete./')
