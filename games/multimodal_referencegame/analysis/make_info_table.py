# -*-coding:utf-8 -*-
# Author: Eileen Kammel, 811770
# Date: 2025-01-14 16:57:21

import pandas as pd
import json


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
]  # List of stimuli ids for 3DS

# Load data
header = [
    "stimuli_id",
    "target",
    "D1",
    "D2",
    "D3",
    "id_type",
    "minimal_expression",
    "ground_truth",
    "human_expression",
    "model_expressions",
]


def load_raw_stimuli_info(data_set_name, stimuli_id):
    """Will return t, D1-D3, id_type, (minimal expression)"""
    if data_set_name == "tuna":
        with open("games/multimodal_referencegame/prep/tuna/tuna_3_distractor_stimuli.json", "r") as f:
            data = json.load(f)
            all_stimuli = data["INSTANCES"]["one_attibute_id"] + data["INSTANCES"]["two_attibute_id"] + data["INSTANCES"]["three_attibute_id"]
            for stimuli in all_stimuli:
                if stimuli["stimuli_id"] == stimuli_id:
                    return (
                        stimuli["target"],
                        stimuli["distractor1"],
                        stimuli["distractor2"],
                        stimuli["distractor3"],
                        stimuli["id_type"],
                        stimuli["id_attributes"],
                    )
    if data_set_name == "3ds":
        with open("games/multimodal_referencegame/prep/3DS/3ds_3_distractor_instances.json", "r") as f:
            data = json.load(f)
            all_stimuli = data["INSTANCES"]["one_attibute_id"] + data["INSTANCES"]["two_attibute_id"] + data["INSTANCES"]["three_attibute_id"]
            for stimuli in all_stimuli:
                if stimuli["stimuli_id"] == stimuli_id:
                    return (
                        stimuli["target"],
                        stimuli["distractor1"],
                        stimuli["distractor2"],
                        stimuli["distractor3"],
                        stimuli["id_type"],
                        stimuli["id_attributes"],
                    )


def load_ground_truth(t):
    """Will return ground_truth"""
    return None


def load_human_expression(experiment_name, stimuli_id):
    """Will return all human expressions from slurk_logs for a given stimuli_id.
    Different expressions will be separated by a $.
    """
    with open("games/multimodal_referencegame/analysis/successful_human_expressions.json", "r") as f:
        all_human_expressions = json.load(f)
    expressions = ""
    if experiment_name == "tuna":
        for game in all_human_expressions["tuna"]:
            if game["stimuli_id"] == stimuli_id:
                expressions += "$" + game["human_expression"]
        for game in all_human_expressions["mixed"]:
            if game["stimuli_id"] == stimuli_id:
                expressions += "$" + game["human_expression"]
    if experiment_name == "3ds":
        for game in all_human_expressions["3ds"]:
            if game["stimuli_id"] == stimuli_id:
                expressions += "$" + game["human_expression"]
        for game in all_human_expressions["mixed"]:
            if game["stimuli_id"] == stimuli_id:
                expressions += "$" + game["human_expression"]
    return expressions.strip("$")


def load_model_expressions(stimuli_id):
    """Will return model_expressions"""
    return None


def write_info_table():
    tuna_data = pd.DataFrame(columns=header)
    three_ds_data = pd.DataFrame(columns=header)
    for id in TUNA_STIMULI_IDS:
        t, D1, D2, D3, id_type, minimal_expression = load_raw_stimuli_info("tuna", id)
        ground_truth = load_ground_truth(t)
        human_expression = load_human_expression("tuna", id)
        model_expressions = load_model_expressions(id)
        tuna_data.loc[len(tuna_data)] = [
            id,
            t,
            D1,
            D2,
            D3,
            id_type,
            minimal_expression,
            ground_truth,
            human_expression,
            model_expressions,
        ]
    for id in THREEDS_STIMULI_IDS:
        t, D1, D2, D3, id_type, minimal_expression = load_raw_stimuli_info("3ds", id)
        ground_truth = load_ground_truth(t)
        human_expression = load_human_expression("3ds", id)
        model_expressions = load_model_expressions(id)
        three_ds_data.loc[len(three_ds_data)] = [
            id,
            t,
            D1,
            D2,
            D3,
            id_type,
            minimal_expression,
            ground_truth,
            human_expression,
            model_expressions,
        ]
    complete_data = pd.concat([tuna_data, three_ds_data])

    tuna_data.to_csv("games/multimodal_referencegame/analysis/tuna_info_table.csv", index=False)
    three_ds_data.to_csv("games/multimodal_referencegame/analysis/three_ds_info_table.csv", index=False)
    complete_data.to_csv("games/multimodal_referencegame/analysis/info_table.csv", index=False)

if __name__ == "__main__":
    write_info_table()
