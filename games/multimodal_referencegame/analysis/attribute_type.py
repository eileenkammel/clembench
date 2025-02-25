# -*-coding:utf-8 -*-
# Author: Eileen Kammel, 811770
# Date: 2025-02-25 20:24:56

# Determine if some attributes make id harder
import json
import pandas as pd

TUNA_ATTRIBUTES = ["colour", "type,", "size", "orientation"]

THREEDS_ATTRIBUTES = [
    "shape",
    "scale",
    "floorHue",
    "wallHue",
    "objectHue",
    "orientation",
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

# To do: For each attribute, check outcome of episodes and
# compute ration of failed episodes to total episodes. Does one attribute
# make the stimuli harder to identify?
