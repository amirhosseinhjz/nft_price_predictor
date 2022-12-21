from .predictor_model_interface import PredictorModelInterface
import random
import requests

class ResnetModel(PredictorModelInterface):
    def __init__(self):
        super().__init__()
        self.model = None

    @staticmethod
    def predict(image) -> int:
        url = "http://predictor:5520/predict/"
        response = requests.post(url, json={"photo": image}).json()
        print(response)
        return response["resp"]