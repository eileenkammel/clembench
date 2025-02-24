# -*-coding:utf-8 -*-
# Author: Eileen Kammel, 811770
# Date: 2025-02-20 15:07:21

import pandas as pd

COMMERCIAL_MODELS = [
    "gpt-4o-2024-08-06",
    "claude-3-5-sonnet-20240620",
    "gemini-2.0-flash-exp",
]

OPEN_WEIGHED_MODELS = [
    "idefics-80b-instruct",
    "InternVL2-Llama3-76B",
    "InternVL2-40B",
    "InternVL2-8B",
]

HUMAN_MOCK = ["programmatic"]

ALL_MODELS = COMMERCIAL_MODELS + OPEN_WEIGHED_MODELS

# Info needed for the table / per model:
# Model Name
# Games Completed
# Games correct
# Correct ID
# Insufficient ID
# No ID
# Mean surplus info


human_commercial = pd.read_csv(
    "games/multimodal_referencegame/analysis/commercial_expressions_by_model_programmatic.csv"
)
human_ow = pd.read_csv(
    "games/multimodal_referencegame/analysis/programmatic_expressions_by_model.csv"
)
df_commercial = pd.read_csv(
    "games/multimodal_referencegame/analysis/commercial_expressions_by_model.csv"
)
df_ow = pd.read_csv("games/multimodal_referencegame/analysis/expressions_by_model.csv")

header = [
    "Model Name",
    "% Games Completed",
    "% Games Completed TUNA",
    "% Games Completed 3DS",
    "% Games Correct",
    "% Games Correct TUNA",
    "% Games Correct 3DS",
    "% Correct ID",
    "% Correct ID TUNA",
    "% Correct ID 3DS",
    "% Insufficient ID",
    "% Insufficient ID TUNA",
    "% Insufficient ID 3DS",
    "% No ID",
    "% No ID TUNA",
    "% No ID 3DS",
    "Mean surplus info",
    "Mean surplus info TUNA",
    "Mean surplus info 3DS",
]

# Concat df_commercial and df_ow
df_production = pd.concat([df_commercial, df_ow])
df_comprehension = pd.concat([human_commercial, human_ow])


production_results = pd.DataFrame(columns=header)

for model in ALL_MODELS:
    model_df = df_production[df_production["model"] == model]
    tuna_df = model_df[model_df["set"] == "TUNA"]
    threeds_df = model_df[model_df["set"] == "3DS"]

    total_games = len(model_df)
    total_tuna = len(tuna_df)
    total_threeds = len(threeds_df)

    model_df = model_df[model_df["status"] == "completed"]
    tuna_df = tuna_df[tuna_df["status"] == "completed"]
    threeds_df = threeds_df[threeds_df["status"] == "completed"]

    games_completed = len(model_df)
    games_tuna_completed = len(tuna_df)
    games_threeds_completed = len(threeds_df)

    games_correct = len(model_df[model_df["correct"] == True])
    games_tuna_correct = len(tuna_df[tuna_df["correct"] == True])
    games_threeds_correct = len(threeds_df[threeds_df["correct"] == True])

    correct_id = len(model_df[model_df["ID"] == "Correct ID"])
    correct_id_tuna = len(tuna_df[tuna_df["ID"] == "Correct ID"])
    correct_id_threeds = len(threeds_df[threeds_df["ID"] == "Correct ID"])

    insufficient_id = len(model_df[model_df["ID"] == "Insufficient ID"])
    insufficient_id_tuna = len(tuna_df[tuna_df["ID"] == "Insufficient ID"])
    insufficient_id_threeds = len(threeds_df[threeds_df["ID"] == "Insufficient ID"])

    no_id = len(model_df[model_df["ID"] == "NO ID"])
    no_id_tuna = len(tuna_df[tuna_df["ID"] == "NO ID"])
    no_id_threeds = len(threeds_df[threeds_df["ID"] == "NO ID"])

    mean_surplus_info = model_df["surplus_info"].mean().round(2)
    mean_surplus_info_tuna = tuna_df["surplus_info"].mean().round(2)
    mean_surplus_info_threeds = threeds_df["surplus_info"].mean().round(2)

    percentage_games_completed = round((games_completed / total_games) * 100, 2)
    percentage_games_completed_tuna = round((games_tuna_completed / total_tuna) * 100, 2)
    percentage_games_completed_threeds = round(
        (games_threeds_completed / total_threeds) * 100, 2
    )

    percentage_games_correct = round((games_correct / games_completed) * 100, 2)
    percentage_games_correct_tuna = round((games_tuna_correct / games_tuna_completed) * 100, 2)
    percentage_games_correct_threeds = round(
        (games_threeds_correct / games_threeds_completed) * 100, 2
    )

    percentage_correct_id = round((correct_id / games_completed) * 100, 2)
    percentage_correct_id_tuna = round((correct_id_tuna / games_tuna_completed) * 100, 2)
    percentage_correct_id_threeds = round(
        (correct_id_threeds / games_threeds_completed) * 100
    )

    percentage_insufficient_id = round((insufficient_id / games_completed) * 100, 2)
    percentage_insufficient_id_tuna = round(
        (insufficient_id_tuna / games_tuna_completed) * 100, 2
    )
    percentage_insufficient_id_threeds = round(
        (insufficient_id_threeds / games_threeds_completed) * 100, 2
    )

    percentage_no_id = round((no_id / games_completed) * 100, 2)
    percentage_no_id_tuna = round((no_id_tuna / games_tuna_completed) * 100, 2)
    percentage_no_id_threeds = round((no_id_threeds / games_threeds_completed) * 100, 2)

    production_results.loc[len(production_results)] = [
        model,
        percentage_games_completed,
        percentage_games_completed_tuna,
        percentage_games_completed_threeds,
        percentage_games_correct,
        percentage_games_correct_tuna,
        percentage_games_correct_threeds,
        percentage_correct_id,
        percentage_correct_id_tuna,
        percentage_correct_id_threeds,
        percentage_insufficient_id,
        percentage_insufficient_id_tuna,
        percentage_insufficient_id_threeds,
        percentage_no_id,
        percentage_no_id_tuna,
        percentage_no_id_threeds,
        mean_surplus_info,
        mean_surplus_info_tuna,
        mean_surplus_info_threeds,
    ]

# save as csv
production_results.to_csv(
    "games/multimodal_referencegame/analysis/production_results.csv", index=False
)

comprehension_header = [
    "Model Name",
    "% Games Completed",
    "% Games Completed TUNA",
    "% Games Completed 3DS",
    "% Games Correct",
    "% Games Correct TUNA",
    "% Games Correct 3DS",
]

comprehension_results = pd.DataFrame(columns=comprehension_header)

for model in ALL_MODELS:
    model_df = df_production[df_production["model"] == model]
    tuna_df = model_df[model_df["set"] == "TUNA"]
    threeds_df = model_df[model_df["set"] == "3DS"]

    total_games = len(model_df)
    total_tuna = len(tuna_df)
    total_threeds = len(threeds_df)

    model_df = model_df[model_df["status"] == "completed"]
    tuna_df = tuna_df[tuna_df["status"] == "completed"]
    threeds_df = threeds_df[threeds_df["status"] == "completed"]

    games_completed = len(model_df)
    games_tuna_completed = len(tuna_df)
    games_threeds_completed = len(threeds_df)

    games_correct = len(model_df[model_df["correct"] == True])
    games_tuna_correct = len(tuna_df[tuna_df["correct"] == True])
    games_threeds_correct = len(threeds_df[threeds_df["correct"] == True])

    percentage_games_completed = round((games_completed / total_games) * 100, 2)
    percentage_games_completed_tuna = round((games_tuna_completed / total_tuna) * 100, 2)
    percentage_games_completed_threeds = round(
        (games_threeds_completed / total_threeds) * 100, 2
    )

    percentage_games_correct = round((games_correct / games_completed) * 100, 2)
    percentage_games_correct_tuna = round((games_tuna_correct / games_tuna_completed) * 100, 2)
    percentage_games_correct_threeds = round(
        (games_threeds_correct / games_threeds_completed) * 100, 2
    )

    comprehension_results.loc[len(comprehension_results)] = [
        model,
        percentage_games_completed,
        percentage_games_completed_tuna,
        percentage_games_completed_threeds,
        percentage_games_correct,
        percentage_games_correct_tuna,
        percentage_games_correct_threeds
    ]

# save as csv
comprehension_results.to_csv(
    "games/multimodal_referencegame/analysis/comprehension_results.csv", index=False
)