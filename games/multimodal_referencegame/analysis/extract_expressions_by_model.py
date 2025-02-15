# -*-coding:utf-8 -*-
# Author: Eileen Kammel, 811770
# Date: 2025-02-10 16:36:58

import os
import pandas as pd
from make_info_table import load_raw_stimuli_info, image_loader
from analyze_expressions import analyze_expression
import json

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

TUNA_STIMULI_IDS = [
    642,
    580,
    965,
    454,
    9,
    588,
    975,
    719,
    784,
    593,
    977,
    55,
    1047,
    793,
    220,
    799,
    96,
    675,
    932,
    101,
    678,
    1060,
    164,
    878,
    307,
    244,
    501,
    567,
    123,
    127,
]  # List of stimuli ids for TUNA
THREEDS_STIMULI_IDS = [
    640,
    1856,
    453,
    2693,
    3014,
    3589,
    2761,
    1224,
    654,
    1559,
    3160,
    3544,
    3991,
    802,
    3367,
    1129,
    491,
    684,
    1389,
    686,
    2671,
    3762,
    3123,
    2482,
    2418,
    2999,
    3512,
    2682,
    1403,
    1276,
]


def extract_expressions_by_model():
    columns = [
        "set",
        "stim_id",
        "target",
        "D1",
        "D2",
        "D3",
        "model",
        "expression",
        "target_pos_P1",
        "target_pos_P2",
        "P2_choice",
        "status",
        "correct",
        "ID",
        "surplus_info"
    ]
    expressions = pd.DataFrame(columns=columns)
    programmatic = pd.DataFrame(columns=columns)
    for model in ALL_MODELS:
        path = f"results/{model}-t0.0--{model}-t0.0/multimodal_referencegame"
        if os.path.isdir(path):
            for experiment in os.listdir(path):
                if os.path.isdir(f"{path}/{experiment}"):
                    for episode in os.listdir(f"{path}/{experiment}"):
                        if os.path.isdir(f"{path}/{experiment}/{episode}"):
                            try:
                                with open(
                                    f"{path}/{experiment}/{episode}/interactions.json"
                                ) as f:
                                    data = json.load(f)
                                    with open(
                                        f"{path}/{experiment}/{episode}/instance.json"
                                    ) as g:
                                        instance = json.load(g)
                                        target_pos_P1 = instance[
                                            "player_1_target_position"
                                        ]
                                        target_pos_P2 = int(
                                            instance["target_image_name"][1]
                                        )
                                    stim_id, model_expression, status, p2_choice = (
                                        parse_log(data)
                                    )
                                    set = (
                                        "TUNA"
                                        if int(stim_id) in TUNA_STIMULI_IDS
                                        else "3DS"
                                    )
                                    with open(
                                        f"{path}/{experiment}/{episode}/scores.json"
                                    ) as h:
                                        scores = json.load(h)
                                        correct = determine_sucess(scores) if status == "completed" else None
                                    target, d1, d2, d3, id_type, minimal_expression = (
                                        load_raw_stimuli_info(set.lower(), stim_id)
                                    )
                                    id, surplus_info = analyze_expression(set.lower(), model_expression, stim_id)
                                    expressions.loc[len(expressions)] = [
                                        set,
                                        stim_id,
                                        target,
                                        d1,
                                        d2,
                                        d3,
                                        model,
                                        model_expression,
                                        target_pos_P1,
                                        target_pos_P2,
                                        p2_choice,
                                        status,
                                        correct,
                                        id,
                                        surplus_info,
                                    ]
                                    if status == "abort at P1":
                                        print(
                                            f"Unsuccessful because of P1: {path}/{experiment}/{episode}"
                                        )
                                    if status == "abort at P2":
                                        print(
                                            f"Unsuccessful because of P2: {path}/{experiment}/{episode}"
                                        )
                            except FileNotFoundError:
                                print(
                                    f"File not found: {path}/{experiment}/{episode}/interactions.json"
                                )
                                continue
        programmatic_path = f"results/programmatic-t0.0--{model}-t0.0/multimodal_referencegame"
        if os.path.isdir(programmatic_path):
            for experiment in os.listdir(programmatic_path):
                if os.path.isdir(f"{programmatic_path}/{experiment}"):
                    for episode in os.listdir(f"{programmatic_path}/{experiment}"):
                        if os.path.isdir(f"{programmatic_path}/{experiment}/{episode}"):
                            try:
                                with open(
                                    f"{programmatic_path}/{experiment}/{episode}/interactions.json"
                                ) as f:
                                    data = json.load(f)
                                    with open(
                                        f"{programmatic_path}/{experiment}/{episode}/instance.json"
                                    ) as g:
                                        instance = json.load(g)
                                        target_pos_P1 = instance[
                                            "player_1_target_position"
                                        ]
                                        target_pos_P2 = int(
                                            instance["target_image_name"][1]
                                        )
                                    stim_id, model_expression, status, p2_choice = (
                                        parse_log(data)
                                    )
                                    set = (
                                        "TUNA"
                                        if int(stim_id) in TUNA_STIMULI_IDS
                                        else "3DS"
                                    )
                                    with open(
                                        f"{programmatic_path}/{experiment}/{episode}/scores.json"
                                    ) as h:
                                        scores = json.load(h)
                                        correct = determine_sucess(scores) if status == "completed" else None
                                    target, d1, d2, d3, id_type, minimal_expression = (
                                        load_raw_stimuli_info(set.lower(), stim_id)
                                    )
                                    id, surplus_info = analyze_expression(set.lower(), model_expression, stim_id)
                                    programmatic.loc[len(programmatic)] = [
                                        set,
                                        stim_id,
                                        target,
                                        d1,
                                        d2,
                                        d3,
                                        model,
                                        model_expression,
                                        target_pos_P1,
                                        target_pos_P2,
                                        p2_choice,
                                        status,
                                        correct,
                                        id,
                                        surplus_info,
                                    ]
                                    if status == "abort at P1":
                                        print(
                                            f"Unsuccessful because of P1: {programmatic_path}/{experiment}/{episode}"
                                        )
                                    if status == "abort at P2":
                                        print(
                                            f"Unsuccessful because of P2: {programmatic_path}/{experiment}/{episode}"
                                        )
                            except FileNotFoundError:
                                print(
                                    f"File not found: {programmatic_path}/{experiment}/{episode}/interactions.json"
                                )
                                continue
    expressions.sort_values(by=["set", "model", "stim_id"], inplace=True)
    expressions.reset_index(drop=True, inplace=True)
    programmatic.sort_values(by=["set", "model", "stim_id"], inplace=True)
    programmatic.reset_index(drop=True, inplace=True)
    # only_1_stim_one_model = expressions[(expressions["stim_id"] == 101) & (expressions["model"] == "idefics-80b-instruct")]
    # print(only_1_stim_one_model)
    expressions.to_csv(
        "games/multimodal_referencegame/analysis/expressions_by_model.csv", index=False
    )
    programmatic.to_csv(
        "games/multimodal_referencegame/analysis/programmatic_expressions_by_model.csv", index=False
    )


def parse_log(log):
    stim_id = log["turns"][0][0]["action"]["content"]["stimuli_id"]
    if len(log["turns"][0]) < 6:
        status = "abort at P1"
        expression = log["turns"][0][2]["action"]["original_content"]
        p2_choice = None
    else:
        type = log["turns"][0][5]["action"]["type"]
        if type == "invalid format":
            status = "abort at P2"
            expression = log["turns"][0][2]["action"]["expression"]
            p2_choice = None
        elif type == "parse":
            status = "completed"
            expression = log["turns"][0][2]["action"]["expression"]
            p2_choice = log["turns"][0][5]["action"]["answer"]
    return stim_id, expression, status, p2_choice


def determine_sucess(log):
    return log["episode scores"]["Success"] == 1


def make_html(filename, output_name):
    expressions = pd.read_csv(filename)
    image_columns = ["target", "D1", "D2", "D3"]
    for col in image_columns:
        expressions[col] = expressions.apply(
            lambda row: image_loader(row, row[col]), axis=1
        )
    table_html = expressions.to_html(escape=False, index=False)
    with open(
        output_name, "w"
    ) as f:
        f.write(
            """
        <html>
        <head>
            <title>Image Table</title>
            <style>
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid black; padding: 8px; text-align: center; }
                img { max-height: 50px; }
            </style>
        </head>
        <body>
            <h2>Experiment Overview</h2>
            """
            + table_html
            + """
        </body>
        </html>"""
        )


if __name__ == "__main__":
    model_expressions = "games/multimodal_referencegame/analysis/expressions_by_model.csv"
    model_expressions_output = "games/multimodal_referencegame/analysis/model_expressions_overview.html"
    programmatic = "games/multimodal_referencegame/analysis/programmatic_expressions_by_model.csv"
    programmatic_output = "games/multimodal_referencegame/analysis/programmatic_expressions_overview.html"
    extract_expressions_by_model()
    make_html(programmatic, programmatic_output)
    make_html(model_expressions, model_expressions_output)
