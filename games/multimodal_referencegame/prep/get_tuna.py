# -*-coding:utf-8 -*-
# Author: Eileen Kammel, 811770
# Date: 2024-10-22 17:01:38

# Downloads and prepares the TUNA dataset for the multimodal reference game.

import os
import zipfile
import requests
import xmltodict
import json
import shutil


def download_tuna():
    url = "http://www.abdn.ac.uk/ncs/documents/corpus.zip"
    tuna = requests.get(url)
    tuna.raise_for_status()
    with open("corpus.zip", "wb") as f:
        f.write(tuna.content)
    with zipfile.ZipFile("corpus.zip", "r") as zip_ref:
        zip_ref.extractall("games/multimodal_referencegame/prep/tuna_original")
    os.remove("corpus.zip")
    print("TUNA corpus downloaded and unzipped.")


# Function to convert XML to JSON
def xml_to_json(xml_string):
    # Parse XML to a Python dictionary
    xml_dict = xmltodict.parse(xml_string)

    # Convert the dictionary to a JSON string
    json_string = json.dumps(xml_dict, indent=3)

    return json_string


# Convert all episodes in the furniture category to JSON
def convert_all_furniture(directory_sg, directory_pl):
    path = "games/multimodal_referencegame/prep/tuna/"
    if not os.path.exists(path):
        os.makedirs(path)

    for filename in os.listdir(directory_sg):
        if filename.endswith(".xml"):
            file_path = os.path.join(directory_sg, filename)
            with open(file_path, "r") as xml_file:
                xml_data = xml_file.read()

            json_data = xml_to_json(xml_data)
            output_name = filename[:-4] + (".json")
            with open(path + output_name, "w") as json_file:
                json_file.write(json_data)
    # Plural episodes
    for filename in os.listdir(directory_pl):
        if filename.endswith(".xml"):
            file_path = os.path.join(directory_pl, filename)
            with open(file_path, "r") as xml_file:
                xml_data = xml_file.read()

            json_data = xml_to_json(xml_data)
            output_name = filename[:-4] + (".json")
            with open(path + output_name, "w") as json_file:
                json_file.write(json_data)

    print("All XML converted to JSON successfully!")


# Extract all unique images and their attributes to a single json
def extract_imgs():
    # Create a directory for the extracted images
    path = "games/multimodal_referencegame/resources/tuna_images"
    if not os.path.exists(path):
        os.makedirs(path)
    old_img_path = (
        "games/multimodal_referencegame/prep/tuna_original/dist/images/furniture"
    )
    tuna_episodes_path = "games/multimodal_referencegame/prep/tuna"
    img_counter = 0
    imgs_seen = set()
    img = {"IMAGES": []}
    # go through all episodes and write unique images in file
    for filename in os.listdir(tuna_episodes_path):
        if filename.endswith(".json"):
            file_path = os.path.join(tuna_episodes_path, filename)
            with open(file_path, "r") as json_file:
                for entity in json.load(json_file)["TRIAL"]["DOMAIN"]["ENTITY"]:
                    img_id = entity["@ID"]
                    img_filename = entity["@IMAGE"]
                    img_path = os.path.join(old_img_path, img_filename)
                    # change filename to mask content
                    img_new_filename = f"{img_counter}.png"
                    # check if image is already seen
                    if img_id not in imgs_seen:
                        imgs_seen.add(img_id)
                        img_counter += 1
                        # replace filename
                        entity["@IMAGE"] = img_new_filename
                        img["IMAGES"].append(entity)
                        # copy image to new directory
                        if os.path.exists(img_path):
                            shutil.copy(img_path, os.path.join(path, img_new_filename))
            # delete file after reading
            os.remove(file_path)
    all_imgs = os.path.join(tuna_episodes_path, "all_imgs.json")
    with open(all_imgs, "w") as json_file:
        json.dump(img, json_file, indent=4)


# Convert attribute structure for images
# TODO incorporate in extract function


def change_tuna_attribute_struct(all_img_json_path):
    with open(all_img_json_path, "r+") as file:
        data = json.load(file)

        for img in data["IMAGES"]:
            attributes = img["ATTRIBUTE"]

            # make one json for all attributes instead of several
            new_attributes = {}
            for attribute in attributes:
                if attribute["@NAME"] == "colour":
                    new_attributes["@COLOUR"] = attribute["@VALUE"]
                elif attribute["@NAME"] == "orientation":
                    new_attributes["@ORIENTATION"] = attribute["@VALUE"]
                elif attribute["@NAME"] == "type":
                    new_attributes["@TYPE"] = attribute["@VALUE"]
                elif attribute["@NAME"] == "size":
                    new_attributes["@SIZE"] = attribute["@VALUE"]
            # Replace the list of jsons with the new single json
            img["ATTRIBUTE"] = new_attributes
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()

    print("The file has been updated.")


def process_tuna():
    # Check if not already downloaded
    if not os.path.exists("games/multimodal_referencegame/prep/tuna_original"):
        download_tuna()
    else:
        print("TUNA corpus already downloaded.")
    # Convert all furniture episodesto json
    directory_sg = "games/multimodal_referencegame/prep/tuna_original/dist/corpus/singular/furniture"
    directory_pl = (
        "games/multimodal_referencegame/prep/tuna_original/dist/corpus/plural/furniture"
    )
    convert_all_furniture(directory_sg, directory_pl)
    # Extract all unique images and their attributes to a single json
    extract_imgs()
    # Change attribute structure for images
    change_tuna_attribute_struct("games/multimodal_referencegame/prep/tuna/all_imgs.json")
    # Remove original tuna folder
    shutil.rmtree("games/multimodal_referencegame/prep/tuna_original")
    print("TUNA corpus prepared. Proceed with making stimuli tuples.")


if __name__ == "__main__":
    process_tuna()
