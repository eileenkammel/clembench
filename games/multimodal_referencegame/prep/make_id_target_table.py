# -*-coding:utf-8 -*-
# Author: Eileen Kammel, 811770
# Date: 2025-02-13 14:03:53

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
]


tuna_stimuli = json.load(open("games/multimodal_referencegame/prep/tuna/tuna_3_distractor_stimuli.json", "r"))
threeds_stimuli = json.load(open("games/multimodal_referencegame/prep/3DS/3ds_3_distractor_instances.json", "r"))
id_target_table = {"tuna": dict(), "threeds": dict()}

for id in TUNA_STIMULI_IDS:
    for id_type in tuna_stimuli["INSTANCES"]:
        for episode in tuna_stimuli["INSTANCES"][id_type]:
            if episode["stimuli_id"] == id:
                id_target_table["tuna"][id] = episode["target"]
for id in THREEDS_STIMULI_IDS:
    for id_type in threeds_stimuli["INSTANCES"]:
        for episode in threeds_stimuli["INSTANCES"][id_type]:
            if episode["stimuli_id"] == id:
                id_target_table["threeds"][id] = episode["target"]

with open("games/multimodal_referencegame/analysis/id_target_table.json", "w") as f:
    json.dump(id_target_table, f)