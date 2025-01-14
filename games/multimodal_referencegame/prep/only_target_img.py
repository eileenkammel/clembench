# -*-coding:utf-8 -*-
# Author: Eileen Kammel, 811770
# Date: 2025-01-14 14:26:21

# This script creates a new data set with only the target images
# for use with ground_truth game.
# As seed is set during instances creation, targets should never change
# and can be hardcoded here. Will break if another seed is used.

import os
import shutil


TUNA_TARGETS = [
    "57.png",
    "52.png",
    "88.png",
    "40.png",
    "0.png",
    "52.png",
    "89.png",
    "64.png",
    "70.png",
    "53.png",
    "89.png",
    "4.png",
    "95.png",
    "70.png",
    "20.png",
    "71.png",
    "9.png",
    "60.png",
    "85.png",
    "10.png",
    "60.png",
    "96.png",
    "15.png",
    "79.png",
    "27.png",
    "22.png",
    "44.png",
    "51.png",
    "11.png",
    "12.png",
]
THREEDS_TARGETS = [
    "1550.png",
    "16856.png",
    "8093.png",
    "2157.png",
    "6528.png",
    "4667.png",
    "3435.png",
    "12985.png",
    "1550.png",
    "1387.png",
    "10067.png",
    "12084.png",
    "15997.png",
    "15752.png",
    "15301.png",
    "17761.png",
    "5496.png",
    "12800.png",
    "13604.png",
    "12800.png",
    "10713.png",
    "4610.png",
    "7303.png",
    "12905.png",
    "11500.png",
    "6132.png",
    "11783.png",
    "2157.png",
    "8774.png",
    "4890.png",
]


def create_target_sets():
    os.makedirs("games/multimodal_referencegame/prep/tuna_targets", exist_ok=True)
    os.makedirs("games/multimodal_referencegame/prep/3DS_targets", exist_ok=True)
    # make tuna target set
    for img in TUNA_TARGETS:
        shutil.copy(
            f"games/multimodal_referencegame/resources/tuna_images/{img}",
            f"games/multimodal_referencegame/prep/tuna_targets/{img}",
        )
    # make 3DS target set
    for img in THREEDS_TARGETS:
        shutil.copy(
            f"games/multimodal_referencegame/resources/3ds_images/{img}",
            f"games/multimodal_referencegame/prep/3DS_targets/{img}",
        )


if __name__ == "__main__":
    create_target_sets()
