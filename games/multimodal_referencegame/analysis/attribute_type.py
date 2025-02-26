# -*-coding:utf-8 -*-
# Author: Eileen Kammel, 811770
# Date: 2025-02-25 20:24:56

# Determine if some attributes make id harder.
# For each model, calculate the ratio of correct answers for each attribute.
# Save the results in a csv file.

import json
import pandas as pd
from games.multimodal_referencegame.analysis.constants import (
    ALL_MODELS,
    TUNA_STIMULI_IDS,
    THREEDS_STIMULI_IDS,
)

TUNA_ATTRIBUTES = ["colour", "type", "size", "orientation"]

THREEDS_ATTRIBUTES = [
    "shape",
    "scale",
    "floorHue",
    "wallHue",
    "objectHue",
    "orientation",
]


attribute_episodes = {
    "tuna": {"colour": [], "type": [], "size": [], "orientation": []},
    "threeds": {
        "shape": [],
        "scale": [],
        "floorHue": [],
        "wallHue": [],
        "objectHue": [],
        "orientation": [],
    },
}

tuna_stimuli = json.load(
    open("games/multimodal_referencegame/prep/tuna/tuna_3_distractor_stimuli.json")
)
tuna_stimuli = (
    tuna_stimuli["INSTANCES"]["one_attibute_id"]
    + tuna_stimuli["INSTANCES"]["two_attibute_id"]
    + tuna_stimuli["INSTANCES"]["three_attibute_id"]
)

for attribute in TUNA_ATTRIBUTES:
    for stim in tuna_stimuli:
        if attribute in stim["id_type"]:
            if stim["stimuli_id"] in TUNA_STIMULI_IDS:
                attribute_episodes["tuna"][attribute].append(stim["stimuli_id"])

threeds_stimuli = json.load(
    open("games/multimodal_referencegame/prep/3DS/3ds_3_distractor_instances.json")
)
threeds_stimuli = (
    threeds_stimuli["INSTANCES"]["one_attibute_id"]
    + threeds_stimuli["INSTANCES"]["two_attibute_id"]
    + threeds_stimuli["INSTANCES"]["three_attibute_id"]
)

for attribute in THREEDS_ATTRIBUTES:
    for stim in threeds_stimuli:
        if attribute in stim["id_type"]:
            if stim["stimuli_id"] in THREEDS_STIMULI_IDS:
                attribute_episodes["threeds"][attribute].append(stim["stimuli_id"])

print(attribute_episodes)

expressions_commercial = pd.read_csv(
    "games/multimodal_referencegame/analysis/commercial_expressions_by_model.csv"
)
expressions_commercial = expressions_commercial[
    expressions_commercial["status"] == "completed"
]

expressions_ow = pd.read_csv(
    "games/multimodal_referencegame/analysis/expressions_by_model.csv"
)
expressions_ow = expressions_ow[expressions_ow["status"] == "completed"]

expressions_all_models = pd.concat([expressions_commercial, expressions_ow])

tuna_attribute_influence = dict()
three_ds_attribute_influence = dict()

for model in ALL_MODELS:
    model_df = expressions_all_models[expressions_all_models["model"] == model]
    tuna_attribute_influence[model] = {}
    three_ds_attribute_influence[model] = {}
    for attribute, episodes in attribute_episodes["tuna"].items():
        attribute_df = model_df[model_df["stim_id"].isin(episodes)]
        correct = attribute_df["correct"].value_counts().to_dict()
        tuna_attribute_influence[model][attribute] = correct
    for attribute, episodes in attribute_episodes["threeds"].items():
        attribute_df = model_df[model_df["stim_id"].isin(episodes)]
        correct = attribute_df["correct"].value_counts().to_dict()
        three_ds_attribute_influence[model][attribute] = correct

tuna_correct_ratio = dict()
three_ds_correct_ratio = dict()

for model, attributes in tuna_attribute_influence.items():
    tuna_correct_ratio[model] = {}
    for attribute, correct in attributes.items():
        true_count = correct[True] if True in correct else 0
        false_count = correct[False] if False in correct else 0
        total = true_count + false_count
        if total == 0:
            continue
        tuna_correct_ratio[model][attribute] = round((true_count / total) * 100, 2)
for model, attributes in three_ds_attribute_influence.items():
    three_ds_correct_ratio[model] = {}
    for attribute, correct in attributes.items():
        true_count = correct[True] if True in correct else 0
        false_count = correct[False] if False in correct else 0
        total = true_count + false_count
        if total == 0:
            continue
        three_ds_correct_ratio[model][attribute] = round((true_count / total) * 100, 2)

print(tuna_attribute_influence)
print(tuna_correct_ratio)
print(three_ds_attribute_influence)
print(three_ds_correct_ratio)


tuna_df = pd.DataFrame(tuna_correct_ratio)
tuna_df = tuna_df.reset_index()
tuna_df = tuna_df.rename(columns={"index": "attribute"})
tuna_df["attribute_type"] = "tuna"


three_ds_df = pd.DataFrame(three_ds_correct_ratio)
three_ds_df = three_ds_df.reset_index()
three_ds_df = three_ds_df.rename(columns={"index": "attribute"})
three_ds_df["attribute_type"] = "three_ds"

combined_df = pd.concat([tuna_df, three_ds_df])


combined_df = combined_df.melt(
    id_vars=["attribute", "attribute_type"], var_name="model", value_name="correct_ratio"
)


combined_df.to_csv(
    "games/multimodal_referencegame/analysis/attribute_influence.csv", index=False
)
