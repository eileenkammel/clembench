# -*-coding:utf-8 -*-
# Author: Eileen Kammel, 811770
# Date: 2025-01-23 16:04:46

# Inserts human expression into instances

import json


def load_he():
    with open("games/multimodal_referencegame/analysis/selected_he.json") as f:
        return json.load(f)


def insert_he():
    instances = json.load(open("games/multimodal_referencegame/in/instances.json"))
    for experiment in instances["experiments"]:
        for instance in experiment["game_instances"]:
            target = determine_target(instance)
            if "tuna" in target:
                human_expression = retrieve_he("tuna", instance["stimuli_id"])
            else:
                human_expression = retrieve_he("3ds", instance["stimuli_id"])
            instance["human_expression"] = human_expression
    with open("games/multimodal_referencegame/in/instances.json", "w") as f:
        json.dump(instances, f)


def determine_target(instance):
    taget_pos = instance["player_1_target_position"]
    if taget_pos == 1:
        return instance["player_1_first_image"]
    if taget_pos == 2:
        return instance["player_1_second_image"]
    if taget_pos == 3:
        return instance["player_1_third_image"]
    if taget_pos == 4:
        return instance["player_1_fourth_image"]


def retrieve_he(set_name, stim_id):
    human_expressions = load_he()
    if set_name == "tuna":
        for game in human_expressions["tuna"] + human_expressions["mixed"]:
            if game["stimuli_id"] == stim_id:
                return game["human_expression"]
    if set_name == "3ds":
        for game in human_expressions["3ds"] + human_expressions["mixed"]:
            if game["stimuli_id"] == stim_id:
                return game["human_expression"]


if __name__ == "__main__":
    insert_he()
