# -*-coding:utf-8 -*-
# Author: Eileen Kammel, 811770
# Date: 2025-01-14 16:57:21

import pandas as pd
import json
import base64
import os
from PIL import Image
import html

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
]  # List of stimuli ids for 3DS

# Load data
header = [
    "set",
    "stimuli_id",
    "target",
    "D1",
    "D2",
    "D3",
    "id_type",
    "minimal_expression",
    "ground_truth",
    "human_expression",
    "model_expressions",
]


def load_raw_stimuli_info(data_set_name, stimuli_id):
    """Will return t, D1-D3, id_type, (minimal expression)"""
    if data_set_name == "tuna":
        with open(
            "games/multimodal_referencegame/prep/tuna/tuna_3_distractor_stimuli.json",
            "r",
        ) as f:
            data = json.load(f)
            all_stimuli = (
                data["INSTANCES"]["one_attibute_id"]
                + data["INSTANCES"]["two_attibute_id"]
                + data["INSTANCES"]["three_attibute_id"]
            )
            for stimuli in all_stimuli:
                if stimuli["stimuli_id"] == stimuli_id:
                    return (
                        stimuli["target"],
                        stimuli["distractor1"],
                        stimuli["distractor2"],
                        stimuli["distractor3"],
                        stimuli["id_type"],
                        stimuli["id_attributes"],
                    )
    if data_set_name == "3ds":
        with open(
            "games/multimodal_referencegame/prep/3DS/3ds_3_distractor_instances.json",
            "r",
        ) as f:
            data = json.load(f)
            all_stimuli = (
                data["INSTANCES"]["one_attibute_id"]
                + data["INSTANCES"]["two_attibute_id"]
                + data["INSTANCES"]["three_attibute_id"]
            )
            for stimuli in all_stimuli:
                if stimuli["stimuli_id"] == stimuli_id:
                    return (
                        stimuli["target"],
                        stimuli["distractor1"],
                        stimuli["distractor2"],
                        stimuli["distractor3"],
                        stimuli["id_type"],
                        stimuli["id_attributes"],
                    )


def load_ground_truth(data_set_name, target):
    """Will return ground_truth"""
    with open("games/multimodal_referencegame/analysis/ground_truth.json", "r") as f:
        ground_truth = json.load(f)
    if data_set_name == "tuna":
        try:
            return ground_truth["tuna"][target]
        except KeyError:
            return None
    if data_set_name == "3ds":
        try:
            return ground_truth["3ds"][target]
        except KeyError:
            return None


def load_human_expression(data_set_name, stimuli_id):
    """Will return all human expressions from slurk_logs for a given stimuli_id.
    Different expressions will be separated by a $.
    """
    with open("games/multimodal_referencegame/analysis/selected_he.json", "r") as f:
        all_human_expressions = json.load(f)
    expressions = ""
    if data_set_name == "tuna":
        for game in all_human_expressions["tuna"]:
            if game["stimuli_id"] == stimuli_id:
                expressions += "$" + game["human_expression"]
        for game in all_human_expressions["mixed"]:
            if game["stimuli_id"] == stimuli_id:
                expressions += "$" + game["human_expression"]
    if data_set_name == "3ds":
        for game in all_human_expressions["3ds"]:
            if game["stimuli_id"] == stimuli_id:
                expressions += "$" + game["human_expression"]
        for game in all_human_expressions["mixed"]:
            if game["stimuli_id"] == stimuli_id:
                expressions += "$" + game["human_expression"]
    return expressions.strip("$")


def load_model_expressions(data_set_name, stimuli_id):
    model_expressions = json.load(
        open("games/multimodal_referencegame/analysis/all_model_expressions.json")
    )
    if data_set_name == "tuna":
        try:
            return model_expressions["tuna"][str(stimuli_id)]
        except KeyError:
            return None
    if data_set_name == "3ds":
        try:
            return model_expressions["threeds"][str(stimuli_id)]
        except KeyError:
            return None


def write_info_table():
    tuna_data = pd.DataFrame(columns=header)
    three_ds_data = pd.DataFrame(columns=header)
    for id in TUNA_STIMULI_IDS:
        t, D1, D2, D3, id_type, minimal_expression = load_raw_stimuli_info("tuna", id)
        ground_truth = load_ground_truth("tuna", t)
        human_expression = load_human_expression("tuna", id)
        model_expressions = load_model_expressions("tuna", id)
        tuna_data.loc[len(tuna_data)] = [
            "tuna",
            id,
            t,
            D1,
            D2,
            D3,
            id_type,
            minimal_expression,
            ground_truth,
            human_expression,
            model_expressions,
        ]
    for id in THREEDS_STIMULI_IDS:
        t, D1, D2, D3, id_type, minimal_expression = load_raw_stimuli_info("3ds", id)
        ground_truth = load_ground_truth("3ds", t)
        human_expression = load_human_expression("3ds", id)
        model_expressions = load_model_expressions("3ds", id)
        three_ds_data.loc[len(three_ds_data)] = [
            "3ds",
            id,
            t,
            D1,
            D2,
            D3,
            id_type,
            minimal_expression,
            ground_truth,
            human_expression,
            model_expressions,
        ]
    complete_data = pd.concat([tuna_data, three_ds_data])

    tuna_data.to_csv(
        "games/multimodal_referencegame/analysis/tuna_info_table.csv", index=False
    )
    three_ds_data.to_csv(
        "games/multimodal_referencegame/analysis/three_ds_info_table.csv", index=False
    )
    complete_data.to_csv(
        "games/multimodal_referencegame/analysis/info_table.csv", index=False
    )


def make_html_table():
    info_table = pd.read_csv("games/multimodal_referencegame/analysis/info_table.csv")
    print(info_table)
    image_columns = ["target", "D1", "D2", "D3"]
    description_column = "human_expression"
    for col in image_columns:
        info_table[col] = info_table.apply(
            lambda row: image_loader(row, row[col]), axis=1
        )
    info_table[description_column] = info_table[description_column].str.replace(
        "ü", "&uuml;"
    )
    info_table[description_column] = info_table[description_column].str.replace(
        "ä", "&auml;"
    )
    info_table[description_column] = info_table[description_column].str.replace(
        "ö", "&ouml;"
    )
    info_table[description_column] = info_table[description_column].str.replace(
        "ß", "&szlig;"
    )

    table_html = info_table.to_html(escape=False, index=False)
    with open(
        "games/multimodal_referencegame/analysis/experiment_overview.html", "w"
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


def image_loader(row, filename):
    small_image = (254, 254)
    large_size = 50
    small_size = 30
    if pd.notna(filename):
        base_path = (
            "games/multimodal_referencegame/resources/tuna_images/"
            if row["set"] == "tuna"
            else "games/multimodal_referencegame/resources/3ds_images/"
        )
        image_path = os.path.join(base_path, filename)
        try:
            with open(image_path, "rb") as img_file:
                encoded_string = base64.b64encode(img_file.read()).decode("utf-8")
            with Image.open(image_path) as img:
                width, height = img.size
                display_width = (
                    small_size
                    if width <= small_image[0] and height <= small_image[1]
                    else large_size
                )
            return f'<img src="data:image/png;base64,{encoded_string}" alt="{filename}" width="{display_width}">'
        except FileNotFoundError:
            return filename + " not found"
    return ""


if __name__ == "__main__":
    write_info_table()
    make_html_table()
