# -*-coding:utf-8 -*-
# Author: Eileen Kammel, 811770
# Date: 2025-02-10 14:32:00

import os
import pandas as pd
from make_info_table import load_ground_truth, load_human_expressions, load_model_expressions
COMMERCIAL_MODELS = [
    "gpt-4o-2024-08-06",
    "claude-3-5-sonnet-20240620",
    "gemini-2.0-flash-exp",
]

OPEN_WEIGHED_MODELS = [
    "idefics-80b-instruct",
    "InternVL2-Llama3-76B",
    "InternVL2-40B",
    "InternVL2-8B",
]

HUMAN_MOCK = ["programmatic"]

ALL_MODELS = COMMERCIAL_MODELS + OPEN_WEIGHED_MODELS

TUNA_STIMULI_IDS = [
    642,
    580,
    965,
    454,
    9,
    588,
    975,
    719,
    784,
    593,
    977,
    55,
    1047,
    793,
    220,
    799,
    96,
    675,
    932,
    101,
    678,
    1060,
    164,
    878,
    307,
    244,
    501,
    567,
    123,
    127,
]  # List of stimuli ids for TUNA
THREEDS_STIMULI_IDS = [
    640,
    1856,
    453,
    2693,
    3014,
    3589,
    2761,
    1224,
    654,
    1559,
    3160,
    3544,
    3991,
    802,
    3367,
    1129,
    491,
    684,
    1389,
    686,
    2671,
    3762,
    3123,
    2482,
    2418,
    2999,
    3512,
    2682,
    1403,
    1276,
]


def make_expression_overview():
    columns = ["set", "stim_id", "GT", "HE", "gpt-4o", "claude-3-5", "gemini-2.0", "idefics-80b", "InternVL2-Llama3", "InternVL2-40B", "InternVL2-8B"]
    overview = pd.DataFrame(columns=columns)
    for id in TUNA_STIMULI_IDS:
        row = []
        row.append("TUNA")
        row.append(id)
        row.append(GT[id])