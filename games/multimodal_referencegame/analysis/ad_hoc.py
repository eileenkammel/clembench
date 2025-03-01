# -*-coding:utf-8 -*-
# Author: Eileen Kammel, 811770
# Date: 2025-02-26 17:55:01

import pandas as pd
import json
from games.multimodal_referencegame.analysis.constants import (
    COMMERCIAL_MODELS,
    OPEN_WEIGHED_MODELS,
    ALL_MODELS,
    COMMERCIAL_MODELS_ALIAS,
    OPEN_WEIGHED_MODELS_ALIAS,
    ALL_MODELS_ALIAS,
    TUNA_STIMULI_IDS,
    THREEDS_STIMULI_IDS,
    ALL_IDS,
)


human_commercial = pd.read_csv(
    "games/multimodal_referencegame/analysis/commercial_expressions_by_model_programmatic.csv"
)
human_ow = pd.read_csv(
    "games/multimodal_referencegame/analysis/expressions_by_model_programmatic.csv"
)
df_commercial = pd.read_csv("games/multimodal_referencegame/analysis/commercial_expressions_by_model.csv")
df_ow = pd.read_csv("games/multimodal_referencegame/analysis/expressions_by_model.csv")

# for each model and for each setting, compute percentage of games completed

def compute_completion_rate(df):
    completion_rate = {}
    for model in ALL_MODELS:
        model_df = df[df["model"] == model]
        completion_rate[model] = round((len(model_df[model_df["status"] == "completed"]) / len(model_df)) *100, 2)
    return pretty_print_dict(completion_rate)


# for each model count if abort at player 1 or player 2
def count_abort(data):
    for model in ALL_MODELS:
        model_df = data[data["model"] == model]
        abort = (model_df["status"].value_counts()).to_dict()
        print(model)
        print(pretty_print_dict(abort))

# for each model find out if difference in aborted rate
# for TUNA vs 3DS


def compare_abort_rate(data):
    for model in ALL_MODELS:
        model_df = data[data["model"] == model]
        tuna = model_df[model_df["set"] == "TUNA"]
        threeds = model_df[model_df["set"] == "3DS"]
        tuna_abort = (tuna["status"].value_counts()).to_dict()
        threeds_abort = (threeds["status"].value_counts()).to_dict()
        print(model)
        print("TUNA")
        print(pretty_print_dict(tuna_abort))
        print("3DS")
        print(pretty_print_dict(threeds_abort))

# find out it models answer determinisitcally
# as player 1, i.e. same stimuli, same description


def check_deterministic(data):
    deterministc = {model: {"deterministic": 0, "non-deterministic": 0} for model in ALL_MODELS}
    for model in ALL_MODELS:
        model_df = data[data["model"] == model]
        for stim_id in ALL_IDS:
            episodes = model_df[model_df["stim_id"] == stim_id]
            descriptions = episodes["expression"]
            unique_descriptions = len(descriptions.unique())
            if unique_descriptions == 1:
                deterministc[model]["deterministic"] += 1
            else:
                deterministc[model]["non-deterministic"] += 1
    print(pretty_print_dict(deterministc))


def pretty_print_dict(data):
    pretty_dict = ""
    for key, value in data.items():
        pretty_dict += f"{key}: {value}\n"
    return pretty_dict

print("COMPLETION RATE")
print("Production")
print(compute_completion_rate(pd.concat([df_commercial, df_ow])))
print("Comprehension")
print(compute_completion_rate(pd.concat([human_commercial, human_ow])))
print("\n --------------------------------- \n")
print("ABORT RATE")
print("Production")
count_abort(pd.concat([df_commercial, df_ow]))
print("Comprehension")
count_abort(pd.concat([human_commercial, human_ow]))
print("\n --------------------------------- \n")
print("ABORT RATE SET")
print("Production")
compare_abort_rate(pd.concat([df_commercial, df_ow]))
print("Comprehension")
compare_abort_rate(pd.concat([human_commercial, human_ow]))
print("\n --------------------------------- \n")
print("DETERMINISTIC")
print("Production")
check_deterministic(pd.concat([df_commercial, df_ow]))
