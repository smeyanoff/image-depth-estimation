import cv2
import matplotlib.pyplot as plt
import torch


class midas_estimator:
    def __init__(self, model, device):

        """
        model:str ["DPT_Large", "DPT_Hybrid", "MiDaS_small"]
        """

        self.device = torch.device(device)
        self.model = torch.hub.load("intel-isl/MiDaS", model)
        self.model.to(device)
        self.model.eval()
        self.transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
        if model == "DPT_Large" or model == "DPT_Hybrid":
            self.transform = self.transforms.dpt_transform
        else:
            self.transform = self.transforms.small_transform
        
    def image_prepare(self, image_path):

        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        return image

    def predict_depth(self, image):

        input_batch = self.transform(image).to(self.device)

        with torch.no_grad():
            prediction = self.model(input_batch)

            prediction = torch.nn.functional.interpolate(
                prediction.unsqueeze(1),
                size=image.shape[:2],
                mode="bicubic",
                align_corners=False,
            ).squeeze()

        depth = prediction.cpu().numpy()

        return depth
