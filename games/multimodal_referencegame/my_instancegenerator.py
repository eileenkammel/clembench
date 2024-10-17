"""
Generate instances for the referencegame
Version 1.6 (strict regex parsing)

Reads grids_v1.5.json from resources/ (grids don't change in this version)
Creates instances.json in instances/
"""

import os
import random
import clemgame
from clemgame.clemgame import GameInstanceGenerator
import shutil
import matplotlib.pyplot as plt
import json


random.seed(123)

logger = clemgame.get_logger(__name__)
GAME_NAME = "multimodal_referencegame"

MAX_NUMBER_INSTANCES = 30


class ReferenceGameInstanceGenerator(GameInstanceGenerator):

    def __init__(self):
        super().__init__(GAME_NAME)

    def get_tuna_dataset(self):
        tuna = self.load_json("resources/tuna_instances.json")
        return tuna

    def get_3ds_dataset(self):
        three_ds = self.load_json("resources/3ds_instances.json")
        return three_ds

    def generate_tuna_instances(self):

        tuna = self.get_tuna_dataset()
        game_counter = 0
        experiment = self.add_experiment("TUNA_images")

        for id_type in tuna["INSTANCES"]:
            instances = tuna["INSTANCES"][id_type]
            player_1_prompt_header = self.load_template(
                "resources/initial_prompts/player_1_prompt_images.template"
            )
            player_2_prompt_header = self.load_template(
                "resources/initial_prompts/player_2_prompt_image.template"
            )
            for instance in instances:
                game_instance = self.add_game_instance(experiment, game_counter)
                player_1_first_image = ""
                player_1_second_image = ""
                player_1_third_image = ""
                player_2_first_image = ""
                player_2_second_image = ""
                player_2_third_image = ""
                if game_counter >= MAX_NUMBER_INSTANCES:
                    break
                tuna_img_path = "games/multimodal_referencegame/resources/tuna_images/"
                # load 3 images
                target = instance["target"]
                distractor1 = instance["distractor1"]
                distractor2 = instance["distractor2"]
                # select random target position
                target_position = random.choice([1, 2, 3])
                # create game instance
                if target_position == 1:
                    player_1_first_image = tuna_img_path + target
                    player_1_second_image = tuna_img_path + distractor1
                    player_1_third_image = tuna_img_path + distractor2

                    player_2_first_image = tuna_img_path + distractor1
                    player_2_second_image = tuna_img_path + target
                    player_2_third_image = tuna_img_path + distractor2

                    player_2_target_name = ["second", "2", "2nd"]

                    player_1_prompt_header = player_1_prompt_header.replace(
                        "TARGET_IMAGE_POSITION", "first"
                    )

                elif target_position == 2:
                    player_1_first_image = tuna_img_path + distractor2
                    player_1_second_image = tuna_img_path + distractor1
                    player_1_third_image = tuna_img_path + target

                    player_2_first_image = tuna_img_path + target
                    player_2_second_image = tuna_img_path + distractor1
                    player_2_third_image = tuna_img_path + distractor2

                    player_2_target_name = ["first", "1", "1st"]

                    player_1_prompt_header = player_1_prompt_header.replace(
                        "TARGET_IMAGE_POSITION", "third"
                    )

                elif target_position == 3:
                    player_1_first_image = tuna_img_path + distractor2
                    player_1_second_image = tuna_img_path + target
                    player_1_third_image = tuna_img_path + distractor1

                    player_2_first_image = tuna_img_path + distractor2
                    player_2_second_image = tuna_img_path + distractor1
                    player_2_third_image = tuna_img_path + target

                    player_2_target_name = ["third", "3", "3rd"]

                    player_1_prompt_header = player_1_prompt_header.replace(
                        "TARGET_IMAGE_POSITION", "second"
                    )
                game_instance["player_1_prompt_header"] = player_1_prompt_header
                game_instance["player_1_first_image"] = player_1_first_image
                game_instance["player_1_second_image"] = player_1_second_image
                game_instance["player_1_third_image"] = player_1_third_image

                game_instance["player_2_prompt_header"] = player_2_prompt_header
                game_instance["player_2_first_image"] = player_2_first_image
                game_instance["player_2_second_image"] = player_2_second_image
                game_instance["player_2_third_image"] = player_2_third_image
                game_instance["target_image_name"] = player_2_target_name
                game_instance["player_1_response_pattern"] = (
                    "^expression:\s(?P<content>.+)\n*(?P<remainder>.*)"
                )

                # named groups:
                # 'content' captures only the generated referring expression
                # 'remainder' should be empty (if models followed the instructions)
                game_instance["player_2_response_pattern"] = (
                    "^answer:\s(?P<content>first|second|third|1|2|3|1st|2nd|3rd)\n*(?P<remainder>.*)"
                )
                # 'content' can directly be compared to gold answer
                # 'remainder' should be empty (if models followed the instructions)

                # the following two fields are no longer required, but kept for backwards compatibility with previous instance versions
                game_instance["player_1_response_tag"] = "expression:"
                game_instance["player_2_response_tag"] = "answer:"
                # for comprehension run. Gets filled after human trials
                game_instance["human_expression"] = ""
                # might be needed for later analysis, better safe than sorry
                game_instance["stimuli_id"] = instance["stimuli_id"]

                game_counter += 1

                if game_counter >= MAX_NUMBER_INSTANCES:
                    break

    def generate_3ds_instances(self):
        three_ds = self.get_3ds_dataset()
        game_counter = 0
        experiment = self.add_experiment("3DS_images")

        for id_type in three_ds["INSTANCES"]:
            instances = three_ds["INSTANCES"][id_type]
            player_1_prompt_header = self.load_template(
                "resources/initial_prompts/player_1_prompt_images.template"
            )
            player_2_prompt_header = self.load_template(
                "resources/initial_prompts/player_2_prompt_image.template"
            )
            for instance in instances:
                game_instance = self.add_game_instance(experiment, game_counter)
                player_1_first_image = ""
                player_1_second_image = ""
                player_1_third_image = ""
                player_2_first_image = ""
                player_2_second_image = ""
                player_2_third_image = ""
                if game_counter >= MAX_NUMBER_INSTANCES:
                    break

                three_ds_img_path = "games/multimodal_referencegame/resources/3ds_images/"

                # load 3 images
                target = instance["target"]
                distractor1 = instance["distractor1"]
                distractor2 = instance["distractor2"]
                # select random target position
                target_position = random.choice([1, 2, 3])
                # create game instance
                if target_position == 1:
                    player_1_first_image = three_ds_img_path + target
                    player_1_second_image = three_ds_img_path + distractor1
                    player_1_third_image = three_ds_img_path + distractor2

                    player_2_first_image = three_ds_img_path + distractor1
                    player_2_second_image = three_ds_img_path + target
                    player_2_third_image = three_ds_img_path + distractor2

                    player_2_target_name = ["second", "2", "2nd"]

                    player_1_prompt_header = player_1_prompt_header.replace(
                        "TARGET_IMAGE_POSITION", "first"
                    )

                elif target_position == 2:
                    player_1_first_image = three_ds_img_path + distractor2
                    player_1_second_image = three_ds_img_path + distractor1
                    player_1_third_image = three_ds_img_path + target

                    player_2_first_image = three_ds_img_path + target
                    player_2_second_image = three_ds_img_path + distractor1
                    player_2_third_image = three_ds_img_path + distractor2

                    player_2_target_name = ["first", "1", "1st"]

                    player_1_prompt_header = player_1_prompt_header.replace(
                        "TARGET_IMAGE_POSITION", "third"
                    )

                elif target_position == 3:
                    player_1_first_image = three_ds_img_path + distractor2
                    player_1_second_image = three_ds_img_path + target
                    player_1_third_image = three_ds_img_path + distractor1

                    player_2_first_image = three_ds_img_path + distractor2
                    player_2_second_image = three_ds_img_path + distractor1
                    player_2_third_image = three_ds_img_path + target

                    player_2_target_name = ["third", "3", "3rd"]

                    player_1_prompt_header = player_1_prompt_header.replace(
                        "TARGET_IMAGE_POSITION", "second"
                    )
                game_instance["player_1_prompt_header"] = player_1_prompt_header
                game_instance["player_1_first_image"] = player_1_first_image
                game_instance["player_1_second_image"] = player_1_second_image
                game_instance["player_1_third_image"] = player_1_third_image

                game_instance["player_2_prompt_header"] = player_2_prompt_header
                game_instance["player_2_first_image"] = player_2_first_image
                game_instance["player_2_second_image"] = player_2_second_image
                game_instance["player_2_third_image"] = player_2_third_image
                game_instance["target_image_name"] = player_2_target_name
                game_instance["player_1_response_pattern"] = (
                    "^expression:\s(?P<content>.+)\n*(?P<remainder>.*)"
                )

                # named groups:
                # 'content' captures only the generated referring expression
                # 'remainder' should be empty (if models followed the instructions)
                game_instance["player_2_response_pattern"] = (
                    "^answer:\s(?P<content>first|second|third|1|2|3|1st|2nd|3rd)\n*(?P<remainder>.*)"
                )
                # 'content' can directly be compared to gold answer
                # 'remainder' should be empty (if models followed the instructions)

                # the following two fields are no longer required, but kept for backwards compatibility with previous instance versions
                game_instance["player_1_response_tag"] = "expression:"
                game_instance["player_2_response_tag"] = "answer:"
                # for comprehension run. Gets filled after human trials
                game_instance["human_expression"] = ""
                # might be needed for later analysis, better safe than sorry
                game_instance["stimuli_id"] = instance["stimuli_id"]

                game_counter += 1

                if game_counter >= MAX_NUMBER_INSTANCES:
                    break

    def on_generate(self):
        self.generate_tuna_instances()
        self.generate_3ds_instances()


if __name__ == "__main__":
    ReferenceGameInstanceGenerator().generate(filename="my_instances.json")
