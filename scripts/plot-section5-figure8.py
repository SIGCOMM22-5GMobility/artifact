#!/usr/bin/env python3
from os import path
import matplotlib.pyplot as plt
import pandas as pd

from utils.context import data_processed_dir, plot_dir
from utils.utils import plot_handler, colorlist20, get_cdf

# comment out these lines if latex not installed
plt.rc('font', family='sans-serif', serif='cm10')
plt.rc('text', usetex=True)

############### Config ####################
SHOW_PLOT_FLAG = False
DATA_FOLDER = path.join(data_processed_dir, 'figure8-ho_prep_duration')

# load data
df = pd.read_csv(path.join(DATA_FOLDER, 'HO-Duration_Combined.csv'))

# do preprocessing
tmb_df = df[df['Operator'] == 'TMB']

### t-mobile ###
tmb_lte_ho_dur = get_cdf(tmb_df[(tmb_df['Type'] == 'PCell') & (tmb_df['Band'] == 'Low') &
                                (tmb_df['Tech'] == 'LTE')]['MR'].to_numpy() * 1000)
tmb_nsa_mcg_ho_dur = get_cdf(tmb_df[(tmb_df['Type'] == 'PCell') & (tmb_df['Band'] == 'Low') &
                                    (tmb_df['Tech'] == 'NSA')]['MR'].to_numpy() * 1000)
tmb_nsa_scg_add_ho_dur = get_cdf(tmb_df[(tmb_df['Type'] == 'SCG Add.') & (tmb_df['Band'] == 'Low') &
                                        (tmb_df['Tech'] == 'NSA')]['MR'].to_numpy() * 1000)
tmb_nsa_scg_mod_ho_dur = get_cdf(tmb_df[(tmb_df['Type'] == 'SCG Mod.') & (tmb_df['Band'] == 'Mid') &
                                        (tmb_df['Tech'] == 'NSA')]['MR'].to_numpy() * 1000)
tmb_nsa_scg_rel_ho_dur = get_cdf(tmb_df[(tmb_df['Type'] == 'SCG Rel.') & (tmb_df['Band'] == 'Low') &
                                        (tmb_df['Tech'] == 'NSA')]['MR'].to_numpy() * 1000)
tmb_nsa_menb_ho_dur = get_cdf(tmb_df[(tmb_df['Type'] == 'MCG') & (tmb_df['Band'] == 'Low') &
                                     (tmb_df['Tech'] == 'NSA')]['MR'].to_numpy() * 1000)
tmb_sa_mcg_ho_dur = get_cdf(tmb_df[(tmb_df['Type'] == 'MCG') & (tmb_df['Band'] == 'Low') &
                                   (tmb_df['Tech'] == 'SA')]['MR'].to_numpy() * 1000)

#### Plot graph
if True:  # use truth value to turn on and off plotting
    plot_id = 'figure8'
    plot_name = 'ho-prep-duration'
    plt.close('all')
    fig, ax = plt.subplots(figsize=(5, 1.65))
    fig.tight_layout()

    pos1 = [0]
    pos2 = [2, 3, 4]
    pos3 = [1]
    width_box = 0.6

    box1 = ax.boxplot([tmb_lte_ho_dur[0]],
                      positions=pos1, autorange=True,
                      showfliers=False, widths=width_box, patch_artist=True, zorder=4)
    for item in ['boxes', 'fliers', 'medians', 'caps']:
        plt.setp(box1[item], color=colorlist20[0], linewidth=2)
    plt.setp(box1['whiskers'], color=colorlist20[0], linewidth=2, linestyle='--')
    plt.setp(box1["boxes"], facecolor=colorlist20[1], linewidth=2)
    box2 = ax.boxplot([tmb_nsa_mcg_ho_dur[0], tmb_nsa_scg_add_ho_dur[0], tmb_nsa_scg_mod_ho_dur[0]],
                      positions=pos2, autorange=True,
                      showfliers=False, widths=width_box, patch_artist=True, zorder=4)
    for item in ['boxes', 'fliers', 'medians', 'caps']:
        plt.setp(box2[item], color=colorlist20[2], linewidth=2)
    plt.setp(box2['whiskers'], color=colorlist20[2], linewidth=2, linestyle='--')
    plt.setp(box2["boxes"], facecolor=colorlist20[3], linewidth=2)
    box3 = ax.boxplot([tmb_sa_mcg_ho_dur[0]],
                      positions=pos3, autorange=True,
                      showfliers=False, widths=width_box, patch_artist=True, zorder=4)
    for item in ['boxes', 'fliers', 'medians', 'caps']:
        plt.setp(box3[item], color=colorlist20[4], linewidth=2)
    plt.setp(box3['whiskers'], color=colorlist20[4], linewidth=2, linestyle='--')
    plt.setp(box3["boxes"], facecolor=colorlist20[5], linewidth=2)

    ax.set_ylim([-20, 210])
    ax.set_yticks([0, 100, 200])
    ax.set_xticks(pos1 + pos2 + pos3)
    ax.set_xticklabels(['LTEH', 'LTEH', 'SCGA', 'SCGM', 'MCGH'], fontsize=16)
    ax.set_ylabel('Duration\n(ms)', fontsize=20)
    ax.yaxis.grid(color='gainsboro', linestyle='dashed', zorder=1)
    ax.tick_params(axis='y', which='major', labelsize=15)
    ax.legend([box1["boxes"][0], box2["boxes"][0], box3["boxes"][0]],
              [r'LTE', r'NSA', r'SA'],
              loc='upper center', ncol=3, bbox_to_anchor=(0.5, 1.5), facecolor='#dddddd',
              columnspacing=0.75, handlelength=1.5, framealpha=.7, fontsize=20,
              borderpad=0.1, labelspacing=.25, handletextpad=.25)
    plot_handler(plt, plot_id, plot_name, plot_dir, show_flag=SHOW_PLOT_FLAG, ignore_eps=True, pad_inches=0.07)

print('Complete./')
