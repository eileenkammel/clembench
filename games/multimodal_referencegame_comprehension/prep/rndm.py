import json


def get_human_expression(stimuli_id):
    with open("games/multimodal_referencegame_comprehension/in/instances.json", "r") as f:
        instances = json.load(f)
        for eperiment in instances["experiments"]:
            for game in eperiment["game_instances"]:
                if game["stimuli_id"] == stimuli_id:
                    return game["human_expression"]
                

if __name__ == "__main__":
    print(get_human_expression(878))