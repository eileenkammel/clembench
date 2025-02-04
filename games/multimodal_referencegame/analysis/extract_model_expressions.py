# -*-coding:utf-8 -*-
# Author: Eileen Kammel, 811770
# Date: 2025-01-27 17:39:52

import json
import os


def extract_model_expressions():
    expressions = {"tuna": {}, "threeds": {}}
    for player_pair in os.listdir("results"):
        # Exclude programmatic player because those are human
        # expressions read from file.
        if os.path.isdir(f"results/{player_pair}") and "programmatic" not in player_pair.lower():
            for game in os.listdir(f"results/{player_pair}"):
                if game == "multimodal_referencegame":
                    for experiment in os.listdir(f"results/{player_pair}/{game}"):
                        if os.path.isdir(f"results/{player_pair}/{game}/{experiment}"):
                            for episode in os.listdir(f"results/{player_pair}/{game}/{experiment}"):
                                if os.path.isdir(f"results/{player_pair}/{game}/{experiment}/{episode}"):
                                    try:
                                        with open(f"results/{player_pair}/{game}/{experiment}/{episode}/interactions.json") as f:
                                            data = json.load(f)
                                            stim_id, model_expression = get_model_expression(data)
                                            if "tuna" in experiment.lower():
                                                if stim_id not in expressions["tuna"]:
                                                    expressions["tuna"][stim_id] = model_expression
                                                else:
                                                    expressions["tuna"][stim_id] += "$" + model_expression
                                            elif "3ds" in experiment.lower():
                                                if stim_id not in expressions["threeds"]:
                                                    expressions["threeds"][stim_id] = model_expression
                                                else:
                                                    expressions["threeds"][stim_id] += "$" + model_expression
                                    except FileNotFoundError:
                                        print(f"File not found: {player_pair}/{game}/{experiment}/{episode}/interactions.json")
                                        continue

    with open("games/multimodal_referencegame/analysis/all_model_expressions.json", "w") as f:
        json.dump(expressions, f)


def get_model_expression(episode_json):
    stim_id = episode_json["turns"][0][0]["action"]["content"]["stimuli_id"]
    model_expression = episode_json["turns"][0][2]["action"]["expression"]
    return stim_id, model_expression


if __name__ == "__main__":
    extract_model_expressions()
