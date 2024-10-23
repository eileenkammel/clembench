# -*-coding:utf-8 -*-
# Author: Eileen Kammel, 811770
# Date: 2024-10-22 19:36:01

import json
import random
import itertools
import os

# set seed for reproducibility
random.seed(1012)


def define_id(n):
    # Return all possible combinations of n attributes
    # by attribut list indices
    attribute_list = [0, 1, 2, 3, 4, 5]
    ids = itertools.combinations(attribute_list, n)
    return list(ids)


def extract_attributes(image):
    # Return a list of all attributes of an image
    return [
        image["ATTRIBUTE"]["floor_hue"],
        image["ATTRIBUTE"]["wall_hue"],
        image["ATTRIBUTE"]["object_hue"],
        image["ATTRIBUTE"]["scale"],
        image["ATTRIBUTE"]["shape"],
        image["ATTRIBUTE"]["orientation"],
    ]


def determine_id_style(id):
    id_style = {
        (0,): "floor_hue",
        (1,): "wall_hue",
        (2,): "object_hue",
        (3,): "scale",
        (4,): "shape",
        (5,): "orientation",
        (0, 1): "floor_hue_wall_hue",
        (0, 2): "floor_hue_object_hue",
        (0, 3): "floor_hue_scale",
        (0, 4): "floor_hue_shape",
        (0, 5): "floor_hue_orientation",
        (1, 2): "wall_hue_object_hue",
        (1, 3): "wall_hue_scale",
        (1, 4): "wall_hue_shape",
        (1, 5): "wall_hue_orientation",
        (2, 3): "object_hue_scale",
        (2, 4): "object_hue_shape",
        (2, 5): "object_hue_orientation",
        (3, 4): "scale_shape",
        (3, 5): "scale_orientation",
        (4, 5): "shape_orientation",
        (0, 1, 2): "floor_hue_wall_hue_object_hue",
        (0, 1, 3): "floor_hue_wall_hue_scale",
        (0, 1, 4): "floor_hue_wall_hue_shape",
        (0, 1, 5): "floor_hue_wall_hue_orientation",
        (0, 2, 3): "floor_hue_object_hue_scale",
        (0, 2, 4): "floor_hue_object_hue_shape",
        (0, 2, 5): "floor_hue_object_hue_orientation",
        (0, 3, 4): "floor_hue_scale_shape",
        (0, 3, 5): "floor_hue_scale_orientation",
        (0, 4, 5): "floor_hue_shape_orientation",
        (1, 2, 3): "wall_hue_object_hue_scale",
        (1, 2, 4): "wall_hue_object_hue_shape",
        (1, 2, 5): "wall_hue_object_hue_orientation",
        (1, 3, 4): "wall_hue_scale_shape",
        (1, 3, 5): "wall_hue_scale_orientation",
        (1, 4, 5): "wall_hue_shape_orientation",
        (2, 3, 4): "object_hue_scale_shape",
        (2, 3, 5): "object_hue_scale_orientation",
        (2, 4, 5): "object_hue_shape_orientation",
        (3, 4, 5): "scale_shape_orientation",
        (0, 1, 2, 3): "floor_hue_wall_hue_object_hue_scale",
        (0, 1, 2, 4): "floor_hue_wall_hue_object_hue_shape",
        (0, 1, 2, 5): "floor_hue_wall_hue_object_hue_orientation",
        (0, 1, 3, 4): "floor_hue_wall_hue_scale_shape",
        (0, 1, 3, 5): "floor_hue_wall_hue_scale_orientation",
        (0, 1, 4, 5): "floor_hue_wall_hue_shape_orientation",
        (0, 2, 3, 4): "floor_hue_object_hue_scale_shape",
        (0, 2, 3, 5): "floor_hue_object_hue_scale_orientation",
        (0, 2, 4, 5): "floor_hue_object_hue_shape_orientation",
        (0, 3, 4, 5): "floor_hue_scale_shape_orientation",
        (1, 2, 3, 4): "wall_hue_object_hue_scale_shape",
        (1, 2, 3, 5): "wall_hue_object_hue_scale_orientation",
        (1, 2, 4, 5): "wall_hue_object_hue_shape_orientation",
        (1, 3, 4, 5): "wall_hue_scale_shape_orientation",
        (2, 3, 4, 5): "object_hue_scale_shape_orientation",
        (0, 1, 2, 3, 4): "floor_hue_wall_hue_object_hue_scale_shape",
        (0, 1, 2, 3, 5): "floor_hue_wall_hue_object_hue_scale_orientation",
        (0, 1, 2, 4, 5): "floor_hue_wall_hue_object_hue_shape_orientation",
        (0, 1, 3, 4, 5): "floor_hue_wall_hue_scale_shape_orientation",
        (0, 2, 3, 4, 5): "floor_hue_object_hue_scale_shape_orientation",
        (1, 2, 3, 4, 5): "wall_hue_object_hue_scale_shape_orientation",
        (0, 1, 2, 3, 4, 5): "floor_hue_wall_hue_object_hue_scale_shape_orientation",
    }
    return id_style[id]


def return_rndm_distractor(distractor_count, excluded_imgs):
    all_img = range(0, 17820)
    possible_distractors = list(set(all_img) - set(excluded_imgs))
    distractors = random.sample(possible_distractors, distractor_count)
    distractors = [f"{distractor}.png" for distractor in distractors]
    return distractors


def get_image_numbers(images):
    return [image.strip(".png") for image in images]


def find_distractors(target, target_attributes, target_id, distractor_count):
    # Return two distractors that fit the target_id
    all_img = json.load(
        open("games/multimodal_referencegame/prep/3DS/3ds_image_subset.json", "r")
    )
    attribute_idx = set([0, 1, 2, 3, 4, 5])
    target_id = set(target_id)
    if len(target_id) == 1:
        possible_distractors = []
        # attributes that are not in the target_id by idx
        non_id_attributes = list(attribute_idx.difference(target_id))
        target_id = list(target_id)
        # index of the target attribute(s)
        a1_idx = target_id[0]
        # loop over all images and find distractors
        for image in all_img["IMAGES"]:
            image_filename = image["@FILENAME"]
            # get the attributes of the potential distractor
            image_attributes = extract_attributes(image)
            # skip img which have same attribute(s) as target id
            if image_attributes[a1_idx] == target_attributes[a1_idx]:
                continue
            # rest of the attributes must be the same
            else:
                if (
                    image_attributes[non_id_attributes[0]]
                    == target_attributes[non_id_attributes[0]]
                    and image_attributes[non_id_attributes[1]]
                    == target_attributes[non_id_attributes[1]]
                    and image_attributes[non_id_attributes[2]]
                    == target_attributes[non_id_attributes[2]]
                    and image_attributes[non_id_attributes[3]]
                    == target_attributes[non_id_attributes[3]]
                    and image_attributes[non_id_attributes[4]]
                    == target_attributes[non_id_attributes[4]]
                ):
                    possible_distractors.append(image_filename)
        try:
            possible_distractors = random.sample(possible_distractors, 2)
            if distractor_count == 2:
                return possible_distractors
            elif distractor_count == 3:
                img_nums = get_image_numbers(possible_distractors + [target])
                additional_distractors = return_rndm_distractor(1, img_nums)
                return possible_distractors + additional_distractors
        except ValueError:
            # print("No distractors found.")
            return None
    elif len(target_id) == 2:
        possible_distractors1 = []
        possible_distractors2 = []
        non_id_attributes = list(attribute_idx.difference(target_id))
        target_id = list(target_id)
        a1_idx = target_id[0]
        a2_idx = target_id[1]
        for image in all_img["IMAGES"]:
            image_filename = image["@FILENAME"]
            image_attributes = extract_attributes(image)
            if (
                image_attributes[a1_idx] == target_attributes[a1_idx]
                and image_attributes[a2_idx] == target_attributes[a2_idx]
            ):
                continue
            else:
                # find first distractor candidates
                if (
                    image_attributes[a1_idx] == target_attributes[a1_idx]
                    and image_attributes[a2_idx] != target_attributes[a2_idx]
                    and image_attributes[non_id_attributes[0]]
                    == target_attributes[non_id_attributes[0]]
                    and image_attributes[non_id_attributes[1]]
                    == target_attributes[non_id_attributes[1]]
                    and image_attributes[non_id_attributes[2]]
                    == target_attributes[non_id_attributes[2]]
                    and image_attributes[non_id_attributes[3]]
                    == target_attributes[non_id_attributes[3]]
                ):
                    possible_distractors1.append(image_filename)

                # find second distractor candidates

                if (
                    image_attributes[a1_idx] != target_attributes[a1_idx]
                    and image_attributes[a2_idx] == target_attributes[a2_idx]
                    and image_attributes[non_id_attributes[0]]
                    == target_attributes[non_id_attributes[0]]
                    and image_attributes[non_id_attributes[1]]
                    == target_attributes[non_id_attributes[1]]
                    and image_attributes[non_id_attributes[2]]
                    == target_attributes[non_id_attributes[2]]
                    and image_attributes[non_id_attributes[3]]
                    == target_attributes[non_id_attributes[3]]
                ):
                    possible_distractors2.append(image_filename)
        # return one random distractor from each list if they exist, else skip
        try:
            possible_distractors1 = random.sample(possible_distractors1, 1)
            possible_distractors2 = random.sample(possible_distractors2, 1)
            distractors = possible_distractors1 + possible_distractors2
            if distractor_count == 2:
                return distractors if len(distractors) == 2 else None
            elif distractor_count == 3:
                img_nums = get_image_numbers(distractors + [target])
                additional_distractors = return_rndm_distractor(1, img_nums)
                return distractors + additional_distractors
        except ValueError:
            # print("Not enough distractors found.")
            return None
    elif len(target_id) == 3:
        possible_distractors1 = []
        possible_distractors2 = []
        possible_distractors3 = []
        # attributes that are not in the target_id by idx
        non_id_attributes = list(attribute_idx.difference(target_id))
        target_id = list(target_id)
        # index of the target attribute(s)
        a1_idx = target_id[0]
        a2_idx = target_id[1]
        a3_idx = target_id[2]
        # loop over all images and find distractors
        for image in all_img["IMAGES"]:
            image_filename = image["@FILENAME"]
            # get the attributes of the potential distractor
            image_attributes = extract_attributes(image)
            # skip img which have same attribute(s) as target id
            if (
                image_attributes[a1_idx] == target_attributes[a1_idx]
                and image_attributes[a2_idx] == target_attributes[a2_idx]
                and image_attributes[a3_idx] == target_attributes[a3_idx]
            ):
                continue
            else:
                # find first distractor candidates
                if (
                    image_attributes[a1_idx] != target_attributes[a1_idx]
                    and image_attributes[a2_idx] == target_attributes[a2_idx]
                    and image_attributes[a3_idx] == target_attributes[a3_idx]
                    and image_attributes[non_id_attributes[0]]
                    == target_attributes[non_id_attributes[0]]
                    and image_attributes[non_id_attributes[1]]
                    == target_attributes[non_id_attributes[1]]
                    and image_attributes[non_id_attributes[2]]
                    == target_attributes[non_id_attributes[2]]
                ):
                    possible_distractors1.append(image_filename)

                # find second distractor candidates
                if (
                    image_attributes[a1_idx] == target_attributes[a1_idx]
                    and image_attributes[a2_idx] != target_attributes[a2_idx]
                    and image_attributes[a3_idx] == target_attributes[a3_idx]
                    and image_attributes[non_id_attributes[0]]
                    == target_attributes[non_id_attributes[0]]
                    and image_attributes[non_id_attributes[1]]
                    == target_attributes[non_id_attributes[1]]
                    and image_attributes[non_id_attributes[2]]
                    == target_attributes[non_id_attributes[2]]
                ):
                    possible_distractors2.append(image_filename)

                # find third distractor candidates
                if (
                    image_attributes[a1_idx] == target_attributes[a1_idx]
                    and image_attributes[a2_idx] == target_attributes[a2_idx]
                    and image_attributes[a3_idx] != target_attributes[a3_idx]
                    and image_attributes[non_id_attributes[0]]
                    == target_attributes[non_id_attributes[0]]
                    and image_attributes[non_id_attributes[1]]
                    == target_attributes[non_id_attributes[1]]
                    and image_attributes[non_id_attributes[2]]
                    == target_attributes[non_id_attributes[2]]
                ):
                    possible_distractors3.append(image_filename)
        # return one random distractor from each list if they exist, else skip
        try:
            possible_distractors1 = random.sample(possible_distractors1, 1)
            possible_distractors2 = random.sample(possible_distractors2, 1)
            possible_distractors3 = random.sample(possible_distractors3, 1)
            distractors = (
                possible_distractors1 + possible_distractors2 + possible_distractors3
            )
            return distractors if len(distractors) == 3 else None
        except ValueError:
            print("Not enough distractors found.")
            return None


def make_stimuli_sets(distractor_count=2):

    assert distractor_count in [2, 3], "Distractor count must be 2 or 3."
    if distractor_count == 2:
        json_instances = {"INSTANCES": {"one_attibute_id": [], "two_attibute_id": []}}
    elif distractor_count == 3:
        json_instances = {
            "INSTANCES": {
                "one_attibute_id": [],
                "two_attibute_id": [],
                "three_attibute_id": [],
            }
        }

    episode_num = 0

    # loop over 3DS/3ds_subset.json, image will be target
    all_img = json.load(
        open("games/multimodal_referencegame/prep/3DS/3ds_image_subset.json", "r")
    )

    # pick 100 random targets, to speed up the process
    random.shuffle(all_img["IMAGES"])
    all_img["IMAGES"] = all_img["IMAGES"][:100]

    for img in all_img["IMAGES"]:
        target_filename = img["@FILENAME"]
        target_attributes = extract_attributes(img)
        # find ids for target with all
        # possible lengths & combinations of attributes
        # max len = 2 if distractors = 2,
        # max len = 3 if distractors = 3
        range_end = distractor_count + 1
        for i in range(1, range_end):
            ids = define_id(i)
            for id in ids:
                distractors = find_distractors(
                    target_filename, target_attributes, id, distractor_count
                )
                if distractors is not None:
                    if distractor_count == 2:
                        episode = {
                            "stimuli_id": episode_num,
                            "target": target_filename,
                            "distractor1": distractors[0],
                            "distractor2": distractors[1],
                            "id_type": determine_id_style(id),
                        }

                        if i == 1:
                            json_instances["INSTANCES"]["one_attibute_id"].append(
                                episode
                            )
                        elif i == 2:
                            json_instances["INSTANCES"]["two_attibute_id"].append(
                                episode
                            )

                        episode_num += 1
                    elif distractor_count == 3:
                        episode = {
                            "stimuli_id": episode_num,
                            "target": target_filename,
                            "distractor1": distractors[0],
                            "distractor2": distractors[1],
                            "distractor3": distractors[2],
                            "id_type": determine_id_style(id),
                        }

                        if i == 1:
                            json_instances["INSTANCES"]["one_attibute_id"].append(
                                episode
                            )
                        elif i == 2:
                            json_instances["INSTANCES"]["two_attibute_id"].append(
                                episode
                            )
                        elif i == 3:
                            json_instances["INSTANCES"]["three_attibute_id"].append(
                                episode
                            )

                        episode_num += 1
        if episode_num % 10 == 0:
            print(f"Processed {episode_num} episodes")

    with open(
        f"games/multimodal_referencegame/prep/3DS/3ds_{distractor_count}_distractor_instances.json",
        "w",
    ) as json_file:
        json.dump(json_instances, json_file, indent=4)
    print("All instances saved successfully!")


# Delete all images not used in the stimuli because there are over 8k images
def delete_unused_images():
    instances = json.load(
        open(
            "games/multimodal_referencegame/prep/3DS/3ds_3_distractor_instances.json",
            "r",
        )
    )
    all_images = json.load(
        open("games/multimodal_referencegame/prep/3DS/3ds_image_subset.json", "r")
    )

    used_images = []
    for instance in instances["INSTANCES"]["one_attibute_id"]:
        used_images.append(instance["target"])
        used_images.append(instance["distractor1"])
        used_images.append(instance["distractor2"])
        used_images.append(instance["distractor3"])

    for instance in instances["INSTANCES"]["two_attibute_id"]:
        used_images.append(instance["target"])
        used_images.append(instance["distractor1"])
        used_images.append(instance["distractor2"])
        used_images.append(instance["distractor3"])

    for instance in instances["INSTANCES"]["three_attibute_id"]:
        used_images.append(instance["target"])
        used_images.append(instance["distractor1"])
        used_images.append(instance["distractor2"])
        used_images.append(instance["distractor3"])

    all_images = all_images["IMAGES"]
    all_images = [image["@FILENAME"] for image in all_images]

    unused_images = list(set(all_images) - set(used_images))

    for image in unused_images:
        os.remove(f"games/multimodal_referencegame/resources/3ds_images/{image}")

    print("Unused images deleted successfully!")


if __name__ == "__main__":
    make_stimuli_sets(distractor_count=3)
    delete_unused_images()
