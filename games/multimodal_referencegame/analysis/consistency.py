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

    consistent_episodes = {model: {"tuna": [], "threeds": []} for model in ALL_MODELS}

    for model in ALL_MODELS:
        model_df_production = production[production["model"] == model]
        model_df_production = model_df_production[model_df_production["status"] == "completed"]
        model_df_comprehension = comprehension[comprehension["model"] == model]
        model_df_comprehension = model_df_comprehension[model_df_comprehension["status"] == "completed"]

        prod_consistency_tuna = check_consistency(model_df_production, TUNA_STIMULI_IDS, "TUNA", "PROD")
        prod_consistency_threeds = check_consistency(model_df_production, THREEDS_STIMULI_IDS, "3DS", "PROD")
        comp_consistency_tuna = check_consistency(model_df_comprehension, TUNA_STIMULI_IDS, "TUNA", "COMP")
        comp_consistency_threeds = check_consistency(model_df_comprehension, THREEDS_STIMULI_IDS, "3DS", "COMP")

        production_consistency = pd.concat([production_consistency, prod_consistency_tuna, prod_consistency_threeds])
        comprehension_consistency = pd.concat([comprehension_consistency, comp_consistency_tuna, comp_consistency_threeds])

        consistent_episodes[model]["tuna"].extend(prod_consistency_tuna[prod_consistency_tuna["consistent"] == True]["stim_id"].tolist())
        consistent_episodes[model]["tuna"].extend(comp_consistency_tuna[comp_consistency_tuna["consistent"] == True]["stim_id"].tolist())
        consistent_episodes[model]["threeds"].extend(prod_consistency_threeds[prod_consistency_threeds["consistent"] == True]["stim_id"].tolist())
        consistent_episodes[model]["threeds"].extend(comp_consistency_threeds[comp_consistency_threeds["consistent"] == True]["stim_id"].tolist())

    production_consistency.to_csv(
        "games/multimodal_referencegame/analysis/production_consistency.csv", index=False
    )
    comprehension_consistency.to_csv(
        "games/multimodal_referencegame/analysis/comprehension_consistency.csv", index=False
    )

    print("Consistent Episodes:")
    for model, sets in consistent_episodes.items():
        print(f"Model: {model}")
        print(f"TUNA: {sets['tuna']}")
        print(f"3DS: {sets['threeds']}")
        print()

    for model_entry in consistent_episodes.items():
        for set in model_entry[1].items():
            for stim_id in set[1]:
                print(type(stim_id))
                stim_id = int(stim_id)
                print(type(stim_id))
            print(set)



def compute_consistency_score(consistency_df):
    consistent = consistency_df[consistency_df["consistent"] == True]
    return round((len(consistent) / len(consistency_df)) * 100, 2)


if __name__ == "__main__":
    analyze_consistency()
    data = pd.read_csv("games/multimodal_referencegame/analysis/comprehension_consistency.csv")
    consitent_data = data[data["consistent"] == True]
    consitent_data.to_csv("games/multimodal_referencegame/analysis/consistent_episodes_comprehension.csv", index=False)
