# -*-coding:utf-8 -*-
# Author: Eileen Kammel, 811770
# Date: 2025-01-08 16:32:41

import random
import json
from typing import Dict, List

from clemgame.clemgame import Player


class Instruction:

    def __init__(self):
        self.user_messages = []
        self.system_messages = []

    def add_user_message(self, message, stimuli_id, images:list):
        self.user_messages.append({"role": "user", "content": message, "stimuli_id": stimuli_id, "image": images})

    def add_system_message(self, message):
        self.system_messages.append(message)

    def convert_to_query_messages(self):
        messages = []
        messages.append({"role": "system", "content": ""})
        for i in range(0, len(self.user_messages)):
            messages.append(self.user_messages[i])

            if i < len(self.system_messages):
                messages.append({"role": "assistant", "content": self.system_messages[i]})

        return messages

    def serialize(self):
        output = []

        for i in range(0, len(self.user_messages)):
            t = {"user": self.user_messages[i]}

            if i < len(self.system_messages):
                t["assistant"] = self.system_messages[i]
            output.append(t)
        return output

    def get_last_user_message(self):
        return self.user_messages[-1]

    def get_last_system_message(self):
        return self.system_messages[-1]


class ImageDescriber(Player):
    def __init__(self, model_name):
        super().__init__(model_name)

    def __call__(self, instruction: Instruction, turn_idx):
        return super().__call__(instruction.convert_to_query_messages(), turn_idx)

    def _custom_response(self, messages, turn_idx):
        return f"Description: {random.choice(['chair', 'desk', 'sofa'])}"
    

class GroundTruthGame:
    def __init__(self, game_instance: Dict, player_backends: List[str]):
        self.player_backends = player_backends
        self.id = game_instance["game_id"]
        self.prompt = game_instance["prompt"]
        self.image = game_instance["image"]

        self.image_describer = ImageDescriber(player_backends[0])

        self.given_instruction = Instruction()
        self.followed_instruction = Instruction()

        self.turn_count = 0

    def proceeds(self) -> bool:
        return True
