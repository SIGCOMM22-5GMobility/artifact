#!/usr/bin/env python3
import os
import pandas as pd
from os import path

from utils.context import data_processed_dir
from utils.utils import remove_nan_object
from common import Environment

############### Config ####################
DEBUG = False
DATA_FOLDER = path.join(data_processed_dir, 'table3-system_evaluation')
DATA_PROCESSED_FOLDER = path.join(DATA_FOLDER, 'logs')
os.makedirs(DATA_PROCESSED_FOLDER, exist_ok=True)
FILENAME_D1 = 'D1'
FILENAME_D2 = 'D2'

## load and prepare data
# D1
d1_lte_df = pd.read_csv(path.join(DATA_FOLDER, FILENAME_D1 + '-lte-mr.csv'), low_memory=False, header=None)
d1_5g_df = pd.read_csv(path.join(DATA_FOLDER, FILENAME_D1 + '-nr-mr.csv'), low_memory=False, header=None)
d1_lte_sequence_list = d1_lte_df.to_numpy()
d1_5g_sequence_list = d1_5g_df.to_numpy()
d1_lte_sequence_list = [remove_nan_object(seq) for seq in d1_lte_sequence_list]
d1_5g_sequence_list = [remove_nan_object(seq) for seq in d1_5g_sequence_list]
# D2
d2_lte_df = pd.read_csv(path.join(DATA_FOLDER, FILENAME_D2 + '-lte-mr.csv'), low_memory=False, header=None)
d2_5g_df = pd.read_csv(path.join(DATA_FOLDER, FILENAME_D2 + '-nr-mr.csv'), low_memory=False, header=None)
d2_lte_sequence_list = d2_lte_df.to_numpy()
d2_5g_sequence_list = d2_5g_df.to_numpy()
d2_lte_sequence_list = [remove_nan_object(seq) for seq in d2_lte_sequence_list]
d2_5g_sequence_list = [remove_nan_object(seq) for seq in d2_5g_sequence_list]

## run experiments and generate results
# D1
print("\t\t\t\t########## D1 Dataset #########")
d1_lte_env = Environment(debug=DEBUG, log_path=path.join(DATA_PROCESSED_FOLDER, f'{FILENAME_D1}'))
print("HOs on 4G Radio Interface ==> ", end="")
d1_lte_env.run_lte(d1_lte_sequence_list)
d1_5g_env = Environment(debug=DEBUG, log_path=path.join(DATA_PROCESSED_FOLDER, f'{FILENAME_D1}'))
print("HOs on 5G Radio Interface ==> ", end="")
d1_5g_env.run_nsa(d1_5g_sequence_list)
# D2
print("\n\t\t\t\t########## D2 Dataset #########")
d2_lte_env = Environment(debug=DEBUG, log_path=path.join(DATA_PROCESSED_FOLDER, f'{FILENAME_D2}'))
print("HOs on 4G Radio Interface ==> ", end="")
d2_lte_env.run_lte(d2_lte_sequence_list)
d2_5g_env = Environment(debug=DEBUG, log_path=path.join(DATA_PROCESSED_FOLDER, f'{FILENAME_D2}'))
print("HOs on 5G Radio Interface ==> ", end="")
d2_5g_env.run_nsa(d2_5g_sequence_list)

print("\n* detailed logs are saved to data/table3-system_evaluation/logs ...")
