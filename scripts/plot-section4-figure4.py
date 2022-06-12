#!/usr/bin/env python3
from os import path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from utils.utils import plot_handler, colorlist20
from utils.context import data_processed_dir, plot_dir
import matplotlib.font_manager as font_manager
import bisect

# comment out these lines if latex not installed
plt.rc('font', family='sans-serif', serif='cm10')
plt.rc('text', usetex=True)

############### Config ####################
SHOW_PLOT_FLAG = False
DATA_FOLDER = path.join(data_processed_dir, 'figure4-video_conf')

# read data
df_driving = pd.read_csv(path.join(DATA_FOLDER, 'laptop_driving_merged.csv'))
driving_ho = pd.read_csv(path.join(DATA_FOLDER, 'driving_2_5g_tracker.csv'))
ho_tses = driving_ho['timestamp']

#### Plot graph
if True:  # use truth value to turn on and off plotting
    plot_name = 'video-conf-stats'
    plot_id = 'figure4'
    plt.close('all')
    fig, ax = plt.subplots(figsize=(5, 2))
    fig.tight_layout()

    axr = ax.twinx()

    timestamps_driving_np = df_driving['time_stamp(s)'].to_numpy()
    send_latency_driving_np = df_driving['latency_send(ms)'].to_numpy()
    ax.plot(df_driving['time_stamp(s)'].to_numpy(), df_driving['latency_send(ms)'].to_numpy(),
            label='driving', color=colorlist20[0], alpha=0.8, lw=1, zorder=4)
    arrow = None
    Q = None
    for ho_ts in ho_tses:
        idx = bisect.bisect(timestamps_driving_np, ho_ts)
        Q = ax.quiver(ho_ts - 5, send_latency_driving_np[idx] + 600, 1.5, -145, angles="xy", color=colorlist20[4],
                      width=0.004, headwidth=3, headlength=3, zorder=8)
    font = font_manager.FontProperties(size=14)
    ax.quiverkey(Q, 0.45, 0.88, 200, label='Handover', labelpos='E', labelcolor=colorlist20[4], fontproperties=font)

    send_pkt_loss_np = df_driving['packet_loss_avg_send(%)'].to_numpy()
    axr.plot(df_driving['time_stamp(s)'].to_numpy(), df_driving['packet_loss_avg_send(%)'].to_numpy(),
             label='driving', color=colorlist20[2], alpha=1.0, lw=1, zorder=4)

    ax.set_xlabel('14 minutes timeline (sec)', fontsize=14)
    ax.set_ylabel('Video latency (ms)', fontsize=14, color=colorlist20[0])
    axr.set_ylabel('Video Packet Loss (\%)', fontsize=14, color=colorlist20[2])
    ax.set_xlim([-15, 830])
    ax.set_xticks(np.arange(0, 801, 100))
    ax.set_ylim([-100, 2500])
    ax.set_yticks(np.arange(0, 2501, 500))
    axr.set_ylim([-5, 80])
    axr.set_yticks(np.arange(0, 80, 25))
    ax.tick_params(axis='both', which='major', labelsize=12)
    axr.tick_params(axis='both', which='major', labelsize=12)
    ax.tick_params(axis='y', colors=colorlist20[0])
    axr.tick_params(axis='y', colors=colorlist20[2])
    ax.yaxis.grid(color='gainsboro', linestyle='dashed', zorder=1)

    ax.set_zorder(axr.get_zorder() + 1)
    ax.patch.set_visible(False)

    plot_handler(plt, plot_id, plot_name, plot_dir, show_flag=SHOW_PLOT_FLAG, ignore_eps=True, pad_inches=0.07)

print("Complete./")
