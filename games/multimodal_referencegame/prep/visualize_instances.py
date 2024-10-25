# -*-coding:utf-8 -*-
# Author: Eileen Kammel, 811770
# Date: 2024-10-23 15:37:48

# Make HTML file of all experiment episodes
# Add all 4 pictures + id_type
import os
import json
import csv
import pandas as pd
from bs4 import BeautifulSoup
import base64


def get_id_type_name(set_name, id):
    tuna_stimuli = json.load(
        open("games/multimodal_referencegame/prep/tuna/tuna_3_distractor_stimuli.json")
    )
    threeds_stimuli = json.load(
        open("games/multimodal_referencegame/prep/3DS/3ds_3_distractor_instances.json")
    )
    stimuli = tuna_stimuli if set_name == "tuna" else threeds_stimuli
    for experiment in stimuli["INSTANCES"]:
        for stimulus in stimuli["INSTANCES"][experiment]:
            if stimulus["stimuli_id"] == id:
                type = stimulus["id_type"]
                attributes = stimulus["id_attributes"]
                return type, attributes


def visualize_instances():
    # load my instances
    instances = json.load(
        open("games/multimodal_referencegame/in/my_instances_3distractors.json")
    )
    csv_header = ["Target", "D1", "D2", "D3", "id_type", "id_attributes"]
    csv_data = []

    for experiment in instances["experiments"]:

        experiment_name = "tuna" if "TUNA" in experiment["name"] else "threeds"

        for episode in experiment["game_instances"]:

            stimuli_id = episode["stimuli_id"]

            if episode["player_1_target_position"] == 1:
                target = episode["player_1_first_image"]
                d1 = episode["player_1_second_image"]
                d2 = episode["player_1_third_image"]
                d3 = episode["player_1_fourth_image"]
            elif episode["player_1_target_position"] == 2:
                d1 = episode["player_1_first_image"]
                target = episode["player_1_second_image"]
                d2 = episode["player_1_third_image"]
                d3 = episode["player_1_fourth_image"]
            elif episode["player_1_target_position"] == 3:
                d1 = episode["player_1_first_image"]
                d2 = episode["player_1_second_image"]
                target = episode["player_1_third_image"]
                d3 = episode["player_1_fourth_image"]
            elif episode["player_1_target_position"] == 4:
                d1 = episode["player_1_first_image"]
                d2 = episode["player_1_second_image"]
                d3 = episode["player_1_third_image"]
                target = episode["player_1_fourth_image"]
            id_type, id_ttributes = get_id_type_name(experiment_name, stimuli_id)
            csv_data.append([target, d1, d2, d3, id_type, id_ttributes])
    with open("games/multimodal_referencegame/prep/instances.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(csv_header)
        writer.writerows(csv_data)


def create_html():
    instances_df = pd.read_csv("games/multimodal_referencegame/prep/instances.csv")
    instances_html = instances_df.to_html(index=False)

    with open("games/multimodal_referencegame/prep/instances.html", "w") as f:
        f.write(instances_html)
    print("HTML table generated")


def img_to_base64(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


def create_html_with_img():
    tuna_path = "/Users/eileen/Desktop/clembench/games/multimodal_referencegame/resources/tuna_images"
    threeds_path = "/Users/eileen/Desktop/clembench/games/multimodal_referencegame/resources/3ds_images"
    with open("games/multimodal_referencegame/prep/instances.html", "r") as f:
        soup = BeautifulSoup(f, "html.parser")
    table = soup.find("table")
    for cell in table.find_all("td"):
        cell_text = cell.get_text().strip()
        if "/" in cell_text:
            if "tuna" in cell_text:
                img_tag = soup.new_tag("img")
                img = os.path.basename(cell_text)
                img_path = os.path.join(tuna_path, img)
                img_base64 = img_to_base64(img_path)
                img_tag["src"] = f"data:image/png;base64,{img_base64}"
                cell.clear()
                cell.append(img_tag)
            elif "3ds" in cell_text:
                img_tag = soup.new_tag("img")
                img = os.path.basename(cell_text)
                img_path = os.path.join(threeds_path, img)
                img_base64 = img_to_base64(img_path)
                img_tag["src"] = f"data:image/png;base64,{img_base64}"
                cell.clear()
                cell.append(img_tag)
    with open("games/multimodal_referencegame/prep/instances_img.html", "w") as f:
        f.write(str(soup))
    print("HTML table with images generated")


if __name__ == "__main__":
    visualize_instances()
    create_html()
    create_html_with_img()
