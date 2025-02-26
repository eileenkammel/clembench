# -*-coding:utf-8 -*-
# Author: Eileen Kammel, 811770
# Date: 2025-02-26 17:55:01

# Check if answers are consistent
# for all 4 configurations

import pandas as pd
from games.multimodal_referencegame.analysis.constants import (
    ALL_MODELS,
    TUNA_STIMULI_IDS,
    THREEDS_STIMULI_IDS,
)


def load_data():
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

    return production, comprehension


def check_consistency(model_df, stim_ids, set_name, setting):
    consistency_df = pd.DataFrame(columns=["set", "model", "stim_id", "consistent"])
    model = model_df["model"].iloc[0]
    for stim_id in stim_ids:
        episodes = model_df[model_df["stim_id"] == stim_id]
        outcomes = list(episodes["correct"])
        consistent = outcomes.count(True) == 4
        consistency_df.loc[len(consistency_df)] = [set_name, model, stim_id, consistent]
    consistency_score = compute_consistency_score(consistency_df)
    print(f"{model} consistency score for {set_name} in {setting} setting: {consistency_score}%")

    return consistency_df


def analyze_consistency():
    production, comprehension = load_data()

    production_consistency = pd.DataFrame(columns=["set", "model", "stim_id", "consistent"])
    comprehension_consistency = pd.DataFrame(columns=["set", "model", "stim_id", "consistent"])

    for model in ALL_MODELS:
        model_df_production = production[production["model"] == model]
        model_df_production = model_df_production[model_df_production["status"] == "completed"]
        model_df_comprehension = comprehension[comprehension["model"] == model]
        model_df_comprehension = model_df_comprehension[model_df_comprehension["status"] == "completed"]

        production_consistency = pd.concat([production_consistency, check_consistency(model_df_production, TUNA_STIMULI_IDS, "TUNA", "PROD")])
        production_consistency = pd.concat([production_consistency, check_consistency(model_df_production, THREEDS_STIMULI_IDS, "3DS", "PROD")])


        comprehension_consistency = pd.concat([comprehension_consistency, check_consistency(model_df_comprehension, TUNA_STIMULI_IDS, "TUNA", "COMP")])
        comprehension_consistency = pd.concat([comprehension_consistency, check_consistency(model_df_comprehension, THREEDS_STIMULI_IDS, "3DS", "COMP")])

    production_consistency.to_csv(
        "games/multimodal_referencegame/analysis/production_consistency.csv", index=False
    )
    comprehension_consistency.to_csv(
        "games/multimodal_referencegame/analysis/comprehension_consistency.csv", index=False
    )


def compute_consistency_score(consistency_df):
    consistent = consistency_df[consistency_df["consistent"] == True]
    return round((len(consistent) / len(consistency_df)) *100, 2)


if __name__ == "__main__":
    analyze_consistency()
