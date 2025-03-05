# -*-coding:utf-8 -*-
# Author: Eileen Kammel, 811770
# Date: 2025-03-03 13:02:20

import pandas as pd
from games.multimodal_referencegame.analysis.constants import ALL_MODELS, ALL_MODELS_ALIAS


def compare_accuracy(production, comprehension, consistent_comprehension):
    results = []

    for model in ALL_MODELS:
        model_alias = ALL_MODELS_ALIAS[model]
        model_production = production[production["model"] == model_alias]
        model_comprehension = comprehension[comprehension["model"] == model_alias]
        model_consistent_comprehension = consistent_comprehension[
            consistent_comprehension["model"] == model_alias
        ]

        if not model_production.empty:
            prod_accuracy_tuna = model_production.loc[
                model_production["set"] == "TUNA", "correct_percentage"
            ].values[0]
            prod_accuracy_3ds = model_production.loc[
                model_production["set"] == "3DS", "correct_percentage"
            ].values[0]
        else:
            prod_accuracy_tuna = None
            prod_accuracy_3ds = None

        if not model_comprehension.empty:
            comp_accuracy_tuna = model_comprehension.loc[
                model_comprehension["set"] == "TUNA", "correct_percentage"
            ].values[0]
            comp_accuracy_3ds = model_comprehension.loc[
                model_comprehension["set"] == "3DS", "correct_percentage"
            ].values[0]
        else:
            comp_accuracy_tuna = None
            comp_accuracy_3ds = None

        if not model_consistent_comprehension.empty:
            consistent_comp_accuracy_tuna = model_consistent_comprehension.loc[
                model_consistent_comprehension["set"] == "TUNA", "correct_percentage"
            ].values[0]
            consistent_comp_accuracy_3ds = model_consistent_comprehension.loc[
                model_consistent_comprehension["set"] == "3DS", "correct_percentage"
            ].values[0]
        else:
            consistent_comp_accuracy_tuna = None
            consistent_comp_accuracy_3ds = None

        comp_prod_diff_tuna = (
            comp_accuracy_tuna - prod_accuracy_tuna
            if comp_accuracy_tuna is not None and prod_accuracy_tuna is not None
            else None
        )
        comp_prod_diff_3ds = (
            comp_accuracy_3ds - prod_accuracy_3ds
            if comp_accuracy_3ds is not None and prod_accuracy_3ds is not None
            else None
        )
        comp_consistent_comp_diff_tuna = (
            consistent_comp_accuracy_tuna - comp_accuracy_tuna
            if consistent_comp_accuracy_tuna is not None and comp_accuracy_tuna is not None
            else None
        )
        comp_consistent_comp_diff_3ds = (
            consistent_comp_accuracy_3ds - comp_accuracy_3ds
            if consistent_comp_accuracy_3ds is not None and comp_accuracy_3ds is not None
            else None
        )
        prod_consistent_comp_diff_tuna = (
            consistent_comp_accuracy_tuna - prod_accuracy_tuna
            if consistent_comp_accuracy_tuna is not None and prod_accuracy_tuna is not None
            else None
        )
        prod_consistent_comp_diff_3ds = (
            consistent_comp_accuracy_3ds - prod_accuracy_3ds
            if consistent_comp_accuracy_3ds is not None and prod_accuracy_3ds is not None
            else None
        )

        # round to 2 decimal places
        prod_accuracy_tuna = (
            round(prod_accuracy_tuna, 2) if prod_accuracy_tuna is not None else None
        )
        prod_accuracy_3ds = (
            round(prod_accuracy_3ds, 2) if prod_accuracy_3ds is not None else None
        )
        comp_accuracy_tuna = (
            round(comp_accuracy_tuna, 2) if comp_accuracy_tuna is not None else None
        )
        comp_accuracy_3ds = (
            round(comp_accuracy_3ds, 2) if comp_accuracy_3ds is not None else None
        )
        consistent_comp_accuracy_tuna = (
            round(consistent_comp_accuracy_tuna, 2)
            if consistent_comp_accuracy_tuna is not None
            else None
        )
        consistent_comp_accuracy_3ds = (
            round(consistent_comp_accuracy_3ds, 2)
            if consistent_comp_accuracy_3ds is not None
            else None
        )
        comp_prod_diff_tuna = (
            round(comp_prod_diff_tuna, 2) if comp_prod_diff_tuna is not None else None
        )
        comp_prod_diff_3ds = (
            round(comp_prod_diff_3ds, 2) if comp_prod_diff_3ds is not None else None
        )
        comp_consistent_comp_diff_tuna = (
            round(comp_consistent_comp_diff_tuna, 2)
            if comp_consistent_comp_diff_tuna is not None
            else None
        )
        comp_consistent_comp_diff_3ds = (
            round(comp_consistent_comp_diff_3ds, 2)
            if comp_consistent_comp_diff_3ds is not None
            else None
        )
        prod_consistent_comp_diff_tuna = (
            round(prod_consistent_comp_diff_tuna, 2)
            if prod_consistent_comp_diff_tuna is not None
            else None
        )
        prod_consistent_comp_diff_3ds = (
            round(prod_consistent_comp_diff_3ds, 2)
            if prod_consistent_comp_diff_3ds is not None
            else None
        )

        print(f"{model_alias} TUNA")
        print(f"Production: {prod_accuracy_tuna}")
        print(f"Comprehension: {comp_accuracy_tuna}")
        print(f"Consistent Comprehension: {consistent_comp_accuracy_tuna}")
        print(f"Comprehension - Production: {comp_prod_diff_tuna}")
        print(
            f"Consistent Comprehension - Comprehension: {comp_consistent_comp_diff_tuna}"
        )
        print(
            f"Consistent Comprehension - Production: {prod_consistent_comp_diff_tuna}"
        )
        print()
        print(f"{model_alias} 3DS")
        print(f"Production: {prod_accuracy_3ds}")
        print(f"Comprehension: {comp_accuracy_3ds}")
        print(f"Consistent Comprehension: {consistent_comp_accuracy_3ds}")
        print(f"Comprehension - Production: {comp_prod_diff_3ds}")
        print(
            f"Consistent Comprehension - Comprehension: {comp_consistent_comp_diff_3ds}"
        )
        print(f"Consistent Comprehension - Production: {prod_consistent_comp_diff_3ds}")
        print()

        # Save results to list
        results.append({
            "model": model_alias,
            "set": "TUNA",
            "production_accuracy": prod_accuracy_tuna,
            "comprehension_accuracy": comp_accuracy_tuna,
            "consistent_comprehension_accuracy": consistent_comp_accuracy_tuna,
            "comprehension_production_diff": comp_prod_diff_tuna,
            "consistent_comprehension_comprehension_diff": comp_consistent_comp_diff_tuna,
            "consistent_comprehension_production_diff": prod_consistent_comp_diff_tuna
        })
        results.append({
            "model": model_alias,
            "set": "3DS",
            "production_accuracy": prod_accuracy_3ds,
            "comprehension_accuracy": comp_accuracy_3ds,
            "consistent_comprehension_accuracy": consistent_comp_accuracy_3ds,
            "comprehension_production_diff": comp_prod_diff_3ds,
            "consistent_comprehension_comprehension_diff": comp_consistent_comp_diff_3ds,
            "consistent_comprehension_production_diff": prod_consistent_comp_diff_3ds
        })

    # Save results to CSV
    results_df = pd.DataFrame(results)
    results_df.to_csv("games/multimodal_referencegame/analysis/compare_accuracy_results.csv", index=False)


if __name__ == "__main__":
    production = pd.read_csv(
        "games/multimodal_referencegame/analysis/plots/completion_correct_ratio_all_correct_percentages.csv"
    )

    comprehension = pd.read_csv(
        "games/multimodal_referencegame/analysis/plots/completion_correct_ratio_all_programmatic_correct_percentages.csv"
    )

    consistent_comprehension = pd.read_csv(
        "games/multimodal_referencegame/analysis/plots/consistent_completion_correct_ratio_all_correct_percentages.csv"
    )
    compare_accuracy(production, comprehension, consistent_comprehension)
