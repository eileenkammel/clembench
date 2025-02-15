# -*-coding:utf-8 -*-
# Author: Eileen Kammel, 811770
# Date: 2025-02-11 21:18:04


import pandas as pd
import json
import os
import matplotlib.pyplot as plt
import matplotlib as mpl

OPEN_WEIGHED_MODELS = [
    "idefics-80b-instruct",
    "InternVL2-Llama3-76B",
    "InternVL2-40B",
    "InternVL2-8B",
]

# load pandas dataframe from csv

human = pd.read_csv(
    "games/multimodal_referencegame/analysis/programmatic_expressions_by_model.csv"
)
df = pd.read_csv("games/multimodal_referencegame/analysis/expressions_by_model.csv")


def autopct_format(pct):
    return f"{pct:.1f}%"


def plot_id_accuracy():
    fig, axs = plt.subplots(
        len(OPEN_WEIGHED_MODELS), 2, figsize=(12, 24)
    )  # Create a subplot for each model
    colors_tuna = mpl.colormaps["YlOrBr"]([0.6, 0.9])
    colors_3ds = mpl.colormaps["PuBuGn"]([0.4, 0.7])

    df_tuna = df[df["set"] == "TUNA"]
    df_3ds = df[df["set"] == "3DS"]

    for i, model in enumerate(OPEN_WEIGHED_MODELS):
        model_df_tuna = df_tuna[df_tuna["model"] == model]
        model_df_3ds = df_3ds[df_3ds["model"] == model]

        # count value "NO ID" in column "ID" for TUNA
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

        # make donut chart with matplotlib for TUNA
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

        # count value "NO ID" in column "ID" for 3DS
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

        # make donut chart with matplotlib for 3DS
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
    # Save the figure as SVG
    fig.savefig(
        "games/multimodal_referencegame/analysis/plots/ID_accuracy_humans.svg",
        format="svg",
    )
    # Save the figure as PNG
    fig.savefig(
        "games/multimodal_referencegame/analysis/plots/ID_accuracy_OW_humans.png",
        format="png",
    )


def plot_id_accuracy_bar_chart():
    no_id_percentages_tuna = []
    insuff_id_percentages_tuna = []
    correct_id_percentages_tuna = []
    no_id_percentages_3ds = []
    insuff_id_percentages_3ds = []
    correct_id_percentages_3ds = []
    labels = []
    df_tuna = df[df["set"] == "TUNA"]
    df_3ds = df[df["set"] == "3DS"]
    for model in OPEN_WEIGHED_MODELS:
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

    y = range(len(OPEN_WEIGHED_MODELS))
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
    # Save the figure as SVG
    fig.savefig(
        "games/multimodal_referencegame/analysis/plots/ID_accuracy_humans_bar_chart_horizontal.svg",
        format="svg",
    )
    # Save the figure as PNG
    fig.savefig(
        "games/multimodal_referencegame/analysis/plots/ID_accuracy_humans_bar_chart_horizontal.png",
        format="png",
    )


def plot_surplus_id_combined():
    fig, ax = plt.subplots(figsize=(12, 8))  # Create a single plot

    # Collect surplus values for each model and set
    surplus_data_tuna = []
    surplus_data_3ds = []
    labels = []
    colors2 = mpl.colormaps["PuBuGn"]([0.4, 0.7, 0.9])
    colors = mpl.colormaps["YlOrBr"]([0.6, 0.7, 0.9])
    df_tuna = df[df["set"] == "TUNA"]
    df_3ds = df[df["set"] == "3DS"]
    human_tuna = human[(human["set"] == "TUNA") & (human["model"] == "InternVL2-8B")]
    human_3ds = human[(human["set"] == "3DS") & (human["model"] == "InternVL2-8B")]

    for model in OPEN_WEIGHED_MODELS:
        model_df_tuna = df_tuna[df_tuna["model"] == model]
        model_df_3ds = df_3ds[df_3ds["model"] == model]

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

    positions_tuna = [i * 2 for i in range(len(OPEN_WEIGHED_MODELS) + 1)]
    positions_3ds = [i * 2 + 1 for i in range(len(OPEN_WEIGHED_MODELS) + 1)]

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
    ax.set_yticks([i * 2 + 0.5 for i in range(len(OPEN_WEIGHED_MODELS) + 1)])
    ax.set_yticklabels(labels)

    # Add legend
    handles = [
        plt.Line2D([0], [0], color=colors[0], lw=4, label="TUNA"),
        plt.Line2D([0], [0], color=colors2[0], lw=4, label="3DS"),
    ]
    legend = ax.legend(handles=handles)
    legend.get_frame().set_alpha(0.5)  # Set the transparency of the legend background

    plt.tight_layout()
    plt.show()
    # Save the figure as SVG
    fig.savefig(
        "games/multimodal_referencegame/analysis/plots/surplus_info_humans_combined.svg",
        format="svg",
    )
    # Save the figure as PNG
    fig.savefig(
        "games/multimodal_referencegame/analysis/plots/surplus_info_humans_combined.png",
        format="png",
    )


def plot_complete_correct_ratio():
    completion_percentages_tuna = []
    correct_percentages_tuna = []
    completion_percentages_3ds = []
    correct_percentages_3ds = []
    labels = []
    df_tuna = df[df["set"] == "TUNA"]
    df_3ds = df[df["set"] == "3DS"]
    for model in OPEN_WEIGHED_MODELS:
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
        labels.append(model)

        # Print the ratio of correct for each data set and model
        print(f"Model: {model}")
        print(
            f"TUNA - Total: {total_tuna}, Correct: {correct_vals_tuna}, Ratio: {correct_pct_tuna:.2f}%"
        )
        print(
            f"3DS - Total: {total_3ds}, Correct: {correct_vals_3ds}, Ratio: {correct_pct_3ds:.2f}%"
        )
        print()

    x = range(len(OPEN_WEIGHED_MODELS))
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

    ax.set_xlabel("Models")
    ax.set_ylabel("% of Games Played")
    # ax.set_title('Referent Identification with LLM made REs')
    ax.set_title("Referent Identification with Human made REs")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=0, ha="center")
    legend = ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=2)
    legend.get_frame().set_alpha(0.5)  # Set the transparency of the legend background

    plt.tight_layout()
    plt.show()
    # Save the figure as SVG
    # fig.savefig("games/multimodal_referencegame/analysis/plots/completion_correct_ratio.svg", format='svg')
    # Save the figure as PNG
    # fig.savefig("games/multimodal_referencegame/analysis/plots/completion_correct_ratio.png", format='png')
    # Save the figure as SVG
    fig.savefig(
        "games/multimodal_referencegame/analysis/plots/completion_correct_ratio_programmatic.svg",
        format="svg",
    )
    # Save the figure as PNG
    fig.savefig(
        "games/multimodal_referencegame/analysis/plots/completion_correct_ratio_programmatic.png",
        format="png",
    )


# plot_complete_correct_ratio()

# plot gt comparison
plot_surplus_id_combined()
