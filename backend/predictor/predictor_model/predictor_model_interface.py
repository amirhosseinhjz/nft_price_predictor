


class PredictorModelInterface(object):
    def __init__(self):
        pass

    def predict(self, image) -> int:
        raise NotImplementedError