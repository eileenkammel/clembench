# -*-coding:utf-8 -*-
# Author: Eileen Kammel, 811770
# Date: 2024-11-28 11:08:08

# This script creates a mapping between the stimulus ids and the corresponding
# id types
# Takes id from the my_instance file and looks up id type in all stimulus file

import json


def get_idtype(set_name, stimulus_id):
    all_stimuli_path = (
        "games/multimodal_referencegame/prep/tuna/tuna_3_distractor_stimuli.json"
        if set_name == "tuna"
        else "games/multimodal_referencegame/prep/3DS/3ds_3_distractor_instances.json"
    )
    all_stimuli = json.load(open(all_stimuli_path, "r"))
    for experiment in all_stimuli["INSTANCES"]:
        for episode in all_stimuli["INSTANCES"][experiment]:
            if episode["stimuli_id"] == stimulus_id:
                # print(f"Stimulus ID: {stimulus_id}, \t ID Type: {episode['id_type']}")
                return episode["id_type"], episode["id_attributes"]


def map_ids():
    instances = json.load(
        open("games/multimodal_referencegame/in/instances.json", "r")
    )
    for experiment in instances["experiments"]:
        set_name = "tuna" if "TUNA" in experiment["name"] else "3DS"
        for episode in experiment["game_instances"]:
            get_idtype(set_name, episode["stimuli_id"])


if __name__ == "__main__":
    map_ids()
