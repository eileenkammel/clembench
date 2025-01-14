# -*-coding:utf-8 -*-
# Author: Eileen Kammel, 811770
# Date: 2025-01-14 16:57:21

import pandas as pd
import numpy as np
import os

# Load data
header = ["stimuli_id", "target", "D1", "D2", "D3", "id_type", "minimal_expression", "ground_truth", "human_expression", "model_expressions"]


def load_raw_stimuli_info(stimuli_id):
    """ Will return t, D1-D3, id_type, (minimal expression)"""
    pass

def load_ground_truth(t):
    """ Will return ground_truth """
    pass

def load_human_expression(stimuli_id):
    """ Will return human_expression """
    pass

def load_model_expressions(stimuli_id):
    """ Will return model_expressions """
    pass

def write_info_table():
    tuna_ids = []
    three_ds_ids = []
    tuna_data = pd.DataFrame(columns=header)
    three_ds_data = pd.DataFrame(columns=header)
    for id in tuna_ids:
        t, D1, D2, D3, id_type, minimal_expression = load_raw_stimuli_info(id)
        ground_truth = load_ground_truth(t)
        human_expression = load_human_expression(id)
        model_expressions = load_model_expressions(id)
        tuna_data.loc[len(tuna_data)] = [id, t, D1, D2, D3, id_type, minimal_expression, ground_truth, human_expression, model_expressions]
    for id in three_ds_ids:
        t, D1, D2, D3, id_type, minimal_expression = load_raw_stimuli_info(id)
        ground_truth = load_ground_truth(t)
        human_expression = load_human_expression(id)
        model_expressions = load_model_expressions(id)
        three_ds_data.loc[len(three_ds_data)] = [id, t, D1, D2, D3, id_type, minimal_expression, ground_truth, human_expression, model_expressions]
    complete_data = pd.concat([tuna_data, three_ds_data])

    tuna_data.to_csv("tuna_info_table.csv", index=False)
    three_ds_data.to_csv("three_ds_info_table.csv", index=False)
    complete_data.to_csv("info_table.csv", index=False)
