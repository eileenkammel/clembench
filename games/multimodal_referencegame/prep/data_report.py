# -*-coding:utf-8 -*-
# Author: Eileen Kammel, 811770
# Date: 2025-01-13 15:32:30

# This script creates a report of the key facts for ma data sets
# used for thesis writing

import json
from collections import Counter


def load_instances():
    all_instances_path = "games/multimodal_referencegame/in/instances.json"
    return json.load(open(all_instances_path, "r"))


def get_unique_stimuli_info(eperiment):
    unique_stims = set()
    for instance in eperiment["game_instances"]:
        unique_stims.add(instance["stimuli_id"])
    return len(unique_stims), unique_stims


def get_stimuli_info(set_name, id_list):
    images = set()
    target = []
    id_types = []
    all_stimuli_path = (
        "games/multimodal_referencegame/prep/tuna/tuna_3_distractor_stimuli.json"
        if set_name == "tuna"
        else "games/multimodal_referencegame/prep/3DS/3ds_3_distractor_instances.json"
    )
    all_stimuli = json.load(open(all_stimuli_path, "r"))
    for id in id_list:
        for experiment in all_stimuli["INSTANCES"]:
            for episode in all_stimuli["INSTANCES"][experiment]:
                if episode["stimuli_id"] == id:
                    target.append(episode["target"])
                    images.add(episode["target"])
                    images.add(episode["distractor1"])
                    images.add(episode["distractor2"])
                    images.add(episode["distractor3"])
                    id_types.append(episode["id_type"])

    return images, target, id_types


def analyze_id_types(id_types):
    id_type_counter = Counter(id_types)
    pairs = list(id_type_counter.items())
    # make dicts from pairs
    id_type_dict = dict(pairs)
    # sort dict by value
    id_type_dict = dict(sorted(id_type_dict.items(), key=lambda item: item[1], reverse=True))
    return id_type_dict


def print_report():
    instances = load_instances()
    tuna_instances = 0
    tuna_stimuli_count = 0
    tuna_stimuli = set()
    used_tuna_images = set()
    tuna_targets = []
    tuna_id_types = []
    threeds_instances = 0
    threeds_stimuli_count = 0
    threeds_stimuli = set()
    threeds_targets = set()
    used_3ds_images = set()
    threeds_targets = []
    threeds_id_types = []

    for experiment in instances["experiments"]:
        set_name = "tuna" if "TUNA" in experiment["name"] else "3DS"
        unique_stimuli_count, unique_stimuli = get_unique_stimuli_info(experiment)
        if set_name == "tuna":
            tuna_instances += len(experiment["game_instances"])
            tuna_stimuli_count += unique_stimuli_count
            tuna_stimuli.update(unique_stimuli)
        else:
            threeds_instances += len(experiment["game_instances"])
            threeds_stimuli_count += unique_stimuli_count
            threeds_stimuli.update(unique_stimuli)
    used_tuna_images, tuna_targets, tuna_id_types = get_stimuli_info("tuna", tuna_stimuli)
    used_3ds_images, threeds_targets, threeds_id_types = get_stimuli_info("3DS", threeds_stimuli)

    # furter analyze id types
    tuna_id_types = analyze_id_types(tuna_id_types)
    threeds_id_types = analyze_id_types(threeds_id_types)

    # Print report
    print("\n")
    print("TUNA")
    print("Number of instances: ", tuna_instances)
    print("Number of unique stimuli: ", tuna_stimuli_count)
    print("Number of used images: ", len(used_tuna_images))
    print("Number of targets: ", len(tuna_targets))
    print("Number of unique targets: ", len(set(tuna_targets)))
    print("Number of different ID types: ", len(tuna_id_types))
    print("ID types: ", tuna_id_types)
    print("\n")
    print("3DS")
    print("Number of instances: ", threeds_instances)
    print("Number of unique stimuli: ", threeds_stimuli_count)
    print("Number of used images: ", len(used_3ds_images))
    print("Number of targets: ", len(threeds_targets))
    print("Number of unique targets: ", len(set(threeds_targets)))
    print("Number of different ID types: ", len(threeds_id_types))
    print("ID types: ", threeds_id_types)
    print("\n")


if __name__ == "__main__":
    print_report()