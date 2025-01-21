# -*-coding:utf-8 -*-
# Author: Eileen Kammel, 811770
# Date: 2025-01-21 16:54:44

# Extracts the ground truth for target images from results.
# Ground truth game must have been run before this script is run.

import json
import os


def extract_gt():
    gt = {"tuna": {}, "threeds": {}}
    for player_pair in os.listdir("results"):
        for game in os.listdir(f"results/{player_pair}"):
            if game == "ground_truth":
                for experiment in os.listdir(f"results/{player_pair}/{game}"):
                    print(experiment)
                    for episode in os.listdir(f"results/{player_pair}/{game}/{experiment}"):
                        if os.path.isdir(f"results/{player_pair}/{game}/{experiment}/{episode}"):
                            try:
                                with open(f"results/{player_pair}/{game}/{experiment}/{episode}/interactions.json") as f:
                                    data = json.load(f)
                                    image, ground_truth = get_img_gt(data)
                                    if "tuna" in image:
                                        image = image.split("/")[-1]
                                        gt["tuna"][image] = ground_truth
                                    elif "3ds" in image:
                                        image = image.split("/")[-1]
                                        gt["threeds"][image] = ground_truth
                            except FileNotFoundError:
                                print(f"File not found: {player_pair}/{game}/{experiment}/{episode}/interactions.json")
                                continue
    with open("games/multimodal_referencegame/analysis/ground_truth.json", "w") as f:
        json.dump(gt, f)


def get_img_gt(episode_json):
    image = episode_json["turns"][0][0]["action"]["content"]["image"][0]
    ground_truth = episode_json["turns"][0][1]["action"]["content"]
    return image, ground_truth


if __name__ == "__main__":
    extract_gt()