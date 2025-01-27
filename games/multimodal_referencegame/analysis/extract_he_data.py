# -*-coding:utf-8 -*-
# Author: Eileen Kammel, 811770
# Date: 2025-01-16 16:25:07

import json
import os


def parse_game_log(logfile):
    with open(logfile, "r") as data:
        game_style = []
        game_log = data.readlines()
        all_data = []
        only_successful = []
        stimuli_id = None
        clue = None
        correct = None
        target = None
        for line in game_log:
            line_json = json.loads(line)
            if "pictures" in line_json["event"]:
                if "tuna" in line_json["data"]["content"][0]:
                    game_style.append("tuna")
                else:
                    game_style.append("3ds")
            if line_json["event"] == "stimuli_id":
                stimuli_id = line_json["data"]["content"]
            if line_json["event"] == "clue":
                clue = line_json["data"]["content"]
            if (
                line_json["event"] == "correct guess"
                or line_json["event"] == "false guess"
            ):
                target = find_target(int(stimuli_id), game_style[-1])
                correct = True if line_json["event"] == "correct guess" else False
                all_data.append(
                    {
                        "stimuli_id": int(stimuli_id),
                        "target": target,
                        "human_expression": clue,
                        "success": correct,
                    }
                )
                if correct:
                    only_successful.append(
                        {
                            "stimuli_id": int(stimuli_id),
                            "target": target,
                            "human_expression": clue,
                            "success": correct,
                        }
                    )
                stimuli_id = None
                clue = None
                correct = None
        game_style = set(game_style)
        game_style = list(game_style)[0] if len(game_style) == 1 else "mixed"

        # determine if all game rounds were played

        if game_style == "tuna" or game_style == "3ds":
            if len(all_data) != 9:
                print("Game was aborted")
        if game_style == "mixed":
            if len(all_data) != 6:
                print("Game was aborted")
        return game_style, all_data, only_successful


def find_target(stimuli_id, game_style):
    if game_style == "tuna":
        with open(
            "games/multimodal_referencegame/prep/tuna/tuna_3_distractor_stimuli.json"
        ) as f:
            data = json.load(f)
            all_stimuli = (
                data["INSTANCES"]["one_attibute_id"]
                + data["INSTANCES"]["two_attibute_id"]
                + data["INSTANCES"]["three_attibute_id"]
            )
            for stimuli in all_stimuli:
                if stimuli["stimuli_id"] == stimuli_id:
                    return stimuli["target"]
    if game_style == "3ds":
        with open(
            "games/multimodal_referencegame/prep/3DS/3ds_3_distractor_instances.json"
        ) as f:
            data = json.load(f)
            all_stimuli = (
                data["INSTANCES"]["one_attibute_id"]
                + data["INSTANCES"]["two_attibute_id"]
                + data["INSTANCES"]["three_attibute_id"]
            )
            for stimuli in all_stimuli:
                if stimuli["stimuli_id"] == stimuli_id:
                    return stimuli["target"]


def parse_all_logs(log_folder):
    all_games = {"tuna": [], "3ds": [], "mixed": []}
    successful_games = {"tuna": [], "3ds": [], "mixed": []}
    all_logs = os.listdir(log_folder)
    for log in all_logs:
        if log.endswith(".jsonl"):
            log_path = os.path.join(log_folder, log)
            game_style, all_logs, successful_logs = parse_game_log(log_path)
            all_games[game_style].extend(all_logs)
            successful_games[game_style].extend(successful_logs)
    # make json file from games dict
    with open("games/multimodal_referencegame/analysis/all_human_expressions.json", "w") as f:
        json.dump(all_games, f)
    with open(
        "games/multimodal_referencegame/analysis/successful_human_expressions.json", "w"
    ) as f:
        json.dump(successful_games, f)
    return all_games, successful_games


if __name__ == "__main__":
    print(parse_all_logs("games/multimodal_referencegame/analysis/slurk_logs"))
