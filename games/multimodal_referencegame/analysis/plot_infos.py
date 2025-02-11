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

df = pd.read_csv("games/multimodal_referencegame/analysis/expressions_by_model.csv")


def autopct_format(pct):
    return f'{pct:.1f}%'


def plot_id_accuracy():

    fig, axs = plt.subplots(2, 2, figsize=(12, 12))  # Adjust the number of rows and columns as needed
    axs = axs.flatten()  # Flatten the array of axes for easy iteration

    for i, model in enumerate(OPEN_WEIGHED_MODELS):
        model_df = df[df["model"] == model]

        # count value "NO ID" in column "ID"
        no_id = model_df[model_df["ID"] == "NO ID"].count()["ID"]
        insuff_id = model_df[model_df["ID"] == "Insufficient ID"].count()["ID"]
        correct_id = model_df[model_df["ID"] == "Correct ID"].count()["ID"]

        # calculate percentages
        total = no_id + insuff_id + correct_id
        no_id_pct = no_id / total * 100
        insuff_id_pct = insuff_id / total * 100
        correct_id_pct = correct_id / total * 100

        # make donut chart with matplotlib
        labels = [f"NO ID\n{no_id_pct:.1f}%", f"Insufficient ID\n{insuff_id_pct:.1f}%", f"Correct ID\n{correct_id_pct:.1f}%"]
        colors = mpl.colormaps["PuBuGn"]([0.4, 0.7, 0.9])
        axs[i].pie([no_id, insuff_id, correct_id], labels=labels, colors=colors, wedgeprops=dict(width=0.3))
        axs[i].set_title(f"ID accuracy for {model}")

    plt.tight_layout()
    plt.show()
    # Save the figure as SVG
    fig.savefig("games/multimodal_referencegame/analysis/ID_accuracy_OW_models.svg", format='svg')
    # Save the figure as PNG
    fig.savefig("games/multimodal_referencegame/analysis/ID_accuracy_OW_models.png", format='png')

def plot_surplus_id():

    fig, axs = plt.subplots(2, 2, figsize=(12, 12))  # Adjust the number of rows and columns as needed
    axs = axs.flatten()  # Flatten the array of axes for easy iteration

    # show the surplus value distribution for each model as boxplot
    for i, model in enumerate(OPEN_WEIGHED_MODELS):
        model_df = df[df["model"] == model]

        # get surplus values
        surplus_values = model_df["surplus_info"]

        # make boxplot with matplotlib
        axs[i].boxplot(surplus_values, patch_artist=True, boxprops=dict(facecolor="skyblue"), whis=[0, 100])
        axs[i].set_title(f"Surplus information distribution for {model}")
        axs[i].set_ylabel("Surplus Information")

    plt.tight_layout()
    plt.show()
    # Save the figure as SVG
    fig.savefig("games/multimodal_referencegame/analysis/surplus_info_OW_models.svg", format='svg')
    # Save the figure as PNG
    fig.savefig("games/multimodal_referencegame/analysis/surplus_info_OW_models.png", format='png')

def plot_surplus_id_combined():

    fig, ax = plt.subplots(figsize=(12, 8))  # Create a single plot

    # Collect surplus values for each model
    surplus_data = []
    labels = []
    for model in OPEN_WEIGHED_MODELS:
        model_df = df[df["model"] == model]
        surplus_values = model_df["surplus_info"]
        surplus_data.append(surplus_values)
        labels.append(model)

    # Make combined boxplot with matplotlib
    ax.boxplot(surplus_data, patch_artist=True, boxprops=dict(facecolor="skyblue"), whis=[0, 100], vert=False)
    ax.set_title("Surplus information distribution for each model")
    ax.set_xlabel("Surplus Information")
    ax.set_yticklabels(labels)

    plt.tight_layout()
    plt.show()
    # Save the figure as SVG
    fig.savefig("games/multimodal_referencegame/analysis/surplus_info_combined.svg", format='svg')
    # Save the figure as PNG
    fig.savefig("games/multimodal_referencegame/analysis/surplus_info_combined.png", format='png')

#plot_surplus_id()
plot_surplus_id_combined()
