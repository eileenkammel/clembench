# -*-coding:utf-8 -*-
# Author: Eileen Kammel, 811770
# Date: 2025-02-09 19:51:52

import json


def sort_he():
    with open(
        "games/multimodal_referencegame/analysis/successful_human_expressions.json", "r"
    ) as file:
        data = json.load(file)
    sorted_tuna = sort_by_stimuli_id(data, "tuna")
    sorted_3ds = sort_by_stimuli_id(data, "3ds")
    sorted_mixed = sort_by_stimuli_id(data, "mixed")

    with open(
        "games/multimodal_referencegame/analysis/sorted_successful_he.json", "w"
    ) as file:
        json.dump(
            {"tuna": sorted_tuna, "3ds": sorted_3ds, "mixed": sorted_mixed},
            file,
            indent=4,
        )


def sort_by_stimuli_id(data, category):
    return sorted(data.get(category, []), key=lambda x: x["stimuli_id"])


if __name__ == "__main__":
    sort_he()
