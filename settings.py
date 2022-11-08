import os 
import torch

DEPTH_ESTIMATOR_WEIGHTS_PATH = os.path.normpath(
    "depth_estimator/weights"
)
PHOTO_DIR = os.path.normpath(
    'test/photos'
)
SAVE_DEPTH_PRED_PATH = os.path.normpath(
    'test/depth_predicted'
)
SAVE_OBJ_PATH = os.path.normpath(
    'test/objects'
)
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"