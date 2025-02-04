#!/bin/bash
# Usage: ./games/multimodal_referencegame/prep/prep_refgame.sh

echo
echo "==================================================="
echo "SETUP MMREFGAME STARTING"
echo "==================================================="
echo
pyhton3 prep_tuna.py
pyhton3 prep_3ds.py
python3 games/multimodal_referencegame/my_instancegenerator_3Distractors.py
python3 loc_bias.py
python3 delete_unused_imgs.py

echo
echo "==================================================="
echo "SELECT IMGS FOR GROUND TRUTH"
echo "==================================================="

python3 games/multimodal_referencegame/prep/only_target_img.py

echo
echo "==================================================="
echo "COPY IMGS TO GROUND TRUTH"
echo "==================================================="

GT_3DS_DESTINATION = "games/ground_truth/recources/3ds_images"
GT_TUNA_DESTINATION = "games/ground_truth/recources/tuna_images"

mkdir -p "$GT_3DS_DESTINATION"
mkdir -p "$GT_TUNA_DESTINATION"

cp games/multimodal_referencegame/prep/3DS_targets/* "$GT_3DS_DESTINATION" && echo "File copied successfully!" || echo "Error: File copy failed!"
cp games/multimodal_referencegame/prep/TUNA_targets/* "$GT_TUNA_DESTINATION" && echo "File copied successfully!" || echo "Error: File copy failed!"