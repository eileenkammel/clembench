# -*-coding:utf-8 -*-
# Author: Eileen Kammel, 811770
# Date: 2025-02-11 21:18:04


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from games.multimodal_referencegame.analysis.constants import (
    ALL_MODELS,
    COMMERCIAL_MODELS,
    OPEN_WEIGHED_MODELS,
    COMMERCIAL_MODELS_ALIAS,
    OPEN_WEIGHED_MODELS_ALIAS,
    ALL_MODELS_ALIAS
)


def autopct_format(pct):
    return f"{pct:.1f}%"


def plot_id_accuracy(models, df, output_path):
    fig, axs = plt.subplots(
        len(models), 2, figsize=(12, 24)
    )
    colors_tuna = mpl.colormaps["YlOrBr"]([0.6, 0.9])
    colors_3ds = mpl.colormaps["PuBuGn"]([0.4, 0.7])

    df_tuna = df[df["set"] == "TUNA"]
    df_3ds = df[df["set"] == "3DS"]

    for i, model in enumerate(models):
        model_df_tuna = df_tuna[df_tuna["model"] == model]
        model_df_3ds = df_3ds[df_3ds["model"] == model]


        no_id_tuna = model_df_tuna[model_df_tuna["ID"] == "NO ID"].count()["ID"]
        insuff_id_tuna = model_df_tuna[
            model_df_tuna["ID"] == "Insufficient ID"
        ].count()["ID"]
        correct_id_tuna = model_df_tuna[model_df_tuna["ID"] == "Correct ID"].count()[
            "ID"
        ]


        total_tuna = no_id_tuna + insuff_id_tuna + correct_id_tuna
        no_id_pct_tuna = no_id_tuna / total_tuna * 100
        insuff_id_pct_tuna = insuff_id_tuna / total_tuna * 100
        correct_id_pct_tuna = correct_id_tuna / total_tuna * 100


        labels_tuna = [
            f"NO ID\n{no_id_pct_tuna:.1f}%",
            f"Insufficient ID\n{insuff_id_pct_tuna:.1f}%",
            f"Correct ID\n{correct_id_pct_tuna:.1f}%",
        ]
        wedges, texts, autotexts = axs[i, 0].pie(
            [no_id_tuna, insuff_id_tuna, correct_id_tuna],
            colors=colors_tuna,
            wedgeprops=dict(width=0.3),
            startangle=90,
            radius=1,
            autopct=autopct_format,
        )
        for text in texts + autotexts:
            text.set_fontsize(10)
            text.set_color("black")
        axs[i, 0].set_title(f"ID accuracy for {model} (TUNA)")

        no_id_3ds = model_df_3ds[model_df_3ds["ID"] == "NO ID"].count()["ID"]
        insuff_id_3ds = model_df_3ds[model_df_3ds["ID"] == "Insufficient ID"].count()[
            "ID"
        ]
        correct_id_3ds = model_df_3ds[model_df_3ds["ID"] == "Correct ID"].count()["ID"]

        # calculate percentages for 3DS
        total_3ds = no_id_3ds + insuff_id_3ds + correct_id_3ds
        no_id_pct_3ds = no_id_3ds / total_3ds * 100
        insuff_id_pct_3ds = insuff_id_3ds / total_3ds * 100
        correct_id_pct_3ds = correct_id_3ds / total_3ds * 100


        labels_3ds = [
            f"NO ID\n{no_id_pct_3ds:.1f}%",
            f"Insufficient ID\n{insuff_id_pct_3ds:.1f}%",
            f"Correct ID\n{correct_id_pct_3ds:.1f}%",
        ]
        wedges, texts, autotexts = axs[i, 1].pie(
            [no_id_3ds, insuff_id_3ds, correct_id_3ds],
            colors=colors_3ds,
            wedgeprops=dict(width=0.3),
            startangle=90,
            radius=1,
            autopct=autopct_format,
        )
        for text in texts + autotexts:
            text.set_fontsize(10)
            text.set_color("black")
        axs[i, 1].set_title(f"ID accuracy for {model} (3DS)")

    plt.tight_layout()
    plt.show()

    fig.savefig(
        output_path + ".svg",
        format="svg",
    )

    fig.savefig(
        output_path + ".png",
        format="png",
    )


def plot_id_accuracy_bar_chart(models, df, output_path):
    no_id_percentages_tuna = []
    insuff_id_percentages_tuna = []
    correct_id_percentages_tuna = []
    no_id_percentages_3ds = []
    insuff_id_percentages_3ds = []
    correct_id_percentages_3ds = []
    labels = []
    df_tuna = df[df["set"] == "TUNA"]
    df_3ds = df[df["set"] == "3DS"]
    for model in models:
        model_df_tuna = df_tuna[df_tuna["model"] == model]
        model_df_3ds = df_3ds[df_3ds["model"] == model]

        # count values for TUNA
        no_id_tuna = model_df_tuna[model_df_tuna["ID"] == "NO ID"].count()["ID"]
        insuff_id_tuna = model_df_tuna[
            model_df_tuna["ID"] == "Insufficient ID"
        ].count()["ID"]
        correct_id_tuna = model_df_tuna[model_df_tuna["ID"] == "Correct ID"].count()[
            "ID"
        ]

        # calculate percentages for TUNA
        total_tuna = no_id_tuna + insuff_id_tuna + correct_id_tuna
        no_id_pct_tuna = no_id_tuna / total_tuna * 100
        insuff_id_pct_tuna = insuff_id_tuna / total_tuna * 100
        correct_id_pct_tuna = correct_id_tuna / total_tuna * 100

        no_id_percentages_tuna.append(no_id_pct_tuna)
        insuff_id_percentages_tuna.append(insuff_id_pct_tuna)
        correct_id_percentages_tuna.append(correct_id_pct_tuna)

        # count values for 3DS
        no_id_3ds = model_df_3ds[model_df_3ds["ID"] == "NO ID"].count()["ID"]
        insuff_id_3ds = model_df_3ds[model_df_3ds["ID"] == "Insufficient ID"].count()[
            "ID"
        ]
        correct_id_3ds = model_df_3ds[model_df_3ds["ID"] == "Correct ID"].count()["ID"]

        # calculate percentages for 3DS
        total_3ds = no_id_3ds + insuff_id_3ds + correct_id_3ds
        no_id_pct_3ds = no_id_3ds / total_3ds * 100
        insuff_id_pct_3ds = insuff_id_3ds / total_3ds * 100
        correct_id_pct_3ds = correct_id_3ds / total_3ds * 100

        no_id_percentages_3ds.append(no_id_pct_3ds)
        insuff_id_percentages_3ds.append(insuff_id_pct_3ds)
        correct_id_percentages_3ds.append(correct_id_pct_3ds)

        labels.append(model)

    y = range(len(models))
    colors = mpl.colormaps["YlOrBr"]([0.6, 0.7, 0.9])
    colors2 = mpl.colormaps["PuBuGn"]([0.4, 0.7, 0.9])

    fig, ax = plt.subplots(figsize=(12, 8))
    bar_height = 0.2
    space = 0.02

    bars1 = ax.barh(
        [p - bar_height - space for p in y],
        no_id_percentages_tuna,
        bar_height,
        label="NO ID (TUNA)",
        color=colors[0],
    )
    bars2 = ax.barh(
        [p - bar_height - space for p in y],
        insuff_id_percentages_tuna,
        bar_height,
        left=no_id_percentages_tuna,
        label="Insufficient ID (TUNA)",
        color=colors[1],
    )
    bars3 = ax.barh(
        [p - bar_height - space for p in y],
        correct_id_percentages_tuna,
        bar_height,
        left=[
            i + j for i, j in zip(no_id_percentages_tuna, insuff_id_percentages_tuna)
        ],
        label="Correct ID (TUNA)",
        color=colors[2],
    )

    bars4 = ax.barh(
        [p + bar_height + space for p in y],
        no_id_percentages_3ds,
        bar_height,
        label="NO ID (3DS)",
        color=colors2[0],
    )
    bars5 = ax.barh(
        [p + bar_height + space for p in y],
        insuff_id_percentages_3ds,
        bar_height,
        left=no_id_percentages_3ds,
        label="Insufficient ID (3DS)",
        color=colors2[1],
    )
    bars6 = ax.barh(
        [p + bar_height + space for p in y],
        correct_id_percentages_3ds,
        bar_height,
        left=[i + j for i, j in zip(no_id_percentages_3ds, insuff_id_percentages_3ds)],
        label="Correct ID (3DS)",
        color=colors2[2],
    )

    ax.set_ylabel("Models")
    ax.set_xlabel("Percentage")
    ax.set_title("ID Accuracy Percentages per Model")
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    legend = ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.0)
    legend.get_frame().set_alpha(0.5)  # Set the transparency of the legend background

    plt.tight_layout()
    plt.show()

    fig.savefig(
        output_path + ".svg",
        format="svg",
    )

    fig.savefig(
        output_path + ".png",
        format="png",
    )


def plot_surplus_id_combined(models_ow, models_commercial, df_ow, df_commercial, human, output_path):
    fig, ax = plt.subplots(figsize=(12, 8))


    surplus_data_tuna = []
    surplus_data_3ds = []
    labels = []
    colors2 = mpl.colormaps["PuBuGn"]([0.4, 0.7, 0.9])
    colors = mpl.colormaps["YlOrBr"]([0.6, 0.7, 0.9])
    
    df_tuna_ow = df_ow[df_ow["set"] == "TUNA"]
    df_3ds_ow = df_ow[df_ow["set"] == "3DS"]
    df_tuna_commercial = df_commercial[df_commercial["set"] == "TUNA"]
    df_3ds_commercial = df_commercial[df_commercial["set"] == "3DS"]
    
    # Choose just one model bc HE is the same 
    human_tuna = human[(human["set"] == "TUNA") & (human["model"] == models_commercial[0])]
    human_3ds = human[(human["set"] == "3DS") & (human["model"] == models_commercial[0])]

    for model in models_ow:
        model_df_tuna = df_tuna_ow[df_tuna_ow["model"] == model]
        model_df_3ds = df_3ds_ow[df_3ds_ow["model"] == model]

        surplus_values_tuna = model_df_tuna["surplus_info"]
        surplus_values_3ds = model_df_3ds["surplus_info"]

        surplus_data_tuna.append(surplus_values_tuna)
        surplus_data_3ds.append(surplus_values_3ds)
        labels.append(model)

    for model in models_commercial:
        model_df_tuna = df_tuna_commercial[df_tuna_commercial["model"] == model]
        model_df_3ds = df_3ds_commercial[df_3ds_commercial["model"] == model]

        surplus_values_tuna = model_df_tuna["surplus_info"]
        surplus_values_3ds = model_df_3ds["surplus_info"]

        surplus_data_tuna.append(surplus_values_tuna)
        surplus_data_3ds.append(surplus_values_3ds)
        labels.append(model)

    # Add human data
    surplus_data_tuna.append(human_tuna["surplus_info"])
    surplus_data_3ds.append(human_3ds["surplus_info"])
    labels.append("Human")

    # Make combined boxplot with matplotlib
    boxprops_tuna = dict(facecolor=colors[0], color=colors[2])
    boxprops_3ds = dict(facecolor=colors2[0], color=colors2[2])
    medianprops_tuna = dict(color=colors[2])
    medianprops_3ds = dict(color=colors2[2])
    whiskerprops_tuna = dict(color=colors[2])
    whiskerprops_3ds = dict(color=colors2[2])
    capprops_tuna = dict(color=colors[2])
    capprops_3ds = dict(color=colors2[2])
    flierprops_tuna = dict(markerfacecolor=colors[1], markeredgecolor=colors[1])
    flierprops_3ds = dict(markerfacecolor=colors2[1], markeredgecolor=colors2[1])

    positions_tuna = [i * 2 for i in range(len(models_ow) + len(models_commercial) + 1)]
    positions_3ds = [i * 2 + 1 for i in range(len(models_ow) + len(models_commercial) + 1)]

    ax.boxplot(
        surplus_data_tuna,
        positions=positions_tuna,
        patch_artist=True,
        boxprops=boxprops_tuna,
        medianprops=medianprops_tuna,
        whiskerprops=whiskerprops_tuna,
        capprops=capprops_tuna,
        flierprops=flierprops_tuna,
        whis=[0, 100],
        vert=False,
    )
    ax.boxplot(
        surplus_data_3ds,
        positions=positions_3ds,
        patch_artist=True,
        boxprops=boxprops_3ds,
        medianprops=medianprops_3ds,
        whiskerprops=whiskerprops_3ds,
        capprops=capprops_3ds,
        flierprops=flierprops_3ds,
        whis=[0, 100],
        vert=False,
    )

    ax.set_title("Surplus Information Distribution for Each Model + Human")
    ax.set_xlabel("Surplus Information (Number of ADJ+NOUN)")
    ax.set_yticks([i * 2 + 0.5 for i in range(len(models_ow) + len(models_commercial) + 1)])
    ax.set_yticklabels(labels)

    # Add legend
    handles = [
        plt.Line2D([0], [0], color=colors[0], lw=4, label="TUNA"),
        plt.Line2D([0], [0], color=colors2[0], lw=4, label="3DS"),
    ]
    legend = ax.legend(handles=handles)
    legend.get_frame().set_alpha(0.5)

    plt.tight_layout()
    plt.show()

    fig.savefig(
        output_path + ".svg",
        format="svg",
    )

    fig.savefig(
        output_path + ".png",
        format="png",
    )


def plot_complete_correct_ratio(models, df, model_alias, output_path, comprehension=False):
    completion_percentages_tuna = []
    correct_percentages_tuna = []
    completion_percentages_3ds = []
    correct_percentages_3ds = []
    labels = []
    df_tuna = df[df["set"] == "TUNA"]
    df_3ds = df[df["set"] == "3DS"]
    for model in models:
        model_df_tuna = df_tuna[df_tuna["model"] == model]
        model_df_3ds = df_3ds[df_3ds["model"] == model]
        total_tuna = model_df_tuna[model_df_tuna["status"] == "completed"].count()[
            "status"
        ]
        total_3ds = model_df_3ds[model_df_3ds["status"] == "completed"].count()[
            "status"
        ]
        correct_vals_tuna = model_df_tuna[model_df_tuna["correct"] == True].count()[
            "correct"
        ]
        correct_vals_3ds = model_df_3ds[model_df_3ds["correct"] == True].count()[
            "correct"
        ]

        completion_pct_tuna = total_tuna / total_tuna * 100
        completion_pct_3ds = total_3ds / total_3ds * 100
        correct_pct_tuna = (
            correct_vals_tuna / total_tuna * 100 if total_tuna > 0 else 0
        )  # Correct percentage out of completed
        correct_pct_3ds = (
            correct_vals_3ds / total_3ds * 100 if total_3ds > 0 else 0
        )  # Correct percentage out of completed
        completion_percentages_tuna.append(completion_pct_tuna)
        completion_percentages_3ds.append(completion_pct_3ds)
        correct_percentages_tuna.append(correct_pct_tuna)
        correct_percentages_3ds.append(correct_pct_3ds)
        labels.append(model_alias[model])

        # Print the ratio of correct for each data set and model to console
        print(f"Model: {model}")
        print(
            f"TUNA - Total: {total_tuna}, Correct: {correct_vals_tuna}, Ratio: {correct_pct_tuna:.2f}%"
        )
        print(
            f"3DS - Total: {total_3ds}, Correct: {correct_vals_3ds}, Ratio: {correct_pct_3ds:.2f}%"
        )
        print()
    # replace full model names with abbreviations in labels

    x = range(len(models))
    colors = mpl.colormaps["YlOrBr"]([0.6, 0.9])
    colors2 = mpl.colormaps["PuBuGn"]([0.4, 0.7])

    fig, ax = plt.subplots(figsize=(12, 8))
    bar_width = 0.35
    space = 0.05

    bars1 = ax.bar(
        [p - bar_width / 2 - space / 2 for p in x],
        completion_percentages_tuna,
        bar_width,
        label="Completed Games (TUNA)",
        color=colors[0],
    )
    bars2 = ax.bar(
        [p - bar_width / 2 - space / 2 for p in x],
        correct_percentages_tuna,
        bar_width,
        label="Correct Referent Id (TUNA)",
        color=colors[1],
    )
    bars3 = ax.bar(
        [p + bar_width / 2 + space / 2 for p in x],
        completion_percentages_3ds,
        bar_width,
        label="Completed Games (3DS)",
        color=colors2[0],
    )
    bars4 = ax.bar(
        [p + bar_width / 2 + space / 2 for p in x],
        correct_percentages_3ds,
        bar_width,
        label="Correct Referent Id (3DS)",
        color=colors2[1],
    )

    ax.axhline(y=25, color="r", linestyle="--", label="Chance Average")
    #    ax.text(0, 25, 'Chance', color='r', va='bottom')

    #ax.set_xlabel("Models")
    ax.set_ylabel("% of Games Played")
    title = "Referent Identification with Human made REs" if comprehension else "Referent Identification with LLM made REs"
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha="center")
    legend = ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.25), ncol=5)
    legend.get_frame().set_alpha(0.5)

    plt.tight_layout()
    plt.show()

    fig.savefig(
        output_path + ".svg",
        format="svg",
    )

    fig.savefig(
        output_path +  ".png",
        format="png",
    )


if __name__ == "__main__":
    human_commercial = pd.read_csv(
        "games/multimodal_referencegame/analysis/commercial_expressions_by_model_programmatic.csv"
    )
    human_ow = pd.read_csv(
        "games/multimodal_referencegame/analysis/expressions_by_model_programmatic.csv"
    )
    df_commercial = pd.read_csv("games/multimodal_referencegame/analysis/commercial_expressions_by_model.csv")
    df_ow = pd.read_csv("games/multimodal_referencegame/analysis/expressions_by_model.csv")

    # plot_id_accuracy(COMMERCIAL_MODELS, df_commercial, "games/multimodal_referencegame/analysis/plots/id_accuracy_commercial")
    # plot_id_accuracy_bar_chart(COMMERCIAL_MODELS, df_commercial, "games/multimodal_referencegame/analysis/plots/id_accuracy_bar_chart_commercial")

    # plot_id_accuracy(OPEN_WEIGHED_MODELS, df_ow, "games/multimodal_referencegame/analysis/plots/id_accuracy_ow")
    # plot_id_accuracy_bar_chart(OPEN_WEIGHED_MODELS, df_ow, "games/multimodal_referencegame/analysis/plots/id_accuracy_bar_chart_ow")

    # plot_surplus_id_combined(OPEN_WEIGHED_MODELS, COMMERCIAL_MODELS, df_ow, df_commercial, human_commercial, "games/multimodal_referencegame/analysis/plots/surplus_info_commercial")

    # plot_complete_correct_ratio(COMMERCIAL_MODELS, df_commercial, "games/multimodal_referencegame/analysis/plots/completion_correct_ratio_commercial")
    # plot_complete_correct_ratio(COMMERCIAL_MODELS, df_commercial, "games/multimodal_referencegame/analysis/plots/completion_correct_ratio_commercial_programmatic", comprehension=True)

    # plot_complete_correct_ratio(OPEN_WEIGHED_MODELS, df_ow, "games/multimodal_referencegame/analysis/plots/completion_correct_ratio_ow")
    # plot_complete_correct_ratio(OPEN_WEIGHED_MODELS, df_ow, "games/multimodal_referencegame/analysis/plots/completion_correct_ratio_ow_programmatic", comprehension=True)

    plot_complete_correct_ratio(ALL_MODELS, pd.concat([df_commercial, df_ow]), ALL_MODELS_ALIAS, "games/multimodal_referencegame/analysis/plots/completion_correct_ratio_all")
    plot_complete_correct_ratio(ALL_MODELS, pd.concat([human_commercial, human_ow]), ALL_MODELS_ALIAS, "games/multimodal_referencegame/analysis/plots/completion_correct_ratio_all_programmatic", comprehension=True)