# -*-coding:utf-8 -*-
# Author: Eileen Kammel, 811770
# Date: 2025-01-08 15:42:03

from typing import List, Dict, Tuple

import numpy as np

import clemgame.metrics as ms
from clemgame.clemgame import GameMaster, GameBenchmark, DialogueGameMaster, GameScorer
from clemgame import get_logger
from clemgame.clemgame import Player

from backends import Model, CustomResponseModel
#from games.cloudgame.players import Speaker
from clemgame.metrics import METRIC_ABORTED, METRIC_SUCCESS, METRIC_LOSE, BENCH_SCORE, METRIC_REQUEST_COUNT, METRIC_REQUEST_COUNT_PARSED,  METRIC_REQUEST_COUNT_VIOLATED, METRIC_REQUEST_SUCCESS
from games.ground_truth.game import GroundTruthGame

GAME_NAME = "ground_truth"
logger = get_logger(__name__)


class GroundTruthMaster(GameMaster):

    def __init__(self, experiment: Dict, player_models: List[Model]):
        super().__init__(GAME_NAME, experiment, player_models)
        self.experiment = experiment
        self.game = None
        self.game_instance = None

    def setup(self, **game_instance):
        self.game_instance = game_instance
        self.game = GroundTruthGame(self.game_instance, self.player_models)

        self.log_players({
            "GM": "Game Master for GroundTruth",
            "Player1": self.player_models[0].get_name(),
        }
        )

    @classmethod
    def applies_to(cls, game_name: str) -> bool:
        return game_name == GAME_NAME

    def play(self) -> None:
        logger.info("Game turn: %d", self.game.turn_count)
        self.turn()

    def turn(self):
        self.log_next_turn()

        self.game.given_instruction.add_user_message(
            self.game.prompt,
            self.game.id,
            images=[self.game.image],
            )

        action = {
            "type": "send_message",
            "content": self.game.given_instruction.user_messages[-1],
        }
        self.log_event(from_="GM", to="Describer Player", action=action)

        player_prompt, player_response, player_response_text = (
            self.game.image_describer(self.game.given_instruction, None)
        )

        action = {"type": "get message", "content": player_response_text}
        self.log_event(
            from_="Describer Player",
            to="GM",
            action=action,
            call=(player_prompt, player_response),
        )

        self.game.given_instruction.add_system_message(player_response_text)

        self.game.turn_count += 1


class GroundTruthScorer(GameScorer):

    def __init__(self, experiment: Dict, game_instance: Dict):
        super().__init__(GAME_NAME, experiment, game_instance)


class GroundTruthBenchmark(GameBenchmark):

    def __init__(self):
        super().__init__(GAME_NAME)

    def is_single_player(self):
        return True

    def get_description(self):
        return "Lets models describe images without game context."

    def create_game_master(self, experiment, player_models):
        return GroundTruthMaster(experiment, player_models)

    def create_game_scorer(self, experiment, game_instance):
        return GroundTruthScorer(experiment, game_instance)
