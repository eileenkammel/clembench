# -*-coding:utf-8 -*-
# Author: Eileen Kammel, 811770
# Date: 2025-02-26 17:55:01

# Check if answers are consistent
# for all 4 configurations

import json
import pandas as pd
from games.multimodal_referencegame.analysis.constants import (
    ALL_MODELS,
    TUNA_STIMULI_IDS,
    THREEDS_STIMULI_IDS,
)


commercial = pd.read_csv(
    "games/multimodal_referencegame/analysis/commercial_expressions_by_model.csv"
)
commercial_programmatic = pd.read_csv(
    "games/multimodal_referencegame/analysis/commercial_expressions_by_model_programmatic.csv"
)
open_weight = pd.read_csv(
    "games/multimodal_referencegame/analysis/expressions_by_model.csv"
)
open_weight_programmatic = pd.read_csv(
    "games/multimodal_referencegame/analysis/expressions_by_model_programmatic.csv"
)

production = pd.concat([commercial, open_weight])
comprehension = pd.concat([commercial_programmatic, open_weight_programmatic])

production_consistency = pd.DataFrame(columns=["set", "model", "stim_id", "consistent"])
comprehension_consistency = pd.DataFrame(columns=["set", "model", "stim_id", "consistent"])

for model in ALL_MODELS:
    model_df_production = production[production["model"] == model]
    model_df_production = model_df_production[
        model_df_production["status"] == "completed"
    ]
    model_df_comprehension = comprehension[comprehension["model"] == model]
    model_df_comprehension = model_df_comprehension[
        model_df_comprehension["status"] == "completed"
    ]

    for stim_id in TUNA_STIMULI_IDS:
        episodes_production = model_df_production[
            model_df_production["stim_id"] == stim_id
        ]
        outcomes_production = list(episodes_production["correct"])
        if outcomes_production.count(True) == 4:
            production_consistency.loc[len(production_consistency)] = [
                "TUNA",
                model,
                stim_id,
                True,
            ]
        else:
            production_consistency.loc[len(production_consistency)] = [
                "TUNA",
                model,
                stim_id,
                False,
            ]

        episodes_comprehension = model_df_comprehension[
            model_df_comprehension["stim_id"] == stim_id
        ]
        outcomes_comprehension = list(episodes_comprehension["correct"])
        if outcomes_comprehension.count(True) == 4:
            comprehension_consistency.loc[len(comprehension_consistency)] = [
                "TUNA",
                model,
                stim_id,
                True,
            ]
        else:
            comprehension_consistency.loc[len(comprehension_consistency)] = [
                "TUNA",
                model,
                stim_id,
                False,
            ]

    for stim_id in THREEDS_STIMULI_IDS:
        episodes_production = model_df_production[
            model_df_production["stim_id"] == stim_id
        ]
        outcomes_production = list(episodes_production["correct"])
        if outcomes_production.count(True) == 4:
            production_consistency.loc[len(production_consistency)] = [
                "3DS",
                model,
                stim_id,
                True,
            ]
        else:
            production_consistency.loc[len(production_consistency)] = [
                "3DS",
                model,
                stim_id,
                False,
            ]

        episodes_comprehension = model_df_comprehension[
            model_df_comprehension["stim_id"] == stim_id
        ]
        outcomes_comprehension = list(episodes_comprehension["correct"])
        if outcomes_comprehension.count(True) == 4:
            comprehension_consistency.loc[len(comprehension_consistency)] = [
                "3DS",
                model,
                stim_id,
                True,
            ]
        else:
            comprehension_consistency.loc[len(comprehension_consistency)] = [
                "3DS",
                model,
                stim_id,
                False,
            ]

production_consistency.to_csv(
    "games/multimodal_referencegame/analysis/production_consistency.csv", index=False
)
comprehension_consistency.to_csv(
    "games/multimodal_referencegame/analysis/comprehension_consistency.csv", index=False
)
