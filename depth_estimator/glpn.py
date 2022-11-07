from transformers import GLPNFeatureExtractor, GLPNForDepthEstimation
import torch
import numpy as np
from PIL import Image
import settings


class glpn_model():

    def __init__(
        self,
        weights_path
    ):

        self.feature_extractor = GLPNFeatureExtractor.from_pretrained(
                    weights_path
        )
        self.model = GLPNForDepthEstimation.from_pretrained(
                    weights_path
        )

    def image_prepare(self, image_path):

        """
        image:str - image path 
        """
        image = Image.open(image_path)

        new_height = 480 if image.height > 480 else image.height
        new_height -= (new_height % 32)
        new_width = int(new_height * image.width / image.height)
        diff = new_width % 32
        new_width = new_width - diff if diff < 16 else new_width + 32 - diff
        new_size = (new_width, new_height)
        image = image.resize(new_size)

        return image


    def predict_depth(self, image:str):

        inputs = self.feature_extractor(
            images=image, 
            return_tensors="pt"
        )

        with torch.no_grad():
            outputs = self.model(**inputs)
            predicted_depth = outputs.predicted_depth

        # interpolate to original size
        prediction = torch.nn.functional.interpolate(
            predicted_depth.unsqueeze(1),
            size=image.size[::-1],
            mode="bicubic",
            align_corners=False,
        )

        # visualize the prediction
        output = prediction.squeeze().to('cpu').numpy()
        formatted = (output * 255 / np.max(output)).astype("uint8")
        depth = Image.fromarray(formatted)

        return depth