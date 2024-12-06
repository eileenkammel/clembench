# -*-coding:utf-8 -*-
# Author: Eileen Kammel, 811770
# Date: 2024-10-30 15:22:10

import json
from copy import deepcopy


def swap_imgs(old_pos, new_pos, images):
    """Takes current target pos, new target pos,
    and list of images in current order of appearance.
    Swaps images at old_pos and new_pos and returns
    the updated list of images.
    """
    old_pos_idx = old_pos - 1  # Adjust for 0-based index
    new_pos_idx = new_pos - 1
    images[old_pos_idx], images[new_pos_idx] = images[new_pos_idx], images[old_pos_idx]
    return images


def anti_loc_bias(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)

    pos_names = {
        1: ["first", "1", "1st"],
        2: ["second", "2", "2nd"],
        3: ["third", "3", "3rd"],
        4: ["fourth", "4", "4th"],
    }

    for experiment in data["experiments"]:
        new_instances = []
        for instance in experiment["game_instances"]:
            # Check existing target positions
            existing_position = int(instance["target_image_name"][1])
            # Define missing positions
            missing_positions = [1, 2, 3, 4]
            missing_positions.remove(existing_position)

            # Extract images in current order
            for pos in missing_positions:
                images = [
                    instance["player_2_first_image"],
                    instance["player_2_second_image"],
                    instance["player_2_third_image"],
                    instance["player_2_fourth_image"],
                ]
                # Swap images according to new target position
                images = swap_imgs(existing_position, pos, images)
                new_instance = deepcopy(instance)
                # new_instance["game_id"] = f"{instance["game_id"]}+{}"  # Append suffix to game_id
                new_instance["player_2_first_image"] = images[0]
                new_instance["player_2_second_image"] = images[1]
                new_instance["player_2_third_image"] = images[2]
                new_instance["player_2_fourth_image"] = images[3]

                new_instance["target_image_name"] = pos_names[pos]
                new_instances.append(new_instance)

        # Add new instances back to experiment"s instances
        experiment["game_instances"].extend(new_instances)

    # Save the updated file
    updated_file_path = "games/multimodal_referencegame/in/updated_my_instances_3distractors.json"
    with open(updated_file_path, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Updated file saved to: {updated_file_path}")

if __name__ == "__main__":
    anti_loc_bias("games/multimodal_referencegame/in/my_instances_3distractors.json")
