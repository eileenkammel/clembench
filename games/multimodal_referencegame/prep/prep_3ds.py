# -*-coding:utf-8 -*-
# Author: Eileen Kammel, 811770
# Date: 2024-10-22 18:45:39

# This script prepares the 3DShapenet dataset for the multimodal reference game.
import argparse
from games.multimodal_referencegame.prep.get_3ds import refine_3ds
from games.multimodal_referencegame.prep.make_3ds_stimuli import make_stimuli_sets


def prep_3Ds(distractors):
    refine_3ds()
    make_stimuli_sets(distractor_count=distractors)

    print("3DS dataset prepared for the multimodal reference game.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--distractors",
        type=int,
        default=3,
        help="Number of distractors in the stimuli sets.",
    )
    args = parser.parse_args()
    prep_3Ds(args.distractors)
