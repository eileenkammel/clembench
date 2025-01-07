# -*-coding:utf-8 -*-
# Author: Eileen Kammel, 811770
# Date: 2024-10-22 13:47:57

# This func deletes all images that are not used in the experiments.

import os
import json


def get_all_used_images():
    # get set of images used in my_instances_3distractors.json
    with open(
        "games/multimodal_referencegame/in/my_instances_3distractors.json"
    ) as f:
        data = json.load(f)
    used_images = set()
    for experiment in data["experiments"]:
        for instance in experiment["game_instances"]:
            used_images.add(instance["player_1_first_image"])
            used_images.add(instance["player_1_second_image"])
            used_images.add(instance["player_1_third_image"])
            used_images.add(instance["player_1_fourth_image"])
    tuna = 0
    threeds = 0
    for img in used_images:
        if "tuna" in img:
            tuna += 1
        elif "3ds" in img:
            threeds += 1
    print(f"Used {tuna} tuna images")
    print(f"Used {threeds} 3ds images")
    return used_images


def delete_unused_images():
    images_kept = 0
    images_deleted = 0

    # Define the path to the images that should be deleted
    TUNA_img_path = "games/multimodal_referencegame/resources/tuna_images"
    ThreeDS_img_path = "games/multimodal_referencegame/resources/3ds_images"
    used_images = get_all_used_images()
    # Loop over images and compare if used
    for img in os.listdir(TUNA_img_path):
        img = os.path.join(TUNA_img_path, img)
        if img not in used_images:
            os.remove(img)
            images_deleted += 1
        else:
            images_kept += 1
    print(f"Deleted {images_deleted} images from TUNA")
    print(f"Kept {images_kept} images from TUNA")
    images_kept = 0
    images_deleted = 0
    for img in os.listdir(ThreeDS_img_path):
        img = os.path.join(ThreeDS_img_path, img)
        if img not in used_images:
            os.remove(img)
            images_deleted += 1
        else:
            images_kept += 1
    print(f"Deleted {images_deleted} images from 3DS")
    print(f"Kept {images_kept} images from 3DS")


if __name__ == "__main__":
    delete_unused_images()
