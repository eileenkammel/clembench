# -*-coding:utf-8 -*-
# Author: Eileen Kammel, 811770
# Date: 2025-02-13 13:29:42

# Compares the ground truth to the model Expressions by LLMs

import json
import pandas as pd
import spacy

OPEN_WEIGHED_MODELS = [
    "idefics-80b-instruct",
    "InternVL2-Llama3-76B",
    "InternVL2-40B",
    "InternVL2-8B",
]

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


def compare_to_gt():
    gt_comparison = pd.DataFrame(
        columns=["set", "model", "episode", "information_comparison", "len_comparison"]
    )
    model_expressions = pd.read_csv(
        "games/multimodal_referencegame/analysis/expressions_by_model.csv"
    )
    for model in OPEN_WEIGHED_MODELS:
        df_model = model_expressions[model_expressions["model"] == model]
        df_model_tuna = df_model[df_model["set"] == "TUNA"]
        df_model_threeds = df_model[df_model["set"] == "3DS"]
        for episode in TUNA_STIMULI_IDS:
            ground_truth = load_gt("tuna", episode, model)
            gt_information, gt_len = analyze_exp([ground_truth])
            df_model_tuna_episode = df_model_tuna[df_model_tuna["stim_id"] == episode]
            expressions = df_model_tuna_episode["expression"].tolist()
            information, total_len = analyze_exp(expressions)
            information_comparison = compare_information(gt_information, information)
            len_coparison = compare_len(gt_len, total_len)
            gt_comparison.loc[len(gt_comparison)] = [
                "TUNA",
                model,
                episode,
                information_comparison,
                len_coparison,
            ]
        for episode in THREEDS_STIMULI_IDS:
            ground_truth = load_gt("threeds", episode, model)
            gt_information, gt_len = analyze_exp([ground_truth])
            df_model_threeds_episode = df_model_threeds[
                df_model_threeds["stim_id"] == episode
            ]
            expressions = df_model_threeds_episode["expression"].tolist()
            information, total_len = analyze_exp(expressions)
            information_comparison = compare_information(gt_information, information)
            len_coparison = compare_len(gt_len, total_len)
            gt_comparison.loc[len(gt_comparison)] = [
                "3DS",
                model,
                episode,
                information_comparison,
                len_coparison,
            ]
    gt_comparison.to_csv("games/multimodal_referencegame/analysis/gt_comparison.csv")
    gt_comparison.to_html("games/multimodal_referencegame/analysis/gt_comparison.html")


def load_gt(set, stimuli_id, model):
    id_t_lookup = json.load(
        open("games/multimodal_referencegame/analysis/id_target_table.json")
    )
    target = id_t_lookup[set][str(stimuli_id)]
    gt = json.load(open("games/multimodal_referencegame/analysis/ground_truth.json"))
    return gt[model][set][target]


def analyze_exp(expression):
    tagger = spacy.load("en_core_web_sm")
    total_len = 0
    total_information = 0
    for exp in expression:
        exp = exp.lower()
        tagged_expression = tagger(exp)
        adjective_count = sum([1 for token in tagged_expression if token.pos_ == "ADJ"])
        noun_count = sum(
            [1 for token in tagged_expression if token.pos_ in {"NOUN", "PROPN"}]
        )
        total_len += len(exp.split())
        total_information += adjective_count + noun_count
    mean_information = total_information / len(expression)
    mean_len = total_len / len(expression)
    return mean_information, mean_len


def compare_information(gt, model):
    """Retruns the difference between
    the ground truth and the model expressions.
    If positive, gt has more information than model expression.
    If negative, model expression has more information than gt.
    """
    return gt - model


def compare_len(gt, model):
    """Returns the difference between the
    ground truth and the model expression lengths.
    If positive, gt is longer than model expression.
    If negative, model expression is longer than gt.
    """
    return gt - model


def get_means():
    df = pd.read_csv("games/multimodal_referencegame/analysis/gt_comparison.csv")
    for model in OPEN_WEIGHED_MODELS:
        df_model = df[df["model"] == model]
        df_model_tuna = df_model[df_model["set"] == "TUNA"]
        mean_info = df_model_tuna["information_comparison"].mean().round(2)
        mean_len = df_model_tuna["len_comparison"].mean().round(2)
        print(f"Model: {model}")
        print(f"Mean information difference TUNA: {mean_info}")
        print(f"Mean length difference TUNA: {mean_len}")
        df_model_threeds = df_model[df_model["set"] == "3DS"]
        mean_info = df_model_threeds["information_comparison"].mean().round(2)
        mean_len = df_model_threeds["len_comparison"].mean().round(2)
        print(f"Mean information difference 3DS: {mean_info}")
        print(f"Mean length difference 3DS: {mean_len}")




#compare_to_gt()
get_means()
