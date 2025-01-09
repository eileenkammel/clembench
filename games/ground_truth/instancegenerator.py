# -*-coding:utf-8 -*-
# Author: Eileen Kammel, 811770
# Date: 2025-01-08 16:32:31

import os
import clemgame
from clemgame.clemgame import GameInstanceGenerator

logger = clemgame.get_logger(__name__)
GAME_NAME = "ground_truth"


class GroundTruthInstanceGenerator(GameInstanceGenerator):

    def __init__(self):
        super().__init__(GAME_NAME)

    def generate_in(self):

        game_counter = 0

        prompt = "Please describe this image."

        experiment = self.add_experiment("tuna")

        for image in os.listdir("games/ground_truth/recources/tuna_images"):
            if image.endswith(".png"):
                game_instance = self.add_game_instance(experiment, game_counter)
                game_instance["prompt"] = prompt
                game_instance["image"] = "games/ground_truth/recources/tuna_images/" + image
                game_counter += 1

        experiment = self.add_experiment("3ds")

        for image in os.listdir("games/ground_truth/recources/3ds_images"):
            if image.endswith(".png"):
                game_instance = self.add_game_instance(experiment, game_counter)
                game_instance["prompt"] = prompt
                game_instance["image"] = "games/ground_truth/recources/3ds_images/" + image
                game_counter += 1


    def on_generate(self):
        self.generate_in()

if __name__ == '__main__':
    GroundTruthInstanceGenerator().generate(filename="instances.json")