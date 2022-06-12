#!/usr/bin/env python3
from os import path
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from utils.context import data_processed_dir, plot_dir
from utils.utils import plot_handler, colorlist20

# comment out these lines if latex not installed
plt.rc('font', family='sans-serif', serif='cm10')
plt.rc('text', usetex=True)

############### Config ####################
SHOW_PLOT_FLAG = False
DATA_FOLDER = path.join(data_processed_dir, 'figure11-coverage_footprint')

# load data
sa_low_coverage = pd.read_csv(path.join(DATA_FOLDER, 'sa_low_coverage.csv'))
nsa_low_coverage = pd.read_csv(path.join(DATA_FOLDER, 'nsa_low_coverage.csv'))
nsa_low_ideal_coverage = pd.read_csv(path.join(DATA_FOLDER, 'nsa_low_ideal_coverage.csv'))
nsa_mid_coverage = pd.read_csv(path.join(DATA_FOLDER, 'nsa_mid_coverage.csv'))
nsa_mid_ideal_coverage = pd.read_csv(path.join(DATA_FOLDER, 'nsa_mid_ideal_coverage.csv'))


#### Plot graph
if True:  # use truth value to turn on and off plotting
    plot_id = 'figure11a'
    plot_name = 'low-band-coverage'
    plt.close('all')
    fig, ax = plt.subplots(figsize=(3.3, 2))
    fig.tight_layout()

    sns.kdeplot(data=sa_low_coverage['distance_ho'].to_numpy().squeeze(), ax=ax, color=colorlist20[0],
                fill=True, label='Coverage w/ SA', alpha=0.3, linewidth=1.5, zorder=4, bw_adjust=1.3)
    sns.kdeplot(data=nsa_low_coverage['distance_ho'].to_numpy().squeeze(), ax=ax, color=colorlist20[6],
                fill=True, label='Coverage w/ NSA', alpha=0.3, linewidth=1.5, bw_adjust=1.6, zorder=4)
    sns.kdeplot(data=nsa_low_ideal_coverage['distance_pci'].to_numpy().squeeze(), ax=ax, color=colorlist20[2],
                label='Coverage w/o NSA', alpha=0.3, linewidth=1.5, zorder=4, bw_adjust=1.3, fill=False, ls='--')

    ax.set_xlim([-100, 4000])
    ax.set_xticks([1000, 2000, 3000])
    ax.set_ylabel('Density', fontsize=15)
    ax.set_xlabel('Distance (m)', fontsize=15)
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.yaxis.grid(color='gainsboro', linestyle='dashed', zorder=0)

    ax.legend(loc='upper right', ncol=1, bbox_to_anchor=(1.01, 1.02), facecolor='#dddddd',
              columnspacing=0.4, handlelength=2, framealpha=.7, fontsize=13, borderpad=0.1,
              labelspacing=.2, handletextpad=.35)

    plot_handler(plt, plot_id, plot_name, plot_dir, show_flag=SHOW_PLOT_FLAG, ignore_eps=True, pad_inches=0.07)

#### Plot graph
if True:  # use truth value to turn on and off plotting
    plot_id = 'figure11b'
    plot_name = 'mid-band-coverage'
    plt.close('all')
    fig, ax = plt.subplots(figsize=(3.3, 2))
    fig.tight_layout()

    sns.kdeplot(data=nsa_mid_coverage['distance_ho'].to_numpy().squeeze(), ax=ax, color=colorlist20[8],
                fill=True, label='Coverage w/ NSA', alpha=0.3, linewidth=1.5, bw_adjust=1.3, zorder=4)
    sns.kdeplot(data=nsa_mid_ideal_coverage['distance_pci'].to_numpy().squeeze(), ax=ax, color=colorlist20[2],
                label='Coverage w/o NSA', alpha=0.3, linewidth=1.5, zorder=4, bw_adjust=1.3, fill=False, ls='--')

    ax.set_xlim([0, 2500])
    ax.set_xticks([500, 1000, 1500, 2000])
    ax.set_ylabel('Density', fontsize=15)
    ax.set_xlabel('Distance (m)', fontsize=13)
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.yaxis.grid(color='gainsboro', linestyle='dashed', zorder=0)

    ax.legend(loc='upper right', ncol=1, bbox_to_anchor=(1.02, 1.05), facecolor='#dddddd',
              columnspacing=0.4, handlelength=2, framealpha=.7, fontsize=13, borderpad=0.1,
              labelspacing=.2, handletextpad=.35)

    plot_handler(plt, plot_id, plot_name, plot_dir, show_flag=SHOW_PLOT_FLAG, ignore_eps=True, pad_inches=0.07)

print('Complete./')
