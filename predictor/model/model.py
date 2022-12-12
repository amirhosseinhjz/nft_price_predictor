from interface.predictor import PredictorInterface
# import numpy as np
# import torch
# from torch import nn
# from torchvision import transforms
# from torchvision.models import resnet50
# from PIL import Image
import random

class Predictor(PredictorInterface):
    def __init__(self, runtimes=100):
        # self.net = self.create_network()
        self.runtimes = runtimes
        # self.net.eval()
        # self.valid_transform = self.create_valid_transformer()

    def _predict(self, photo=None):
        return random.randint(1,5)
        # photo = Image.open(photo).convert('RGB')
        # photo = self.valid_transform(photo)
        # photo = photo.unsqueeze(0)
        # photo = photo.to('cpu')
        # pred = self.net(photo)
        # pred = pred.detach().numpy()
        # pred = np.argmax(pred)
        # return pred

    def predict(self, photo=None):
        resp = sum([self._predict(photo) for _ in range(self.runtimes)]) / self.runtimes
        return resp
        
    def __call__(self, photo):
        return self.predict(photo)

    @staticmethod
    def create_valid_transformer():
        valid_transform = transforms.Compose([
            transforms.Resize([224, 224]),
            transforms.ToTensor(),
            transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
        ])
        return valid_transform

    @staticmethod
    def create_network():
        net = resnet50(pretrained=False)
        net.fc = nn.Sequential(nn.Linear(in_features=2048, out_features=100, bias=True),
                            nn.Dropout(.2),
                            nn.Linear(in_features=100, out_features=5, bias=True),
                            nn.Softmax())
        pth = torch.load("model/Run4/checkpoint.pth.tar", map_location=torch.device('cpu'))
        net.load_state_dict(pth['state_dict'])
        net.to('cpu')
        return net
