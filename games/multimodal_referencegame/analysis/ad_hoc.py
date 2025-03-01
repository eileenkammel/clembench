import pandas as pd
import json
from games.multimodal_referencegame.analysis.constants import (
    COMMERCIAL_MODELS,
    OPEN_WEIGHED_MODELS,
    ALL_MODELS,
    COMMERCIAL_MODELS_ALIAS,
    OPEN_WEIGHED_MODELS_ALIAS,
    ALL_MODELS_ALIAS,
    TUNA_STIMULI_IDS,
    THREEDS_STIMULI_IDS,
    ALL_IDS,
)


human_commercial = pd.read_csv(
    "games/multimodal_referencegame/analysis/commercial_expressions_by_model_programmatic.csv"
)
human_ow = pd.read_csv(
    "games/multimodal_referencegame/analysis/expressions_by_model_programmatic.csv"
)
df_commercial = pd.read_csv("games/multimodal_referencegame/analysis/commercial_expressions_by_model.csv")
df_ow = pd.read_csv("games/multimodal_referencegame/analysis/expressions_by_model.csv")

# for each model and for each setting, compute percentage of games completed

def compute_completion_rate(df):
    completion_rate = {}
    for model in ALL_MODELS:
        model_df = df[df["model"] == model]
        completion_rate[model] = round((len(model_df[model_df["status"] == "completed"]) / len(model_df)) *100, 2)
    return completion_rate


# for each model count if abort at player 1 or player 2
def count_abort(data):
    for model in ALL_MODELS:
        model_df = data[data["model"] == model]
        abort = model_df["status"].value_counts()
        print(model)
        print(abort)

print("Production")
print(compute_completion_rate(pd.concat([df_commercial, df_ow])))
print("Comprehension")
print(compute_completion_rate(pd.concat([human_commercial, human_ow])))

print("Production")
count_abort(pd.concat([df_commercial, df_ow]))
print("Comprehension")
count_abort(pd.concat([human_commercial, human_ow]))