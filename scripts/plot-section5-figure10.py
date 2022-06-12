#!/usr/bin/env python3
import json
from os import path
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Patch

from utils.context import data_processed_dir, plot_dir
from utils.utils import plot_handler, colorlist20, get_std

# comment out these lines if latex not installed
plt.rc('font', family='sans-serif', serif='cm10')
plt.rc('text', usetex=True)

############### Config ####################
SHOW_PLOT_FLAG = False
PROCESSED_DATA_FOLDER = path.join(data_processed_dir, "figure10-ho_energy_consumption")
COMBINED_DATA_FILE = path.join(PROCESSED_DATA_FOLDER, f"handoff-energy_combined.csv")
BASELINE_DATA_FILE = path.join(PROCESSED_DATA_FOLDER, "baseline_combined.csv")
DISTANCE_DICT = json.load(open(path.join(PROCESSED_DATA_FOLDER, 'distance.json')))
DISTANCE_REFERENCE = 1000  # in meters
MID_BAND_LTE_HO = DISTANCE_REFERENCE / DISTANCE_DICT['MID_BAND_LTE_HO']
LOW_BAND_SCG_ADD = DISTANCE_REFERENCE / DISTANCE_DICT['LOW_BAND_SCG_ADD']
LOW_BAND_SCG_MOD = DISTANCE_REFERENCE / DISTANCE_DICT['LOW_BAND_SCG_MOD']
LOW_BAND_SCG_REL = DISTANCE_REFERENCE / DISTANCE_DICT['LOW_BAND_SCG_REL']
MMWAVE_SCG_ADD = DISTANCE_REFERENCE / DISTANCE_DICT['MMWAVE_SCG_ADD']
MMWAVE_SCG_MOD = DISTANCE_REFERENCE / DISTANCE_DICT['MMWAVE_SCG_MOD']
MMWAVE_SCG_REL = DISTANCE_REFERENCE / DISTANCE_DICT['MMWAVE_SCG_REL']

########### Data Preprocessing ############
baseline_df = pd.read_csv(BASELINE_DATA_FILE)
logging_df = baseline_df[baseline_df['type'] == 'logging']
df_raw = pd.read_csv(COMBINED_DATA_FILE)
mpa_df = df_raw[df_raw['location'] == 'MPA'].copy(deep=True)
mrchms_df = df_raw[df_raw['location'] == 'MRCHMS'].copy(deep=True)
mrchmss_df = df_raw[df_raw['location'] == 'MRCHMSS'].copy(deep=True)

## mmwave
mpa_df['mmwave_promotion'] = (mpa_df['network'] != 'mmwave') & (mpa_df['network'].shift(-1) == 'mmwave')
mpa_df['mmwave_demotion'] = (mpa_df['network'] == 'mmwave') & (mpa_df['network'].shift(-1) != 'mmwave')
mpa_df['mmwave_modification'] = (mpa_df['mmwave_demotion']) & (mpa_df['mmwave_promotion'].shift(-2))
mpa_df['mmwave_demotion'] = (mpa_df['mmwave_demotion']) & (~mpa_df['mmwave_modification'])
lte_mpa_df = mpa_df[mpa_df['network'] == 'lte']
mmwave_mpa_df = mpa_df[mpa_df['network'] == 'mmwave']
low_mpa_df = mpa_df[mpa_df['network'] == 'nsa']
mmwave_pro_mpa_df = mpa_df[mpa_df['mmwave_promotion']]
mmwave_dem_mpa_df = mpa_df[mpa_df['mmwave_demotion']]
mmwave_mod_mpa_df = mpa_df[mpa_df['mmwave_modification']]
mmwave_scg_add = mmwave_pro_mpa_df['hw_avg_power'].mean()
mmwave_scg_mod = mmwave_mod_mpa_df['hw_avg_power'].mean()
mmwave_scg_rel = mmwave_dem_mpa_df['hw_avg_power'].mean()
mmwave_scg_add_std = get_std(mmwave_pro_mpa_df['hw_avg_power'], 1)
mmwave_scg_mod_std = get_std(mmwave_mod_mpa_df['hw_avg_power'])
mmwave_scg_rel_std = get_std(mmwave_dem_mpa_df['hw_avg_power'], 1)
mmwave_scg_add_baseline = mmwave_scg_add - logging_df['hw_avg_power'].mean()
mmwave_scg_mod_baseline = mmwave_scg_mod - logging_df['hw_avg_power'].mean()
mmwave_scg_rel_baseline = mmwave_scg_rel - logging_df['hw_avg_power'].mean()

## low-band (mrchms)
mrchms_df['lte_ho'] = (mrchms_df['pci'] != mrchms_df['pci'].shift(-1))
mrchms_df['nsa_ho'] = (mrchms_df['nr_pci'] != mrchms_df['nr_pci'].shift(-1))
mrchms_df['lte_ho'] = mrchms_df['lte_ho'] & ~mrchms_df['nsa_ho']  # remove lte mod ho type
nsa_mrchms_df = mrchms_df[mrchms_df['network'] == 'nsa']
lte_ho_mrchms_df = mrchms_df[mrchms_df['lte_ho']]
nsa_mod_mrchms_df = mrchms_df[mrchms_df['nsa_ho']]
lte_mod_mrchms_df = mrchms_df[mrchms_df['lte_ho'] & mrchms_df['nsa_ho']]
low_scg_mod = nsa_mod_mrchms_df['hw_avg_power'].mean()
low_scg_mod_std = get_std(nsa_mod_mrchms_df['hw_avg_power'], 1)
mid_lte_ho = lte_ho_mrchms_df['hw_avg_power'].mean()
mid_lte_ho_std = get_std(lte_ho_mrchms_df['hw_avg_power'], 1)
mid_lte_ho_baseline = mid_lte_ho - logging_df['hw_avg_power'].mean()

## low-band (mrchmss)
mrchmss_df['hw_avg_power_new'] = mrchmss_df['hw_avg_power'].rolling(window=5).max()
mrchmss_df['nsa_promotion'] = (mrchmss_df['network'] != 'nsa') & (mrchmss_df['network'].shift(-1) == 'nsa')
mrchmss_df['nsa_demotion'] = (mrchmss_df['network'] == 'nsa') & (mrchmss_df['network'].shift(-1) != 'nsa')
nsa_dem_mrchmss_df = mrchmss_df[mrchmss_df['nsa_demotion']]
nsa_pro_mrchmss_df = mrchmss_df[mrchmss_df['nsa_promotion']]
low_scg_add = nsa_pro_mrchmss_df['hw_avg_power_new'].mean()
low_scg_add_std = get_std(nsa_pro_mrchmss_df['hw_avg_power_new'], 1)
low_scg_rel = nsa_dem_mrchmss_df['hw_avg_power'].mean()
low_scg_rel_std = get_std(nsa_dem_mrchmss_df['hw_avg_power'], 1)
low_scg_add_baseline = low_scg_add - logging_df['hw_avg_power'].mean()
low_scg_mod_baseline = low_scg_mod - logging_df['hw_avg_power'].mean()
low_scg_rel_baseline = low_scg_rel - logging_df['hw_avg_power'].mean()

##### calculate average power consumption #####
mid_lte_ho_pwr = mid_lte_ho_baseline * MID_BAND_LTE_HO
low_scg_add_pwr = low_scg_add_baseline * LOW_BAND_SCG_ADD
low_scg_mod_pwr = low_scg_mod_baseline * LOW_BAND_SCG_MOD
low_scg_rel_pwr = low_scg_rel_baseline * LOW_BAND_SCG_REL
mmwave_scg_add_pwr = mmwave_scg_add_baseline * MMWAVE_SCG_ADD
mmwave_scg_mod_pwr = mmwave_scg_mod_baseline * MMWAVE_SCG_MOD
mmwave_scg_rel_pwr = mmwave_scg_rel_baseline * MMWAVE_SCG_REL

#### Plot graph
if True:  # use truth value to turn on and off plotting
    plot_id = 'figure10'
    plot_name = 'ho-energy-comparison'
    plt.close('all')
    fig, ax = plt.subplots(figsize=(5.94, 2.5))
    fig.tight_layout()
    axr = ax.twinx()

    x = [0.5, 2, 3, 4, 5.5, 6.5, 7.5]
    width = 0.35
    pad = 0.075
    lc_idx = 0
    rc_idx = 2

    x_labels = ['LTE HO', 'SCG Rel.', 'SCG Mod.', 'SCG Add.', 'SCG Rel.', 'SCG Mod.', 'SCG Add.']
    hatch_list = ('--', '//', 'xx', 'O', '//', 'xx', 'O')

    y = [mid_lte_ho_baseline,
         low_scg_add_baseline,
         low_scg_mod_baseline,
         low_scg_rel_baseline,
         mmwave_scg_add_baseline,
         mmwave_scg_mod_baseline,
         mmwave_scg_rel_baseline]
    y = [ele / 1000 for ele in y]
    y_err = [mid_lte_ho_std,
             low_scg_add_std,
             low_scg_mod_std,
             low_scg_rel_std,
             mmwave_scg_add_std,
             mmwave_scg_mod_std,
             mmwave_scg_rel_std]
    y_err = [ele / 1000 for ele in y_err]

    container = ax.bar(x, y, width, alpha=1, zorder=2, color=colorlist20[lc_idx+1], ec=colorlist20[lc_idx], fill=False)
    for pos, y, err in zip(x, y, y_err):
        ax.errorbar(pos, y, err, lw=1.25, capsize=2, capthick=1.5, color=colorlist20[lc_idx], zorder=4)
    for bar, pattern in zip(container, hatch_list):
        bar.set_hatch(pattern)

    y = [mid_lte_ho_pwr,
         low_scg_add_pwr,
         low_scg_mod_pwr,
         low_scg_rel_pwr,
         mmwave_scg_add_pwr,
         mmwave_scg_mod_pwr,
         mmwave_scg_rel_pwr]
    y = [ele / 1000 for ele in y]

    container = axr.bar([x_ + width + pad for x_ in x],
                        y, width, alpha=1, zorder=2, color=colorlist20[rc_idx+1], ec=colorlist20[rc_idx], fill=False)
    for bar, pattern in zip(container, hatch_list):
        bar.set_hatch(pattern)

    ax.set_ylabel('power consumed\nper HO (W)', fontsize=22, color=colorlist20[lc_idx])
    # ax.yaxis.set_label_coords(-0.06, 0.4)
    ax.set_ylim([0, 3.1])
    ax.set_yticks([0, 1, 2])
    ax.set_xticks([0.5 + (width+pad)/2, 3 + (width+pad)/2, 6.5 + (width+pad)/2])
    ax.set_xticklabels(['LTE\n(Mid-Band)', 'NSA\n(Low-band)', 'NSA\n(mmWave)'])
    ax.tick_params(axis='x', which='both', labelsize=19)
    ax.tick_params(axis='y', which='major', labelsize=18, colors=colorlist20[lc_idx])
    ax.yaxis.grid(color='gainsboro', linestyle='dashed', zorder=1)

    axr.set_ylabel('power per unit \ndistance (W/Km)', fontsize=22, color=colorlist20[rc_idx])
    # axr.yaxis.set_label_coords(1.07, 0.35)
    axr.set_ylim([0, 15.5])
    axr.set_yticks([0, 5, 10])
    axr.set_xlim([0.1, 8.4])
    axr.tick_params(axis='y', which='both', labelsize=18, colors=colorlist20[rc_idx])

    patches = [Patch(fc=(0, 0, 0, 0), edgecolor='black', label='LTEH', hatch=hatch_list[0]),
               Patch(fc=(0, 0, 0, 0), edgecolor='black', label='SCGA', hatch=hatch_list[1]),
               Patch(fc=(0, 0, 0, 0), edgecolor='black', label='SCGM', hatch=hatch_list[2]),
               Patch(fc=(0, 0, 0, 0), edgecolor='black', label='SCGR', hatch=hatch_list[3])]

    ax.legend(handles=patches, loc='upper center',
              ncol=4, bbox_to_anchor=(0.5, 1.07), facecolor='#dddddd', columnspacing=0.4,
              handlelength=2, framealpha=.8, fontsize=19, borderpad=0.1, labelspacing=.15, handletextpad=0.25)

    plot_handler(plt, plot_id, plot_name, plot_dir, show_flag=SHOW_PLOT_FLAG, ignore_eps=True, pad_inches=0.07)

print('Complete./')
