# -*-coding:utf-8 -*-
# Author: Eileen Kammel, 811770
# Date: 2025-02-11 15:22:32

from games.multimodal_referencegame.prep.stim_id_map import get_idtype
import spacy

# TUNA Attributes


tuna_types = {
    "chair": ["chair"],
    "sofa": ["couch", "sofa", "loveseat"],
    "desk": ["desk", "table", "drawer", "cabinet", "chest"],
    "fan": ["fan", "ventilator"],
}

tuna_colors = {
    "red": ["red"],
    "blue": ["blue"],
    "green": ["green"],
    "grey": ["black", "grey", "gray", "white", "beige", "cream"],
}

tuna_sizes = {
    "small": ["small", "smallest"],
    "large": ["big", "large", "bigger", "lager"],
}

tuna_orientation = {
    "left": ["left"],
    "right": ["right"],
    "front": ["front", "to me", "to you", "frontal", "facing me", "facing you", "faces me", "faces you", "facing stright"],
    "back": ["back", "behind", "backwards", "away"],
}

tuna_attributes = {
    "type": tuna_types,
    "colour": tuna_colors,
    "size": tuna_sizes,
    "orientation": tuna_orientation,
}


# 3DS Attributes


threeds_floorhues = {
    "red": ["red"],
    "orange": ["orange"],
    "yellow": ["yellow"],
    "green": ["green"],
    "turquoise": ["turquoise"],
    "blue": ["blue"],
    "purple": ["purple"],
    "pink": ["pink"],
    "moss": ["moss", "green"],
    "darkblue": ["darkblue", "dark blue", "blue"]
}

threeds_wallhues = {
    "red": ["red"],
    "orange": ["orange"],
    "yellow": ["yellow"],
    "green": ["green"],
    "turquoise": ["turquoise"],
    "blue": ["blue"],
    "purple": ["purple"],
    "pink": ["pink"],
    "moss": ["moss", "green"],
    "darkblue": ["darkblue", "dark blue", "blue"]
}

threeds_objecthues = {
    "red": ["red"],
    "orange": ["orange"],
    "yellow": ["yellow"],
    "green": ["green"],
    "turquoise": ["turquoise"],
    "blue": ["blue"],
    "purple": ["purple"],
    "pink": ["pink"],
    "moss": ["moss", "green"],
    "darkblue": ["darkblue", "dark blue", "blue"]
}

threeds_shape = {
    "cube": ["cube"],
    "cylinder": ["cylinder"],
    "ball": ["sphere", "ball"],
}

threeds_scale = {
    "small": ["small", "smaller"],
    "large": ["big", "bigger", "large", "lager"],
}

# This is confusing. The image is rotated: rotating left makes the corner in the
# right appear and vice versa. People refer to lacation
# of corner and not rotation.
threeds_orientation = {"left": ["right"], "front": ["front"], "right": ["left"]}

threeds_attributes = {
    "floorHue": threeds_floorhues,
    "wallHue": threeds_wallhues,
    "objectHue": threeds_objecthues,
    "shape": threeds_shape,
    "scale": threeds_scale,
    "orientation": threeds_orientation,
}


def analyze_expression(set_name, expression, stim_id):
    expression = expression.lower()
    id_type, id_attributes = get_idtype(set_name, stim_id)
    id_type = id_type.split("_")
    id_attributes = id_attributes.split(",")
    included_attributes = 0
    for attribute in zip(id_type, id_attributes):
        correct_attribute = attribute[1]
        attributes = (
            tuna_attributes[attribute[0]]
            if set_name == "tuna"
            else threeds_attributes[attribute[0]]
        )
        synonyms = attributes[correct_attribute]
        if correct_attribute in expression:
            included_attributes += 1
        else:
            for synonym in synonyms:
                if synonym in expression:
                    included_attributes += 1
                    # adjust for multiword syns to count as one token
                    expression.replace(synonym, correct_attribute)
    if len(id_type) == included_attributes:
        if len(id_type) ==  len(expression.split()):
            return "Correct ID", 0
        else:
            return "Correct ID", analyze_surplus(expression, included_attributes)
    else:
        if included_attributes > 0:
            return "Insufficient ID", analyze_surplus(expression, included_attributes)
        if included_attributes == 0:
            return "NO ID", analyze_surplus(expression, included_attributes)



def analyze_surplus(expression, id_type_len):
    expression = expression.lower()
    tagger = spacy.load("en_core_web_sm")
    tagged_expression = tagger(expression)
    adjective_count = sum([1 for token in tagged_expression if token.pos_ == "ADJ"])
    noun_count = sum([1 for token in tagged_expression if token.pos_ in {"NOUN", "PROPN"}])
    total_info_surplus = adjective_count + noun_count
    surplus_info = total_info_surplus - id_type_len
    return surplus_info


#print(analyze_expression("tuna", "the small red desk", 55))
#print(analyze_expression("tuna", "red", 220))
#print(analyze_expression("tuna", "green sofa", 977))
#print(analyze_expression("3ds", "sphere", 1403))
#analyze_expression("3ds", "green, chair, blue", 48)
