# -*-coding:utf-8 -*-
# Author: Eileen Kammel, 811770
# Date: 2025-02-24 17:48:34

# Check if model have location bias
# in comprehension/orogrammatic mode

import json
import pandas as pd

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

ALL_IDS = TUNA_STIMULI_IDS + THREEDS_STIMULI_IDS


def check_loc_bias(data, models, output_path):
    out_df = pd.DataFrame(columns=["model", "stim_id", "loc bias"])
    df = pd.read_csv(data)
    df = df[df["status"] == "completed"]
    for model in models:
        model_df = df[df["model"] == model]
        for stim_id in ALL_IDS:
            episodes = model_df[model_df["stim_id"] == stim_id]
            loc_bias = compare_episodes(episodes)
            out_df.loc[len(out_df)] = [model, stim_id, loc_bias]
    out_df.to_csv(output_path, index=False)


def compare_episodes(episodes):
    choices = episodes["P2_choice"]
    unique_choices = len(choices.unique())
    if unique_choices == 4:
        return False
    elif unique_choices == 1:
        return True
    else:
        return compare_choices(choices)


def compare_choices(choices):
    unique_choices = list(choices.unique())
    if len(unique_choices) == 2:

        choice_one = list(choices).count(unique_choices[0])
        choice_two = list(choices).count(unique_choices[1])
        if choice_one == 3 or choice_two == 3:
            return True
        else:
            return False
    else:
        return False


def count_loc_bias(models, data):
    for model in models:
        model_df = data[data["model"] == model]
        loc_bias = model_df["loc bias"].value_counts()
        print(model)
        print(loc_bias)



if __name__ == "__main__":
    check_loc_bias(
        "games/multimodal_referencegame/analysis/commercial_expressions_by_model_programmatic.csv",
        COMMERCIAL_MODELS,
        "games/multimodal_referencegame/analysis/commercial_loc_bias.csv",
    )
    check_loc_bias(
        "games/multimodal_referencegame/analysis/expressions_by_model_programmatic.csv",
        OPEN_WEIGHED_MODELS,
        "games/multimodal_referencegame/analysis/open_loc_bias.csv",
    )

    commercial_loc_bias = pd.read_csv("games/multimodal_referencegame/analysis/commercial_loc_bias.csv")
    open_loc_bias = pd.read_csv("games/multimodal_referencegame/analysis/open_loc_bias.csv")
    count_loc_bias(COMMERCIAL_MODELS, commercial_loc_bias)
    count_loc_bias(OPEN_WEIGHED_MODELS, open_loc_bias)
