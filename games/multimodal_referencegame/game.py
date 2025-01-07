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


class InstructionFollower(Player):

    def __init__(self, model_name):
        super().__init__(model_name)

    def __call__(self, instruction: Instruction, turn_idx):
        return super().__call__(instruction.convert_to_query_messages(), turn_idx)

    def _custom_response(self, messages, turn_idx):
        answer = random.choice(["first", "second", "third"])
        return f"Answer: {answer}"


class InstructionGiver(Player):

    def __init__(self, model_name):
        super().__init__(model_name)

    def __call__(self, instruction: Instruction, turn_idx):
        return super().__call__(instruction.convert_to_query_messages(), turn_idx)

    def _get_human_expression(self, stimuli_id):
        with open("games/multimodal_referencegame_comprehension/in/instances.json", "r") as f:
            instances = json.load(f)
            for eperiment in instances["experiments"]:
                for game in eperiment["game_instances"]:
                    if game["stimuli_id"] == stimuli_id:
                        return game["human_expression"]

    def _custom_response(self, messages, turn_idx):
        expression = self._get_human_expression(messages[-1]['stimuli_id'])
        return f"Expression: {expression}"


class MultimodalReferenceGame:

    def __init__(self, game_instance: Dict, player_backends: List[str]):
        self.player_backends = player_backends
        self.game_id = game_instance['game_id']
        self.stimuli_id = game_instance['stimuli_id']
        self.player_1_prompt_header = game_instance['player_1_prompt_header']
        self.player_2_prompt_header = game_instance['player_2_prompt_header']
        self.target_image_name = game_instance['target_image_name']
        self.player_backends = player_backends

        self.player_1_response_pattern = r'{}'.format(game_instance['player_1_response_pattern'])
        self.player_2_response_pattern = r'{}'.format(game_instance['player_2_response_pattern'])

        self.player_1_first_image = game_instance['player_1_first_image']
        self.player_1_second_image = game_instance['player_1_second_image']
        self.player_1_third_image = game_instance['player_1_third_image']
        self.player_1_fourth_image = game_instance['player_1_fourth_image']
        self.player_1_human_expression = game_instance['human_expression']

        self.player_2_first_image = game_instance['player_2_first_image']
        self.player_2_second_image = game_instance['player_2_second_image']
        self.player_2_third_image = game_instance['player_2_third_image']
        self.player_2_fourth_image = game_instance['player_2_fourth_image']

        self.instruction_giver = InstructionGiver(player_backends[0])
        self.instruction_follower = InstructionFollower(player_backends[1])

        self.given_instruction = Instruction()
        self.followed_instruction = Instruction()

        self.turn_count = 0


    def proceeds(self) -> bool:
        return True
