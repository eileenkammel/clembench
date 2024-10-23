# -*-coding:utf-8 -*-
# Author: Eileen Kammel, 811770
# Date: 2024-10-22 18:45:39

# This script prepares the 3DShapenet dataset for the multimodal reference game.
import numpy as np
import h5py
import time
import json
from PIL import Image
import os

dataset = h5py.File("3DS/3dshapes.h5", "r")

images1 = dataset["images"][
    :260000
]  # array shape [260000,64,64,3], uint8 in range(256)
labels1 = dataset["labels"][:260000]  # array shape [260000,6], float64
images2 = dataset["images"][
    260000:
]  # array shape [260000,64,64,3], uint8 in range(256)
labels2 = dataset["labels"][260000:]  # array shape [260000,6], float64


hues = {
    0.0: "red",
    0.1: "orange",
    0.2: "yellow",
    0.30000000000000004: "green",  # somewhere 0.3 becomes this
    0.4: "moss",  # removed from the dataset
    0.5: "turquoise",
    0.6000000000000001: "blue",  # somewhere 0.6 becomes this
    0.7000000000000001: "darkblue",  # removed from the dataset
    0.8: "purple",
    0.9: "pink",
}

scale = {
    0.75: "small",
    1.25: "large"
}

shape = {
    0: "cube",
    1: "cylinder",
    2: "ball",
    3: "pill"  # removed from the dataset
}

orientation = {
    -30.0: "left",
    0.0: "front",
    30.0: "right"
}

# Select susbet of data with only the desired values
# 1. Get rid of images where floor_hue, wall_hue, object_hue are the same
# 2. Get rid of images that are not largest or smallest scale
# 3. Get rid of images where the orientation is not left, right or frontal (-30, 0, 30)
# All selection criteria  subject to change.

# Work in two batches, because of memory issues
# Batch 1

start = time.time()
print("Start time batch 1:", start)


# 1. Get rid of images where floor_hue, wall_hue, object_hue are the same
# When not all values are the same, that means at least two have to be different
different_hue_mask1 = (labels1[:, 0] != labels1[:, 1]) | (
    labels1[:, 1] != labels1[:, 2]
)

labels1 = labels1[different_hue_mask1]
images1 = images1[different_hue_mask1]

print("Different hue mask applied.")
print(labels1.shape)
print(images1.shape)

# 2. Get rid of images that are not largest or smallest scale
two_sizes_mask1 = (labels1[:, 3] == 0.75) | (labels1[:, 3] == 1.25)

labels1 = labels1[two_sizes_mask1]
images1 = images1[two_sizes_mask1]

print("Two sizes mask applied.")
print(labels1.shape)
print(images1.shape)

# 3. Get rid of images where the orientation is not left, right or frontal (-30, 0, 30)
three_orientations_mask1 = (
    (labels1[:, 5] == -30.0) | (labels1[:, 5] == 0.0) | (labels1[:, 5] == 30.0)
)

labels1 = labels1[three_orientations_mask1]
images1 = images1[three_orientations_mask1]

print("Three orientations mask applied.")
print(labels1.shape)
print(images1.shape)

# 4. Get rid of to silimar hues
colour_mask = (
    (labels1[:, 0] != 0.4)
    | (labels1[:, 0] != 0.7000000000000001) & (labels1[:, 1] != 0.4)
    | (labels1[:, 1] != 0.7000000000000001) & (labels1[:, 2] != 0.4)
    | (labels1[:, 2] != 0.7000000000000001)
)

labels1 = labels1[colour_mask]
images1 = images1[colour_mask]

print("Colour mask applied.")
print(labels1.shape)
print(images1.shape)

# 5. Get rid of har to name pill shape
shape_mask = labels1[:, 4] != 3

labels1 = labels1[shape_mask]
images1 = images1[shape_mask]

print("Shape mask applied.")
print(labels1.shape)
print(images1.shape)

print("Colour mask applied.")
print(labels1.shape)
print(images1.shape)

end = time.time()
print("End time batch 1:", end)

# Batch 2
start = time.time()
print("Start time batch 2:", start)

# 1. Get rid of images where floor_hue, wall_hue, object_hue are the same
# When not all values are the same, that means at leat two have to be different
different_hue_mask2 = (labels2[:, 0] != labels2[:, 1]) | (
    labels2[:, 1] != labels2[:, 2]
)

labels2 = labels2[different_hue_mask2]
images2 = images2[different_hue_mask2]

print("Different hue mask applied.")
print(labels2.shape)
print(images2.shape)

# Get rid of images that are not largest or smallest scale
two_sizes_mask2 = (labels2[:, 3] == 0.75) | (labels2[:, 3] == 1.25)

labels2 = labels2[two_sizes_mask2]
images2 = images2[two_sizes_mask2]

print("Two sizes mask applied.")
print(labels2.shape)
print(images2.shape)


# Get rid of images where the orientation is not left, right or frontal (-30, 0, 30)
three_orientations_mask2 = (
    (labels2[:, 5] == -30.0) | (labels2[:, 5] == 0.0) | (labels2[:, 5] == 30.0)
)

labels2 = labels2[three_orientations_mask2]
images2 = images2[three_orientations_mask2]

print("Three orientations mask applied.")
print(labels2.shape)
print(images2.shape)

# 4. Get rid of har to name pill shape
shape_mask2 = labels2[:, 4] != 3

labels2 = labels2[shape_mask2]
images2 = images2[shape_mask2]

print("Shape mask applied.")
print(labels2.shape)
print(images2.shape)

# 5. Get rid of to silimar hues
colour_mask2 = (
    (labels2[:, 0] != 0.4)
    | (labels2[:, 0] != 0.7000000000000001) & (labels2[:, 1] != 0.4)
    | (labels2[:, 1] != 0.7000000000000001) & (labels2[:, 2] != 0.4)
    | (labels2[:, 2] != 0.7000000000000001)
)

labels2 = labels2[colour_mask2]
images2 = images2[colour_mask2]

print("Colour mask applied.")
print(labels2.shape)
print(images2.shape)

end = time.time()
print("End time batch 2:", end)

# Concatenate the two batches
images = np.concatenate((images1, images2), axis=0)
labels = np.concatenate((labels1, labels2), axis=0)

# Save images as png (jpg has to much loss, I tried it) and make
# corresponding json that saves filename and attributes.
# Translate the labels to strings.

data_set = zip(images, labels)

json_data = {"IMAGES": []}

for i, (image, label) in enumerate(data_set):
    filename = f"{i}.png"
    json_data["IMAGES"].append(
        {
            "@ID": i,
            "@FILENAME": filename,
            "ATTRIBUTE": {
                "floor_hue": hues[label[0]],
                "wall_hue": hues[label[1]],
                "object_hue": hues[label[2]],
                "scale": scale[label[3]],
                "shape": shape[label[4]],
                "orientation": orientation[label[5]],
            },
        }
    )
    img = Image.fromarray(image.astype("uint8"), "RGB")
    image_path = os.path.join("3DS/", filename)
    img.save(image_path)

with open("3DS/3ds_subset.json", "w") as f:
    json.dump(json_data, f, indent=4)
