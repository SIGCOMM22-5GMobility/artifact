#!/usr/bin/env python3
from os import path
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.patches import Patch

from utils.context import data_processed_dir, plot_dir
from utils.utils import plot_handler, colorlist20, get_cdf, get_std

# comment out these lines if latex not installed
plt.rc('font', family='sans-serif', serif='cm10')
plt.rc('text', usetex=True)

############### Config ####################
SHOW_PLOT_FLAG = False
DATA_FOLDER = path.join(data_processed_dir, 'figure9-ho_exec_duration')

# load data
df = pd.read_csv(path.join(DATA_FOLDER, 'HO-Duration_Combined.csv'))

# do preprocessing
df['HO'] = df['HO'] + df['RCH']
vzw_df = df[df['Operator'] == 'VZW']
tmb_df = df[df['Operator'] == 'TMB']

### verizon ###
vzw_lte_ho_dur = get_cdf(vzw_df[(vzw_df['Type'] == 'PCell') &
                                (vzw_df['Tech'] == 'LTE')]['HO'].to_numpy() * 1000)
vzw_nsa_mcg_ho_dur = get_cdf(vzw_df[(vzw_df['Type'] == 'PCell') &
                                    (vzw_df['Tech'] == 'NSA')]['HO'].to_numpy() * 1000)
vzw_nsa_scg_add_ho_dur = get_cdf(vzw_df[(vzw_df['Type'] == 'SCG Add.') &
                                        (vzw_df['Tech'] == 'NSA')]['HO'].to_numpy() * 1000)
vzw_nsa_scg_mod_ho_dur = get_cdf(vzw_df[(vzw_df['Type'] == 'SCG Mod.') &
                                        (vzw_df['Tech'] == 'NSA')]['HO'].to_numpy() * 1000)
vzw_nsa_scg_rel_ho_dur = get_cdf(vzw_df[(vzw_df['Type'] == 'SCG Rel.') &
                                        (vzw_df['Tech'] == 'NSA')]['HO'].to_numpy() * 1000)
vzw_nsa_menb_ho_dur = get_cdf(vzw_df[(vzw_df['Type'] == 'MCG') &
                                     (vzw_df['Tech'] == 'NSA')]['HO'].to_numpy() * 1000)

# Low-Band
vzw_nsa_low_mcg_ho_dur = get_cdf(vzw_df[(vzw_df['Type'] == 'PCell') &
                                        (vzw_df['Tech'] == 'NSA') &
                                        (vzw_df['Band'] == 'Low')]['HO'].to_numpy() * 1000)
vzw_nsa_low_scg_add_ho_dur = get_cdf(vzw_df[(vzw_df['Type'] == 'SCG Add.') &
                                            (vzw_df['Tech'] == 'NSA') &
                                            (vzw_df['Band'] == 'Low')]['HO'].to_numpy() * 1000)
vzw_nsa_low_scg_mod_ho_dur = get_cdf(vzw_df[(vzw_df['Type'] == 'SCG Mod.') &
                                            (vzw_df['Tech'] == 'NSA') &
                                            (vzw_df['Band'] == 'Low')]['HO'].to_numpy() * 1000)
vzw_nsa_low_scg_rel_ho_dur = get_cdf(vzw_df[(vzw_df['Type'] == 'SCG Rel.') &
                                            (vzw_df['Tech'] == 'NSA') &
                                            (vzw_df['Band'] == 'Low')]['HO'].to_numpy() * 1000)

# mmWave
vzw_nsa_mm_mcg_ho_dur = get_cdf(vzw_df[(vzw_df['Type'] == 'PCell') &
                                       (vzw_df['Tech'] == 'NSA') &
                                       (vzw_df['Band'] == 'MM')]['HO'].to_numpy() * 1000)
vzw_nsa_mm_scg_add_ho_dur = get_cdf(vzw_df[(vzw_df['Type'] == 'SCG Add.') &
                                           (vzw_df['Tech'] == 'NSA') &
                                           (vzw_df['Band'] == 'MM')]['HO'].to_numpy() * 1000)
vzw_nsa_mm_scg_mod_ho_dur = get_cdf(vzw_df[(vzw_df['Type'] == 'SCG Mod.') &
                                           (vzw_df['Tech'] == 'NSA') &
                                           (vzw_df['Band'] == 'MM')]['HO'].to_numpy() * 1000)
vzw_nsa_mm_scg_rel_ho_dur = get_cdf(vzw_df[(vzw_df['Type'] == 'SCG Rel.') &
                                           (vzw_df['Tech'] == 'NSA') &
                                           (vzw_df['Band'] == 'MM')]['HO'].to_numpy() * 1000)

### t-mobile ###
tmb_lte_ho_dur = get_cdf(tmb_df[(tmb_df['Type'] == 'PCell') &
                                (tmb_df['Tech'] == 'LTE')]['HO'].to_numpy() * 1000)
tmb_nsa_mcg_ho_dur = get_cdf(tmb_df[(tmb_df['Type'] == 'PCell') & (tmb_df['Band'] == 'Mid') &
                                    (tmb_df['Tech'] == 'NSA')]['HO'].to_numpy() * 1000)
tmb_nsa_scg_add_ho_dur = get_cdf(tmb_df[(tmb_df['Type'] == 'SCG Add.') & (tmb_df['Band'] == 'Mid') &
                                        (tmb_df['Tech'] == 'NSA')]['HO'].to_numpy() * 1000)
tmb_nsa_scg_mod_ho_dur = get_cdf(tmb_df[(tmb_df['Type'] == 'SCG Mod.') & (tmb_df['Band'] == 'Mid') &
                                        (tmb_df['Tech'] == 'NSA')]['HO'].to_numpy() * 1000)
tmb_nsa_scg_rel_ho_dur = get_cdf(tmb_df[(tmb_df['Type'] == 'SCG Rel.') & (tmb_df['Band'] == 'Mid') &
                                        (tmb_df['Tech'] == 'NSA')]['HO'].to_numpy() * 1000)
tmb_nsa_menb_ho_dur = get_cdf(tmb_df[(tmb_df['Type'] == 'MCG') & (tmb_df['Band'] == 'Mid') &
                                     (tmb_df['Tech'] == 'NSA')]['HO'].to_numpy() * 1000)
tmb_sa_mcg_ho_dur = get_cdf(tmb_df[(tmb_df['Type'] == 'MCG') &
                                   (tmb_df['Tech'] == 'SA')]['HO'].to_numpy() * 1000)
#### Plot graph
if True:  # use truth value to turn on and off plotting
    plot_id = 'figure9'
    plot_name = 'ho-exec-duration'
    plt.close('all')
    fig, (ax, ax2) = plt.subplots(2, 1, figsize=(6, 2.75), sharex='all',
                                  gridspec_kw={'height_ratios': [4, 3]})
    fig.tight_layout()
    plt.subplots_adjust(wspace=0.2, bottom=-0.1)

    width = 0.65
    pos = [0, 1, 2, 3, 4]
    lte_c_idx = 0
    nsa_c_idx = 2
    sa_c_idx = 4
    color_idx_list = [lte_c_idx, nsa_c_idx, nsa_c_idx, nsa_c_idx, sa_c_idx]
    fc_list = [colorlist20[x + 1] for x in color_idx_list]
    ec_list = [colorlist20[x] for x in color_idx_list]

    lte_ho_mean = np.mean(tmb_lte_ho_dur[0])
    nsa_lte_lte_ho_mean = np.mean(tmb_nsa_scg_rel_ho_dur[0]) + np.mean(tmb_nsa_mcg_ho_dur[0]) + \
                          np.mean(tmb_nsa_scg_add_ho_dur[0])
    nsa_nr_nr_ho_mean = np.mean(tmb_nsa_scg_rel_ho_dur[0]) + np.mean(tmb_nsa_scg_add_ho_dur[0])
    nsa_scg_mod_ho_mean = np.mean(tmb_nsa_scg_mod_ho_dur[0])
    sa_ho_mean = np.mean(tmb_sa_mcg_ho_dur[0])

    lte_ho_std = get_std(tmb_lte_ho_dur[0])
    nsa_lte_lte_ho_std = get_std(tmb_nsa_scg_rel_ho_dur[0]) + get_std(tmb_nsa_mcg_ho_dur[0]) + \
                         get_std(tmb_nsa_scg_add_ho_dur[0])
    nsa_nr_nr_ho_std = get_std(tmb_nsa_scg_rel_ho_dur[0]) + get_std(tmb_nsa_scg_add_ho_dur[0])
    nsa_scg_mod_ho_std = get_std(tmb_nsa_scg_mod_ho_dur[0])
    sa_ho_std = get_std(tmb_sa_mcg_ho_dur[0])

    mean_list = [lte_ho_mean, nsa_lte_lte_ho_mean, nsa_nr_nr_ho_mean, nsa_scg_mod_ho_mean, sa_ho_mean]
    std_list = [lte_ho_std, nsa_lte_lte_ho_std, nsa_nr_nr_ho_std, nsa_scg_mod_ho_std, sa_ho_std]

    ## subplot 1
    container = ax.barh(pos, mean_list, width,
                        alpha=1, zorder=3, color=fc_list, ec=ec_list)

    for x, y, err, color in zip(pos, mean_list, std_list, ec_list):
        ax.errorbar(y, x, xerr=err, lw=1.5, capsize=3, capthick=1.5, color=color, zorder=4)

    ax.set_title('OpY (LTE vs. NSA vs. SA)', fontsize=17)
    ax.set_ylim([-0.5, 4.5])
    ax.set_yticks(pos)
    ax.set_yticklabels(['LTEH', 'LTEH', 'SCGC', 'SCGM', 'MCGH'], fontsize=11)
    ax.xaxis.grid(color='gainsboro', linestyle='dashed', zorder=1)
    ax.tick_params(axis='both', which='major', labelsize=12, left=False, bottom=False)
    ax.tick_params(axis='y', which='major')

    ax.bar([-10], [10], color=colorlist20[1], ec=colorlist20[0], label='LTE (over Mid-Band)')
    ax.bar([-10], [10], color=colorlist20[3], ec=colorlist20[2], label='NSA (over Mid-Band)')
    ax.bar([-10], [10], color=colorlist20[5], ec=colorlist20[4], label='SA (over Low-Band)')

    lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
    lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
    ax.legend(lines, labels, loc='upper right',
              ncol=1, bbox_to_anchor=(1.01, 1.05), facecolor='#dddddd', columnspacing=0.4,
              handlelength=2, framealpha=.8, fontsize=15, borderpad=0.2, labelspacing=.2, handletextpad=0.75)

    ## subplot 2

    width = 0.4
    pos = [0, 1]
    low_c_idx = 18
    mm_c_idx = 6
    fc_low_list = [colorlist20[low_c_idx + 1], colorlist20[low_c_idx + 1]]
    ec_low_list = [colorlist20[low_c_idx], colorlist20[low_c_idx]]
    fc_mm_list = [colorlist20[mm_c_idx + 1], colorlist20[mm_c_idx + 1]]
    ec_mm_list = [colorlist20[mm_c_idx], colorlist20[mm_c_idx]]

    vzw_nsa_low_mcg_ho_mean = np.mean(vzw_nsa_low_scg_rel_ho_dur[0]) + np.mean(vzw_nsa_low_mcg_ho_dur[0]) + \
                              np.mean(vzw_nsa_low_scg_add_ho_dur[0])
    vzw_nsa_low_nr_nr_ho_mean = np.mean(vzw_nsa_low_scg_rel_ho_dur[0]) + np.mean(vzw_nsa_low_scg_add_ho_dur[0])
    vzw_nsa_mm_mcg_ho_mean = np.mean(vzw_nsa_mm_scg_rel_ho_dur[0]) + np.mean(vzw_nsa_mm_mcg_ho_dur[0]) + \
                             np.mean(vzw_nsa_mm_scg_add_ho_dur[0])
    vzw_nsa_mm_nr_nr_ho_mean = np.mean(vzw_nsa_mm_scg_rel_ho_dur[0]) + np.mean(vzw_nsa_mm_scg_add_ho_dur[0])

    vzw_nsa_low_mcg_ho_std = get_std(vzw_nsa_low_scg_rel_ho_dur[0]) + get_std(vzw_nsa_low_mcg_ho_dur[0]) + \
                             get_std(vzw_nsa_low_scg_add_ho_dur[0])
    vzw_nsa_low_nr_nr_ho_std = get_std(vzw_nsa_low_scg_rel_ho_dur[0]) + get_std(vzw_nsa_low_scg_add_ho_dur[0])
    vzw_nsa_mm_mcg_ho_std = get_std(vzw_nsa_mm_scg_rel_ho_dur[0]) + get_std(vzw_nsa_mm_mcg_ho_dur[0]) + \
                            get_std(vzw_nsa_mm_scg_add_ho_dur[0])
    vzw_nsa_mm_nr_nr_ho_std = get_std(vzw_nsa_mm_scg_rel_ho_dur[0]) + get_std(vzw_nsa_mm_scg_add_ho_dur[0])

    mean_list_low = [vzw_nsa_low_mcg_ho_mean, vzw_nsa_low_nr_nr_ho_mean]
    mean_list_mm = [vzw_nsa_mm_mcg_ho_mean, vzw_nsa_mm_nr_nr_ho_mean]
    std_list_low = [vzw_nsa_low_mcg_ho_std, vzw_nsa_low_nr_nr_ho_std]
    std_list_mm = [vzw_nsa_mm_mcg_ho_std, vzw_nsa_mm_nr_nr_ho_std]

    container = ax2.barh(pos, mean_list_low, width,
                         alpha=1, zorder=3, color=fc_low_list, ec=ec_low_list)

    for x, y, err, color in zip(pos, mean_list_low, std_list_low, ec_low_list):
        ax2.errorbar(y, x, xerr=err, lw=1.5, capsize=3, capthick=1.5, color=color, zorder=4)

    container = ax2.barh([x + width for x in pos], mean_list_mm, width,
                         alpha=1, zorder=3, color=fc_mm_list, ec=ec_mm_list)

    for x, y, err, color in zip(pos, mean_list_mm, std_list_mm, ec_mm_list):
        ax2.errorbar(y, x + width, xerr=err, lw=1.5, capsize=3, capthick=1.5, color=color, zorder=4)

    ax2.set_title('OpX (NSA Low-Band vs. NSA mmWave)', fontsize=17)
    ax2.set_xlim([0, 250])
    ax2.set_xticks(np.arange(0, 250, 20))
    ax2.set_ylim([-0.3, 1.725])
    ax2.set_xlabel('Duration (ms)', fontsize=16)
    ax2.set_yticks([0 + width / 2, 1 + width / 2])
    ax2.set_yticklabels(['LTEH', 'SCGC'], fontsize=11)
    ax2.xaxis.grid(color='gainsboro', linestyle='dashed', zorder=-1)
    ax2.tick_params(axis='both', which='major', labelsize=12, left=False)
    ax2.tick_params(axis='y', which='major')
    ax2.tick_params(axis='x', which='major', labelsize=15)

    ax3 = fig.add_subplot(111, zorder=-1)
    for _, spine in ax3.spines.items():
        spine.set_visible(False)
    ax3.tick_params(labelleft=False, labelbottom=False, left=False, right=False)
    ax3.get_shared_x_axes().join(ax3, ax)
    ax3.set_xlim([0, 250])
    ax3.set_xticks(np.arange(0, 250, 20))
    ax3.xaxis.grid(color='gainsboro', linestyle='dashed', zorder=1)

    bar1 = ax2.bar([-10], [10], color=colorlist20[19], ec=colorlist20[18], label='Low-Band')
    bar2 = ax2.bar([-10], [10], color=colorlist20[7], ec=colorlist20[6], label='mmWave')

    patches = [Patch(facecolor=colorlist20[19], edgecolor=colorlist20[18], label='Low-Band'),
               Patch(facecolor=colorlist20[7], edgecolor=colorlist20[6], label='mmWave')]

    ax2.legend(handles=patches, loc='upper right',
               ncol=1, bbox_to_anchor=(1.015, 1.07), facecolor='#dddddd', columnspacing=0.4,
               handlelength=2, framealpha=.8, fontsize=15, borderpad=0.2, labelspacing=.2, handletextpad=0.75)

    plot_handler(plt, plot_id, plot_name, plot_dir, show_flag=SHOW_PLOT_FLAG, ignore_eps=True, pad_inches=0.07)

print('Complete./')
