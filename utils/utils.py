import matplotlib.pyplot as plt
import os
import numpy as np
import mpu
from math import pi, log, tan

import pandas as pd

ZOOM0_SIZE = 512

# get colors
cmap10 = plt.cm.tab10
colorlist10 = [cmap10(i) for i in range(cmap10.N)]

cmap20 = plt.cm.tab20
colorlist20 = [cmap20(i) for i in range(cmap20.N)]

cmap20c = plt.cm.tab20c
colorlist20c = [cmap20c(i) for i in range(cmap20c.N)]

pastel1 = plt.cm.Pastel1
pastel1list = [pastel1(i) for i in range(pastel1.N)]

pastel2 = plt.cm.Pastel1
pastel2list = [pastel2(i) for i in range(pastel2.N)]

paired = plt.cm.Paired
pairedlist = [paired(i) for i in range(paired.N)]

set210 = plt.cm.Set2
colorlistset2 = [set210(i) for i in range(set210.N)]

# color indices for colorlist20
lte_c_idx = 0
nsa_c_idx = 2
sa_c_idx = 4
low_band_c_idx = 6
mid_band_c_idx = 8
high_band_c_idx = 10

# hex list
hex_col_list = ['#4078c0', '#6cc644', '#bd2c00', '#c9510c', '#6e5494', '#ffff00', '#87005f']


def remove_nan(arr):
    return arr[~np.isnan(arr)]


def remove_nan_object(arr):
    return arr[~pd.isnull(arr)]


def get_cdf(arr, is_object=False):
    if is_object:
        arr = remove_nan_object(arr)
    else:
        arr = remove_nan(arr)
    arr_x = np.sort(arr)
    arr_y = 1. * np.arange(len(arr)) / (len(arr) - 1)
    return arr_x, arr_y


def remove_outliers(arr, max_deviations=3):
    mean = np.mean(arr)
    standard_deviation = np.std(arr)
    distance_from_mean = abs(arr - mean)
    not_outlier = distance_from_mean < max_deviations * standard_deviation
    no_outliers = arr[not_outlier]
    return no_outliers


def get_std(arr, max_deviations=3):
    return np.std(remove_outliers(arr, max_deviations))


def plot_handler(plt_, plot_id, plot_name, plot_path='plots', show_flag=True, ignore_eps=True, pad_inches=0):
    if show_flag:
        print('Showing Plot {}-{}'.format(plot_id, plot_name))
        plt_.show(bbox_inches='tight')
    else:
        ax = plt_.gca()
        os.makedirs(os.path.join(plot_path, 'png'), exist_ok=True)
        os.makedirs(os.path.join(plot_path, 'pdf'), exist_ok=True)

        plt_.savefig(os.path.join(plot_path, 'png', f'{plot_id}-{plot_name}.png'), format='png', dpi=300,
                     bbox_inches='tight', pad_inches=pad_inches)
        plt_.savefig(os.path.join(plot_path, 'pdf', f'{plot_id}-{plot_name}.pdf'), format='pdf', dpi=300,
                     bbox_inches='tight', pad_inches=pad_inches)
        if not ignore_eps:
            # Save it with rasterized points
            ax.set_rasterization_zorder(1)
            os.makedirs(os.path.join(plot_path, 'eps'), exist_ok=True)
            plt_.savefig(os.path.join(plot_path, 'eps', f'{plot_id}-{plot_name}.eps'), dpi=300, rasterized=True,
                         bbox_inches='tight', pad_inches=0)
        print('Saved Plot {}-{}'.format(plot_name, plot_id))


def get_geo_distance(lat1, lon1, lat2, lon2):
    return mpu.haversine_distance((lat1, lon1), (lat2, lon2))


def g2p_string(lat, lon, zoom):
    loc_str = str(ZOOM0_SIZE * (2 ** zoom) * (1 + lon / 180) / 2)[:3] + \
              str(ZOOM0_SIZE / (2 * pi) * (2 ** zoom) * (pi - log(tan(pi / 4 * (1 + lat / 90)))))[:3]
    return loc_str
