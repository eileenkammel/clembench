# Data Preparation
## Requirements
Requirements not already satisfied by clem requirements:\
```h5py```\
```xmltodict```\
run ```pip install -r games/multimodal_referencegame/prep/requirements.txt```
## TUNA Corpus
run: ```python3 games/multimodal_referencegame/prep/prep_tuna.py```
- Downloads Corpus
- Adapts data format from XML to json
- Extracts all unique images and their attributes for furniture sub category while deleting information not needed
- Pairs targets with distractors (exhaustively for later sub selection)
    - Default is set to 3 distractors, can also be run with argument ```-p 2``` for only 2 Distractors
- Image files are only stored locally and will not be pushed to remote



## 3D Shapes Corpus
- Download raw corpus here: https://storage.cloud.google.com/3d-shapes/3dshapes.h5 (needs Google account authentication) and save to ```games/multimodal_referencegame/prep/```
- Image files are only stored locally and will not be pushed to remote


## Prune/delete Data
- In case the models cannot handle 4 images (1 target + 3 distractors), the instances can be pruned to only 3 images by running ```prune_instances.py```
- Instances were set up and will be pruned in such a way that human data gathered with it will still be valid
- Optional: To free up space, image files not used in the final instances can be deleted by running ```delete_unused_imgs.py```