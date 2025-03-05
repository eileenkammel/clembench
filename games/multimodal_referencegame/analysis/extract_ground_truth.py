# -*-coding:utf-8 -*-
# Author: Eileen Kammel, 811770
# Date: 2025-01-21 16:54:44

# Extracts the ground truth for target images from results.
# Ground truth game must have been run before this script is run.

import json
import os
from games.multimodal_referencegame.analysis.constants import ALL_MODELS


def extract_gt(models, output_path):
    gt = dict()
    for model in models:
        gt[model] = {"tuna": dict(), "threeds": dict()}
        path = path = f"results/{model}-t0.0--{model}-t0.0/ground_truth"
        if os.path.isdir(path):
            for experiment in os.listdir(path):
                if os.path.isdir(f"{path}/{experiment}"):
                    for episode in os.listdir(f"{path}/{experiment}"):
                        if os.path.isdir(f"{path}/{experiment}/{episode}"):
                            try:
                                with open(f"{path}/{experiment}/{episode}/interactions.json") as f:
                                    data = json.load(f)
                                    image, ground_truth = get_img_gt(data)
                                    if "tuna" in image:
                                        image = image.split("/")[-1]
                                        gt[model]["tuna"][image] = ground_truth
                                    elif "3ds" in image:
                                        image = image.split("/")[-1]
                                        gt[model]["threeds"][image] = ground_truth
                            except FileNotFoundError:
                                print(f"File not found: {model}/{experiment}/{episode}/interactions.json")
                                continue
    with open(output_path, "w") as f:
        json.dump(gt, f)


def get_img_gt(episode_json):
    image = episode_json["turns"][0][0]["action"]["content"]["image"][0]
    ground_truth = episode_json["turns"][0][1]["action"]["content"]
    return image, ground_truth


if __name__ == "__main__":
    extract_gt(ALL_MODELS, "games/multimodal_referencegame/analysis/all_gt.json")