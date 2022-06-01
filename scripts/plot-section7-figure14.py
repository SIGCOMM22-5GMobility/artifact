#!/usr/bin/env python3
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import numpy as np
import pandas as pd
from os import path
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
import matplotlib.gridspec as gridspec
import json

from utils.context import data_processed_dir, plot_dir
from utils.utils import plot_handler, colorlist20, remove_nan

plt.rc('font', family='sans-serif', serif='cm10')
plt.rc('text', usetex=True)

matplotlib.use('Agg') # used just for saving figures

## Config
SHOW_PLOT_FLAG = False
EXPR_TYPE = 'figure14-16k_and_volumetric_video/volumetric-emulation'
DATA_FOLDER = path.join(data_processed_dir, EXPR_TYPE)
VOD_DATA_FOLDER=path.join(data_processed_dir, 'figure14-16k_and_volumetric_video/16k-vod-emulation')
# print(DATA_FOLDER)

## read all data here
file_list = [
                'vivo-wo-ho-sub.csv',
                'vivo-w-ho-sub.csv',
                'festive-wo-ho.csv',
                'festive-w-ho.csv',
                'vivo-w-ho-gt-sub.csv',
                'festive-w-ho-gt.csv'
            ]

data = {}
for file_name in file_list:
    file_path = path.join(DATA_FOLDER, file_name)
    data[file_name[:-4]] = pd.read_csv(file_path)
# print(data)


data_f = open(VOD_DATA_FOLDER+'/summary.json')
data_vod = json.load(data_f)
data_pred = open(VOD_DATA_FOLDER+'/predict_summary.json')
data_vod_pred = json.load(data_pred)
colormap = {'RBHO': 'navy', 'robustMPCGT': 'violet', 'RB': 'brown', 'robustMPC': 'darkgreen', 'robustMPCHO': 'r', 'fastMPC': 'darkorange', 'fastMPCHO': 'b',
            'fastMPCGT': 'maroon', 'RBHOGT': 'purple'}


## preprocess data
quality_avg = []
quality_std = []
stall_avg = []
stall_std = []
for key in data.keys():
    for i in range(0, len(data[key]['quality'])):
        data[key]['quality'][i] = (data[key]['quality'][i] + 1) / 5
        data[key]['stall'][i] = data[key]['stall'][i] * 100 / (5824 / 30)
for key in data.keys():
    quality_avg.append(data[key]['quality'].mean())
    quality_std.append(data[key]['quality'].std() / 2)
    stall_avg.append(data[key]['stall'].mean())
    stall_std.append(data[key]['stall'].std() / 2)
# for key in data.keys():
#     quality_avg.append((data[key]['quality'].mean() + 1) / 5)
#     quality_std.append(data[key]['quality'].std() / (5 * 2))
#     stall_avg.append(data[key]['stall'].mean() * 100 / (5824 / 30))
#     stall_std.append(data[key]['stall'].std() * 100 / ((5824 / 30) * 2))
quality_improve = {'ViVo-PR':[], 'FESTIVE-PR':[], 'ViVo-GT':[], 'FESTIVE-GT':[]}
stall_improve = {'ViVo-PR':[], 'FESTIVE-PR':[], 'ViVo-GT':[], 'FESTIVE-GT':[]}

quality_improve['ViVo-PR'].append((data['vivo-w-ho-sub']['quality'] - data['vivo-wo-ho-sub']['quality']).mean() * 100)
quality_improve['ViVo-PR'].append((data['vivo-w-ho-sub']['quality'] - data['vivo-wo-ho-sub']['quality']).std() * 100)
stall_improve['ViVo-PR'].append((data['vivo-w-ho-sub']['stall'] - data['vivo-wo-ho-sub']['stall']).mean())
stall_improve['ViVo-PR'].append((data['vivo-w-ho-sub']['stall'] - data['vivo-wo-ho-sub']['stall']).std())

quality_improve['FESTIVE-PR'].append((data['festive-w-ho']['quality'] - data['festive-wo-ho']['quality']).mean() * 100)
quality_improve['FESTIVE-PR'].append((data['festive-w-ho']['quality'] - data['festive-wo-ho']['quality']).std() * 100)
stall_improve['FESTIVE-PR'].append((data['festive-w-ho']['stall'] - data['festive-wo-ho']['stall']).mean())
stall_improve['FESTIVE-PR'].append((data['festive-w-ho']['stall'] - data['festive-wo-ho']['stall']).std())

quality_improve['ViVo-GT'].append((data['vivo-w-ho-gt-sub']['quality'] - data['vivo-wo-ho-sub']['quality']).mean() * 100)
quality_improve['ViVo-GT'].append((data['vivo-w-ho-gt-sub']['quality'] - data['vivo-wo-ho-sub']['quality']).std() * 100)
stall_improve['ViVo-GT'].append((data['vivo-w-ho-gt-sub']['stall'] - data['vivo-wo-ho-sub']['stall']).mean())
stall_improve['ViVo-GT'].append((data['vivo-w-ho-gt-sub']['stall'] - data['vivo-wo-ho-sub']['stall']).std())

quality_improve['FESTIVE-GT'].append((data['festive-w-ho-gt']['quality'] - data['festive-wo-ho']['quality']).mean() * 100)
quality_improve['FESTIVE-GT'].append((data['festive-w-ho-gt']['quality'] - data['festive-wo-ho']['quality']).std() * 100)
stall_improve['FESTIVE-GT'].append((data['festive-w-ho-gt']['stall'] - data['festive-wo-ho']['stall']).mean())
stall_improve['FESTIVE-GT'].append((data['festive-w-ho-gt']['stall'] - data['festive-wo-ho']['stall']).std())
# print(quality_avg)
# print(quality_std)
# print(stall_avg)
# print(stall_std)
# print((data['vivo-w-ho-sub']['quality'].mean() - data['vivo-wo-ho-sub']['quality'].mean()) * 100 / data['vivo-wo-ho-sub']['quality'].mean())
# print((data['festive-w-ho']['quality'].mean() - data['festive-wo-ho']['quality'].mean()) * 100 / data['festive-wo-ho']['quality'].mean())
# print((data['vivo-w-ho-sub']['stall'].mean() - data['vivo-wo-ho-sub']['stall'].mean()) * 100 / data['vivo-wo-ho-sub']['stall'].mean())
# print((data['festive-w-ho-gt']['stall'].mean() - data['festive-wo-ho']['stall'].mean()) * 100 / data['festive-wo-ho']['stall'].mean())
# print(quality_improve['ViVo-PR'][0] - quality_improve['ViVo-GT'][0])
# print(quality_improve['FESTIVE-PR'][0] - quality_improve['FESTIVE-GT'][0])
# print(stall_improve['ViVo-PR'][0] - stall_improve['ViVo-GT'][0])
# print(stall_improve['FESTIVE-PR'][0] - stall_improve['FESTIVE-GT'][0])
schemes = data_vod.keys()
pred_schemes = data_vod_pred.keys()

## plot data
if True:
    plot_id = '50a'
    plot_name = 'volumetric-qoe'
    plt.close('all')
    # fig, ax = plt.subplots(figsize=(4, 1.85))
    fig = plt.figure(figsize=(18, 4.5), constrained_layout=True)
    subfigs = fig.subfigures(1, 3, width_ratios=[3.5, 3, 3.5])
    ax0, ax1, ax2 = subfigs.flat[0].subplots(3, 1, sharex=True), subfigs.flat[1].subplots(1, 1), subfigs.flat[2].subplots(1, 2, sharey=True)
    # fig, (ax0, ax1, ax2) = plt.subplots(1, 3, figsize=(17, 3.5), gridspec_kw={'width_ratios': [4, 3, 3]})
    labels = {'ViVo':'ViVo', 'ViVo-PR':'ViVo-PR', 'FESTIVE':'FESTIVE', 'FESTIVE-PR':'FESTIVE-PR', 'ViVo-GT':'ViVo-GT', 'FESTIVE-GT':'FESTIVE-GT'}
    markers = {'ViVo':'o', 'ViVo-PR':'^', 'FESTIVE':'o', 'FESTIVE-PR':'^', 'ViVo-GT':'o', 'FESTIVE-GT':'o'}
    colors = {'ViVo':'violet', 'ViVo-PR':'r', 'FESTIVE':'brown', 'FESTIVE-PR':'navy', 'ViVo-GT':'darkgreen', 'FESTIVE-GT':'darkorange'}
    linestyles = {'ViVo':'--', 'ViVo-PR':'-', 'FESTIVE':'--', 'FESTIVE-PR':'-', 'ViVo-GT':'--', 'FESTIVE-GT':'--'}
    fontsize = 22
    fontsize_label = 20
    ## TODO: update the volumetric video results here (Anlan)
    # for key in quality_improve.keys():
    #     if(key == 'ViVo-GT' or key == 'ViVo-PR'):
    #         myax = ax2[0]
    #     else:
    #         myax = ax2[1]
    #     # ax2.scatter(stall_improve[key][0], quality_improve[key][0], label=key, marker=markers[key], color=colors[key])
    #     # eb = ax2.errorbar(stall_improve[key][0], quality_improve[key][0], xerr=stall_improve[key][1], yerr=quality_improve[key][1], color=colors[key], capsize=6, lw=2, capthick=2)
    #     myax.scatter(stall_improve[key][0], quality_improve[key][0], label=key, marker=markers[key], color=colors[key])
    #     eb = myax.errorbar(stall_improve[key][0], quality_improve[key][0], xerr=stall_improve[key][1], yerr=quality_improve[key][1], color=colors[key], capsize=6, lw=2, capthick=2)
    #     eb[-1][0].set_linestyle(linestyles[key])
    #     eb[-1][1].set_linestyle(linestyles[key])
    #     if(key == 'ViVo-GT' or key == 'FESTIVE-GT'):
    #         eb[-1][0].set_dashes((0, (5, 5)))
    #         eb[-1][1].set_dashes((0, (5, 5)))
    #     if(key == 'ViVo-GT'):
    #         myax.annotate(key, (stall_improve[key][0] + 0.1, quality_improve[key][0] - 7.0), color=colors[key], fontsize=fontsize_label)
    #     if(key == 'ViVo-PR'):
    #         myax.annotate("$\\textit{%s}$" % key, (stall_improve[key][0] + 0.11, quality_improve[key][0] + 3.0), color=colors[key], fontsize=fontsize_label)
    #         # myax.annotate("$\\textit{%s}$" % key, color=colors[key], fontsize=fontsize_label, horizontalalignment="center", xy=(stall_improve[key][0], quality_improve[key][0]), xycoords='data',
    #         #         xytext=(stall_improve[key][0] - 0.5, quality_improve[key][0] + 30.0), textcoords='data', arrowprops=dict(arrowstyle="<-, head_width=0.15, head_length=0.15", connectionstyle="arc3,rad=-0.3", lw=1, color=colors[key], linestyle = '--'))
    #     if(key == 'FESTIVE-GT'):
    #         myax.annotate(key, (stall_improve[key][0] + 0.2, quality_improve[key][0] + 30.0), color=colors[key], fontsize=17)
    #     if(key == 'FESTIVE-PR'):
    #         myax.annotate("$\\textit{%s}$" % key, (stall_improve[key][0] + 0.6, quality_improve[key][0] - 33.0), color=colors[key], fontsize=17)
    # ax2[0].annotate("Better QoE", fontsize=fontsize, horizontalalignment="center", xy=(-0.03, 45.0), xycoords='data',
    #                 xytext=(0.02, 30.0), textcoords='data', arrowprops=dict(arrowstyle="->, head_width=0.3", connectionstyle="arc3", lw=3))
    # ax2[1].set_xlabel("Stall Time Change (\%)", fontsize=fontsize, x=-0.05)
    # ax2[0].set_ylabel("Average Quality Change (\%)", fontsize=fontsize) # , loc='top'
    # ax2[0].set_ylim(-15.0, 51.0)
    # ax2[0].set_yticks(np.arange(-10.0, 55.0, 20.0))
    # # ax2[0].tick_params(labelsize=fontsize_label)
    # ax2[0].yaxis.set_major_formatter(mtick.PercentFormatter())
    # ax2[0].set_xlim(0.1,-0.095)
    # # ax2[0].set_xticks(np.arange(0.1, -0.1, -0.1), fontsize=fontsize_label)
    # # ax2[0].set_xticks(np.arange(0.1, -0.1, -0.1))
    # ax2[0].xaxis.set_major_formatter(mtick.PercentFormatter(decimals=2))
    # ax2[1].set_xlim(0.6,-1.1)
    # # ax2[1].set_xticks(np.arange(0.7, -1.0, -0.5), fontsize=fontsize_label)
    # # ax2[1].set_xticks(np.arange(0.7, -1.0, -0.5))
    # ax2[1].xaxis.set_major_formatter(mtick.PercentFormatter(decimals=2))
    # ax2[0].set_title('(c) Volumetric Video QoE',x=1.0,y=-0.4,fontsize=fontsize)
    # ax2[0].grid(linestyle='--')
    # ax2[1].grid(linestyle='--')
    # ax2[0].tick_params(axis='both', which='major', labelsize=fontsize_label)
    # ax2[1].tick_params(axis='both', which='major', labelsize=fontsize_label)
    # plt.subplots_adjust(wspace=0.05)
    # plt.gca().invert_xaxis()
    # plt.legend()
    # fig.tight_layout()

    ### Plot 16K VOD ###
    ax0[0].set_xlim(1.5, -0.1)
    ax0[0].set_xticks(np.arange(1.5, 0.0, -0.5))
    ax0[0].xaxis.set_major_formatter(mtick.PercentFormatter())
    ax0[0].set_ylim(0.63, 1.05)
    ax0[0].set_yticks([0.75, 1.00])
    ax0[1].set_ylim(0.51, 1.0)
    ax0[1].set_yticks([0.75, 1.00])
    ax0[2].set_ylim(0.2, 0.7)
    ax0[2].set_yticks([0.25, 0.50])
    fontsize = 22
    fontsize_label = 20
    ax0[2].annotate("Better QoE", fontsize=fontsize, horizontalalignment="center", xy=(1.02, 0.48), xycoords='data',
                    xytext=(1.27, 0.25), textcoords='data', arrowprops=dict(arrowstyle="->, head_width=0.3", connectionstyle="arc3", lw=3))

    map_scheme_ax = {'RBHO': 2, 'robustMPCGT': 1, 'RB': 2, 'robustMPC': 1, 'robustMPCHO': 1, 'fastMPC': 0, 'fastMPCHO': 0,
            'fastMPCGT': 0, 'RBHOGT':2}
    for scheme in schemes:
        selected_ax = map_scheme_ax[scheme]
        line = ax0[selected_ax].errorbar(data_vod[scheme][0], data_vod[scheme][1], xerr=data_vod[scheme][2], yerr=data_vod[scheme][3], capsize=3, color=colormap[scheme])
        if 'GT' in scheme:
            line[-1][0].set_linestyle('-.')
            line[-1][1].set_linestyle('-.')
            ax0[selected_ax].scatter(data_vod[scheme][0], data_vod[scheme][1], marker='x', color=colormap[scheme])
        elif 'HO' in scheme:
            ax0[selected_ax].scatter(data_vod[scheme][0], data_vod[scheme][1], marker='^', color=colormap[scheme])
        else:
            line[-1][0].set_linestyle('--')
            line[-1][1].set_linestyle('--')
            ax0[selected_ax].scatter(data_vod[scheme][0], data_vod[scheme][1], color=colormap[scheme])
        if scheme == 'robustMPC':           
            ax0[1].annotate("robustMPC", (data_vod[scheme][0]+0.5, data_vod[scheme][1]-0.11), fontsize=fontsize_label, color=colormap[scheme])
        elif scheme == 'fastMPC':            
            ax0[0].annotate("fastMPC", (data_vod[scheme][0]+0.35, data_vod[scheme][1]+0.04), fontsize=fontsize_label, color=colormap[scheme])
        elif scheme == 'FESTIVE':           
            ax0[0].annotate("FESTIVE", (data_vod[scheme][0]+0.35, data_vod[scheme][1]-0.15), fontsize=fontsize_label, color=colormap[scheme])
        elif scheme == 'robustMPCGT':
            ax0[1].annotate("robustMPC-GT", (data_vod[scheme][0]+0.2, data_vod[scheme][1]+0.12), fontsize=fontsize_label, color=colormap[scheme])
            # ax0[1].annotate('robustMPC-GT', color=colormap[scheme], fontsize=fontsize_label, horizontalalignment="center", xy=(data_vod[scheme][0], data_vod[scheme][1]), xycoords='data',
            #         xytext=(data_vod[scheme][0], data_vod[scheme][1] - 0.65), textcoords='data', arrowprops=dict(arrowstyle="<|-, head_width=0.15, head_length=0.15", connectionstyle="arc3,rad=-0.3", lw=1, color=colormap[scheme], linestyle = '--'))
        elif scheme == 'fastMPCGT':
            ax0[0].annotate("fastMPC-GT", (data_vod[scheme][0]+0.2, data_vod[scheme][1]+0.09), fontsize=fontsize_label, color=colormap[scheme], weight='bold')
        elif scheme == 'robustMPCHO':
            ax0[1].annotate("$\\textit{%s}$" % "robustMPC-PR", (data_vod[scheme][0]+0.08, data_vod[scheme][1]-0.2), fontsize=fontsize_label, color=colormap[scheme])
        elif scheme == 'fastMPCHO':
            # ax0[0].annotate("$\\textit{%s}$" % 'fastMPC-PR', color=colormap[scheme], fontsize=fontsize_label, horizontalalignment="center", xy=(data_vod[scheme][0], data_vod[scheme][1]), xycoords='data',
            #         xytext=(data_vod[scheme][0]+0.8, data_vod[scheme][1] + 0.18), textcoords='data', arrowprops=dict(arrowstyle="<|-, head_width=0.15, head_length=0.15", connectionstyle="arc3,rad=-0.3", lw=1, color=colormap[scheme], linestyle = '--'))
            ax0[0].annotate("$\\textit{%s}$" % "fastMPC-PR", (data_vod[scheme][0]+0.2, data_vod[scheme][1]-0.18), fontsize=fontsize_label, color=colormap[scheme], weight='bold')
        elif scheme == 'RBHO':
            ax0[2].annotate("$\\textit{%s}$" % "RB-PR", (data_vod[scheme][0]+0.27, data_vod[scheme][1]-0.2), fontsize=fontsize_label, color=colormap[scheme])
        elif scheme == 'RB':
            ax0[2].annotate("RB", (data_vod[scheme][0]+0.2, data_vod[scheme][1]+0.01), fontsize=fontsize_label, color=colormap[scheme])
        elif scheme == 'BOLA':
            ax0[0].annotate("BOLA", (data_vod[scheme][0]-0.05, data_vod[scheme][1]-0.12), fontsize=fontsize_label, color=colormap[scheme])
        elif scheme == 'RBHOGT':
            ax0[2].annotate("RB-GT", (data_vod[scheme][0]-0.05, data_vod[scheme][1]-0.12), fontsize=fontsize_label, color=colormap[scheme])
        else:          
            ax0[0].annotate(scheme, (data_vod[scheme][0]-0.02, data_vod[scheme][1]+0.01), fontsize=fontsize_label, color=colormap[scheme])    
    ax0[2].set_xlabel('Time Spent on Stall (\%)', fontsize=fontsize)
    ax0[1].set_ylabel('Normalized Bitrate', fontsize=fontsize)
    ax0[0].grid(linestyle='--')
    ax0[1].grid(linestyle='--')
    ax0[2].grid(linestyle='--')
    ax0[0].tick_params(axis='both', which='major', labelsize=fontsize_label)
    ax0[1].tick_params(axis='both', which='major', labelsize=fontsize_label)
    ax0[0].tick_params(axis='x', which='major', bottom=False)
    ax0[1].tick_params(axis='x', which='major', bottom=False)
    ax0[2].tick_params(axis='both', which='major', labelsize=fontsize_label)
    # subfigs.flat[0].suptitle('(a) 16K panormaic VoD QoE', y = 0.0, fontsize=22)
    ax0[2].set_title('(a) 16K panormaic VoD QoE',y=-1.3,fontsize=22)
    # ax0.text(0.5, 0.01, '(a) 16k VoD QoE', wrap=True, horizontalalignment='center', fontsize=20)

    ### plot throughput prediction ###
    # ax1.bar([0], [data_vod_pred['w/o HO\n(fastMPC)'][0]], 0.35, color='none', edgecolor='darkred', ecolor='darkred', hatch='/', linewidth=2, 
    #             yerr=data_vod_pred['w/o HO\n(fastMPC)'][1], error_kw=dict(lw=2.5, capsize=5, capthick=2))
    # ax1.bar([0.5], [data_vod_pred['w/ HO\n(fastMPC)'][0]], 0.35, color='none', edgecolor='darkblue', ecolor='darkblue', hatch='o', linewidth=2, 
    #             yerr=data_vod_pred['w/ HO\n(fastMPC)'][1], error_kw=dict(lw=2.5, capsize=5, capthick=2))
    # ax1.bar([1], [data_vod_pred['w/ HO\n(fastMPC-PR)'][0]], 0.35, color='none', edgecolor='darkgreen', ecolor='darkgreen', hatch='x', linewidth=2, 
    #             yerr=data_vod_pred['w/ HO\n(fastMPC-PR)'][1], error_kw=dict(lw=2.5, capsize=5, capthick=2))
    hd1 = ax1.bar([0], [data_vod_pred['w/o HO\n(fastMPC)'][0]], 0.35, color='none', edgecolor='darkred', ecolor='darkred', hatch='/', linewidth=2, 
                yerr=data_vod_pred['w/o HO\n(fastMPC)'][1], error_kw=dict(lw=2.5, capsize=5, capthick=2), label='fastMPC')
    hd2 = ax1.bar([0.5], [data_vod_pred['w/ HO\n(fastMPC)'][0]], 0.35, color='none', edgecolor='darkred', ecolor='darkred', hatch='/', linewidth=2, 
                yerr=data_vod_pred['w/ HO\n(fastMPC)'][1], error_kw=dict(lw=2.5, capsize=5, capthick=2), label='fastMPC')
    hd3 = ax1.bar([1], [data_vod_pred['w/o HO\n(fastMPC-PR)'][0]], 0.35, color='none', edgecolor='darkgreen', ecolor='darkgreen', hatch='x', linewidth=2, 
                yerr=data_vod_pred['w/o HO\n(fastMPC-PR)'][1], error_kw=dict(lw=2.5, capsize=5, capthick=2), label='fastMPC-PR')
    hd4 = ax1.bar([1.5], [data_vod_pred['w/ HO\n(fastMPC-PR)'][0]], 0.35, color='none', edgecolor='darkgreen', ecolor='darkgreen', hatch='x', linewidth=2, 
                yerr=data_vod_pred['w/ HO\n(fastMPC-PR)'][1], error_kw=dict(lw=2.5, capsize=5, capthick=2), label='fastMPC-PR')
    ax1.set_ylabel('Mean Average Error (Mbps)', fontsize=fontsize)
    ax1.tick_params(axis='both', which='major', labelsize=fontsize)
    ax1.set_xticks([0, 0.5, 1, 1.5])
    ax1.set_xticklabels(['w/o \nHO', 'w/ \nHO', 'w/o \nHO', 'w/ \nHO'], fontsize=22)
    ax1.grid(linestyle='--', axis='y')
    ax1.set_title('(b) 16K VoD Tput. prediction',y=-0.4,fontsize=22)
    # subfigs.flat[1].suptitle('(b) 16K VoD Tput. prediction', y=0.0,fontsize=22)
    ax1.legend(handles=[hd1, hd3], loc='upper right', fontsize=24, borderpad=0.0, handlelength=1.2, edgecolor='white', borderaxespad=0.1, labelspacing=0.1,
                columnspacing=1.0, handletextpad=0.1, bbox_to_anchor=(1.00, 0.99))
    # ax1.text(0.5, 0.01, '(a) Thrpt Prediction', wrap=True, horizontalalignment='center', fontsize=20)

    # fig.tight_layout()

    plot_handler(plt, plot_name, plot_id, plot_dir, show_flag=SHOW_PLOT_FLAG, pad_inches=0.07)

print('Complete./')