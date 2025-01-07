# -*-coding:utf-8 -*-
# Author: Eileen Kammel, 811770
# Date: 2024-10-25 13:23:45

# Get rid of fields not needed for Slurk

import os
import json


def prune_path(path):
    path = path.replace("games/multimodal_referencegame/resources/", "")
    return path


def return_p2_target_pos(episode):
    pos = episode["target_image_name"]
    return pos[1]


def prep_for_slurk():
    instances = json.load(open(
        "games/multimodal_referencegame/in/my_instances_3distractors.json", "r")
    )
    fields_to_remove = [
        "player_1_prompt_header",
        "player_2_prompt_header",
        "target_image_name",
        "player_1_response_pattern",
        "player_2_response_pattern",
        "player_1_response_tag",
        "player_2_response_tag",
        "human_expression",
    ]
    fields_with_path = [
        "player_1_first_image",
        "player_1_second_image",
        "player_1_third_image",
        "player_1_fourth_image",
        "player_2_first_image",
        "player_2_second_image",
        "player_2_third_image",
        "player_2_fourth_image",
    ]
    for experiment in instances["experiments"]:
        for episode in experiment["game_instances"]:
            player_2_target_pos = episode["target_image_name"] = return_p2_target_pos(
                episode
            )
            for field in fields_to_remove:
                episode.pop(field, None)
            for field in fields_with_path:
                episode[field] = prune_path(episode[field])
            episode["player_2_target_position"] = player_2_target_pos
    with open("games/multimodal_referencegame/prep/slurk_in.json", "w") as f:
        json.dump(instances, f, indent=4)


if __name__ == "__main__":
    prep_for_slurk()