# -*-coding:utf-8 -*-
# Author: Eileen Kammel, 811770
# Date: 2024-10-25 15:33:23

# Groups episodes so that each explainer/guesser pair
# plays 10 episodes from one data set (TUNA or 3DS)
# 3 episodes out of one_attribute_id,
# 4 out of two_attribute_id,
# 3 out of three_attribute_id

import json
import random

# set seed for reproducibility
random.seed(1012)


def pair_episodes():
    instances = json.load(
        open("games/multimodal_referencegame/prep/slurk_in.json", "r")
    )
    # Number of games out of each setting

    paired_instances = {"experiments": []}
    # make the 3 sets of 10 episodes for TUNA
    tuna_episodes = {"name": "tuna", "experiment_instances": []}

    three_ds_episodes = {"name": "3ds", "experiment_instances": []}

    mixed_episodes = {"name": "mixed", "experiment_instances": []}

    for experiment_id in range(3):  # 3experiments per set
        tuna_experiment = {"experiment_id": experiment_id, "game_instances": []}
        threeds_experiment = {"experiment_id": experiment_id, "game_instances": []}
        for tuna_exp in range(3):  # tuna experiments
            episodes = instances["experiments"][tuna_exp]["game_instances"]
            sampled_episodes = random.sample(episodes, 3)
            # remove samples episoded from the original list
            for episode in sampled_episodes:
                instances["experiments"][tuna_exp]["game_instances"].remove(episode)
            tuna_experiment["game_instances"].extend(sampled_episodes)
        for threeds_exp in range(3, 6):  # 3ds experiments
            episodes = instances["experiments"][threeds_exp]["game_instances"]
            sampled_episodes = random.sample(episodes, 3)
            # remove samples episoded from the original list
            for episode in sampled_episodes:
                instances["experiments"][threeds_exp]["game_instances"].remove(episode)
            threeds_experiment["game_instances"].extend(sampled_episodes)
        tuna_episodes["experiment_instances"].append(tuna_experiment)
        three_ds_episodes["experiment_instances"].append(threeds_experiment)
    paired_instances["experiments"].append(tuna_episodes)
    paired_instances["experiments"].append(three_ds_episodes)
    # make one game of mixed episodes
    mixed_experiment = {"experiment_id": 0, "game_instances": []}
    for i in range(6):
        mixed_experiment["game_instances"].extend(instances["experiments"][i]["game_instances"])
    mixed_episodes["experiment_instances"].append(mixed_experiment)
    paired_instances["experiments"].append(mixed_episodes)
    with open("games/multimodal_referencegame/prep/slurk_instances.json", "w") as f:
        json.dump(paired_instances, f, indent=4)

if __name__ == "__main__":
    pair_episodes()
