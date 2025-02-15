# -*-coding:utf-8 -*-
# Author: Eileen Kammel, 811770
# Date: 2025-01-21 16:54:44

# Extracts the ground truth for target images from results.
# Ground truth game must have been run before this script is run.

import json
import os

COMMERCIAL_MODELS = [
    "gpt-4o-2024-08-06",
    "claude-3-5-sonnet-20240620",
    "gemini-2.0-flash-exp",
]

OPEN_WEIGHED_MODELS = [
    "idefics-80b-instruct",
    "InternVL2-Llama3-76B",
    "InternVL2-40B",
    "InternVL2-8B",
]


def extract_gt():
    gt = dict()
    for model in OPEN_WEIGHED_MODELS:
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
    with open("games/multimodal_referencegame/analysis/ground_truth.json", "w") as f:
        json.dump(gt, f)


def get_img_gt(episode_json):
    image = episode_json["turns"][0][0]["action"]["content"]["image"][0]
    ground_truth = episode_json["turns"][0][1]["action"]["content"]
    return image, ground_truth


if __name__ == "__main__":
    extract_gt()