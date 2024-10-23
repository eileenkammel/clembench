# -*-coding:utf-8 -*-
# Author: Eileen Kammel, 811770
# Date: 2024-10-23 13:17:58

import random
import clemgame
from clemgame.clemgame import GameInstanceGenerator


random.seed(123)

logger = clemgame.get_logger(__name__)
GAME_NAME = "multimodal_referencegame"

# MAX_NUMBER_INSTANCES = 30


class ReferenceGameInstanceGenerator(GameInstanceGenerator):

    def __init__(self):
        super().__init__(GAME_NAME)

    def get_tuna_dataset(self):
        tuna = self.load_json(
            "prep/tuna/tuna_3_distractor_stimuli.json"
        )
        return tuna

    def get_3ds_dataset(self):
        three_ds = self.load_json(
            "prep/3DS/3ds_3_distractor_instances.json"
        )
        return three_ds

    def generate_tuna_instances(self):

        tuna = self.get_tuna_dataset()
        game_counter = 0
        for id_type in tuna["INSTANCES"]:
            counter = 0
            instances = tuna["INSTANCES"][id_type]
            experiment = self.add_experiment("TUNA_" + id_type)

            # shuffle them for more diverse targets
            random.shuffle(instances)

            player_1_prompt_header = self.load_template(
                "resources/initial_prompts/player_1_prompt_images.template"
            )
            player_2_prompt_header = self.load_template(
                "resources/initial_prompts/player_2_prompt_image.template"
            )
            for instance in instances:
                if counter >= 10:
                    break
                counter += 1
                game_instance = self.add_game_instance(experiment, game_counter)
                player_1_first_image = ""
                player_1_second_image = ""
                player_1_third_image = ""
                player_1_fourth_image = ""
                player_2_first_image = ""
                player_2_second_image = ""
                player_2_third_image = ""
                player_2_fourth_image = ""
                # if game_counter >= MAX_NUMBER_INSTANCES:
                #     break
                tuna_img_path = "games/multimodal_referencegame/resources/tuna_images/"
                # load 3 images
                target = instance["target"]
                distractor1 = instance["distractor1"]
                distractor2 = instance["distractor2"]
                distractor3 = instance["distractor3"]
                # select random target position
                target_position = random.choice([1, 2, 3, 4])
                # create game instance
                if target_position == 1:
                    player_1_first_image = tuna_img_path + target
                    player_1_second_image = tuna_img_path + distractor1
                    player_1_third_image = tuna_img_path + distractor2
                    player_1_fourth_image = tuna_img_path + distractor3

                    player_1_target_pos = 1

                    player_2_first_image = tuna_img_path + distractor1
                    player_2_second_image = tuna_img_path + target
                    player_2_third_image = tuna_img_path + distractor2
                    player_2_fourth_image = tuna_img_path + distractor3

                    player_2_target_name = ["second", "2", "2nd"]

                    player_1_prompt_header = player_1_prompt_header.replace(
                        "TARGET_IMAGE_POSITION", "first"
                    )

                elif target_position == 2:
                    player_1_first_image = tuna_img_path + distractor2
                    player_1_second_image = tuna_img_path + distractor1
                    player_1_third_image = tuna_img_path + target
                    player_1_fourth_image = tuna_img_path + distractor3

                    player_1_target_pos = 2

                    player_2_first_image = tuna_img_path + distractor1
                    player_2_second_image = tuna_img_path + target
                    player_2_third_image = tuna_img_path + distractor2
                    player_2_fourth_image = tuna_img_path + distractor3

                    player_2_target_name = ["first", "1", "1st"]

                    player_1_prompt_header = player_1_prompt_header.replace(
                        "TARGET_IMAGE_POSITION", "third"
                    )

                elif target_position == 3:
                    player_1_first_image = tuna_img_path + distractor2
                    player_1_second_image = tuna_img_path + distractor3
                    player_1_third_image = tuna_img_path + distractor1
                    player_1_fourth_image = tuna_img_path + target

                    player_1_target_pos = 3

                    player_2_first_image = tuna_img_path + distractor2
                    player_2_second_image = tuna_img_path + distractor1
                    player_2_third_image = tuna_img_path + target
                    player_2_fourth_image = tuna_img_path + distractor3

                    player_2_target_name = ["third", "3", "3rd"]

                    player_1_prompt_header = player_1_prompt_header.replace(
                        "TARGET_IMAGE_POSITION", "fourth"
                    )
                elif target_position == 4:
                    player_1_first_image = tuna_img_path + distractor2
                    player_1_second_image = tuna_img_path + target
                    player_1_third_image = tuna_img_path + distractor3
                    player_1_fourth_image = tuna_img_path + distractor1

                    player_1_target_pos = 4

                    player_2_first_image = tuna_img_path + distractor2
                    player_2_second_image = tuna_img_path + distractor1
                    player_2_third_image = tuna_img_path + distractor3
                    player_2_fourth_image = tuna_img_path + target

                    player_2_target_name = ["fourth", "4", "4th"]

                    player_1_prompt_header = player_1_prompt_header.replace(
                        "TARGET_IMAGE_POSITION", "second"
                    )

                game_instance["player_1_prompt_header"] = player_1_prompt_header
                game_instance["player_1_first_image"] = player_1_first_image
                game_instance["player_1_second_image"] = player_1_second_image
                game_instance["player_1_third_image"] = player_1_third_image
                game_instance["player_1_fourth_image"] = player_1_fourth_image
                game_instance["player_1_target_position"] = player_1_target_pos

                game_instance["player_2_prompt_header"] = player_2_prompt_header
                game_instance["player_2_first_image"] = player_2_first_image
                game_instance["player_2_second_image"] = player_2_second_image
                game_instance["player_2_third_image"] = player_2_third_image
                game_instance["player_2_fourth_image"] = player_2_fourth_image
                game_instance["target_image_name"] = player_2_target_name
                game_instance["player_1_response_pattern"] = (
                    "^expression:\s(?P<content>.+)\n*(?P<remainder>.*)"
                )

                # named groups:
                # 'content' captures only the generated referring expression
                # 'remainder' should be empty (if models followed the instructions)
                game_instance["player_2_response_pattern"] = (
                    "^answer:\s(?P<content>first|second|third|fourth|1|2|3|4|1st|2nd|3rd|4th)\n*(?P<remainder>.*)"
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

                # if game_counter >= MAX_NUMBER_INSTANCES:
                #     break

    def generate_3ds_instances(self):
        three_ds = self.get_3ds_dataset()
        game_counter = 0
        for id_type in three_ds["INSTANCES"]:
            counter = 0
            instances = three_ds["INSTANCES"][id_type]
            experiment = self.add_experiment("3DS_" + id_type)
            # shuffle them for more diverse targets
            random.shuffle(instances)

            player_1_prompt_header = self.load_template(
                "resources/initial_prompts/player_1_prompt_images.template"
            )
            player_2_prompt_header = self.load_template(
                "resources/initial_prompts/player_2_prompt_image.template"
            )
            for instance in instances:
                if counter >= 10:
                    break
                counter += 1
                game_instance = self.add_game_instance(experiment, game_counter)
                player_1_first_image = ""
                player_1_second_image = ""
                player_1_third_image = ""
                player_2_first_image = ""
                player_2_second_image = ""
                player_2_third_image = ""
                # if game_counter >= MAX_NUMBER_INSTANCES:
                #     break

                three_ds_img_path = (
                    "games/multimodal_referencegame/resources/3ds_images/"
                )

                # load 3 images
                target = instance["target"]
                distractor1 = instance["distractor1"]
                distractor2 = instance["distractor2"]
                distractor3 = instance["distractor3"]
                # select random target position
                target_position = random.choice([1, 2, 3, 4])
                # create game instance
                if target_position == 1:
                    player_1_first_image = three_ds_img_path + target
                    player_1_second_image = three_ds_img_path + distractor1
                    player_1_third_image = three_ds_img_path + distractor2
                    player_1_fourth_image = three_ds_img_path + distractor3

                    player_1_target_pos = 1

                    player_2_first_image = three_ds_img_path + distractor1
                    player_2_second_image = three_ds_img_path + target
                    player_2_third_image = three_ds_img_path + distractor2
                    player_2_fourth_image = three_ds_img_path + distractor3

                    player_2_target_name = ["second", "2", "2nd"]

                    player_1_prompt_header = player_1_prompt_header.replace(
                        "TARGET_IMAGE_POSITION", "first"
                    )

                elif target_position == 2:
                    player_1_first_image = three_ds_img_path + distractor2
                    player_1_second_image = three_ds_img_path + distractor1
                    player_1_third_image = three_ds_img_path + target
                    player_1_fourth_image = three_ds_img_path + distractor3

                    player_1_target_pos = 2

                    player_2_first_image = three_ds_img_path + distractor1
                    player_2_second_image = three_ds_img_path + target
                    player_2_third_image = three_ds_img_path + distractor2
                    player_2_fourth_image = three_ds_img_path + distractor3

                    player_2_target_name = ["first", "1", "1st"]

                    player_1_prompt_header = player_1_prompt_header.replace(
                        "TARGET_IMAGE_POSITION", "third"
                    )

                elif target_position == 3:
                    player_1_first_image = three_ds_img_path + distractor2
                    player_1_second_image = three_ds_img_path + distractor3
                    player_1_third_image = three_ds_img_path + distractor1
                    player_1_fourth_image = three_ds_img_path + target

                    player_1_target_pos = 3

                    player_2_first_image = three_ds_img_path + distractor2
                    player_2_second_image = three_ds_img_path + distractor1
                    player_2_third_image = three_ds_img_path + target
                    player_2_fourth_image = three_ds_img_path + distractor3

                    player_2_target_name = ["third", "3", "3rd"]

                    player_1_prompt_header = player_1_prompt_header.replace(
                        "TARGET_IMAGE_POSITION", "fourth"
                    )
                elif target_position == 4:
                    player_1_first_image = three_ds_img_path + distractor2
                    player_1_second_image = three_ds_img_path + target
                    player_1_third_image = three_ds_img_path + distractor3
                    player_1_fourth_image = three_ds_img_path + distractor1

                    player_1_target_pos = 4

                    player_2_first_image = three_ds_img_path + distractor2
                    player_2_second_image = three_ds_img_path + distractor1
                    player_2_third_image = three_ds_img_path + distractor3
                    player_2_fourth_image = three_ds_img_path + target

                    player_2_target_name = ["fourth", "4", "4th"]

                    player_1_prompt_header = player_1_prompt_header.replace(
                        "TARGET_IMAGE_POSITION", "second"
                    )

                game_instance["player_1_prompt_header"] = player_1_prompt_header
                game_instance["player_1_first_image"] = player_1_first_image
                game_instance["player_1_second_image"] = player_1_second_image
                game_instance["player_1_third_image"] = player_1_third_image
                game_instance["player_1_fourth_image"] = player_1_fourth_image
                game_instance["player_1_target_position"] = player_1_target_pos

                game_instance["player_2_prompt_header"] = player_2_prompt_header
                game_instance["player_2_first_image"] = player_2_first_image
                game_instance["player_2_second_image"] = player_2_second_image
                game_instance["player_2_third_image"] = player_2_third_image
                game_instance["player_2_fourth_image"] = player_2_fourth_image
                game_instance["target_image_name"] = player_2_target_name
                game_instance["player_1_response_pattern"] = (
                    "^expression:\s(?P<content>.+)\n*(?P<remainder>.*)"
                )

                # named groups:
                # 'content' captures only the generated referring expression
                # 'remainder' should be empty (if models followed the instructions)
                game_instance["player_2_response_pattern"] = (
                    "^answer:\s(?P<content>first|second|third|fourth|1|2|3|4|1st|2nd|3rd|4th)\n*(?P<remainder>.*)"
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

                # if game_counter >= MAX_NUMBER_INSTANCES:
                #     break

    def on_generate(self):
        self.generate_tuna_instances()
        self.generate_3ds_instances()


if __name__ == "__main__":
    ReferenceGameInstanceGenerator().generate(filename="my_instances_3distractors.json")
