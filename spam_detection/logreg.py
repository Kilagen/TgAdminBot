import os
from base import BaseSpamDetector
from joblib import load

from .util import TextPreprocessor

model_path = os.path.dirname(os.path.abspath(__file__)) + "/./models/tfidf_logreg.pipe"


class LogRegDetector(BaseSpamDetector):
    def __init__(self):
        super().__init__()
        self.model = load(model_path)

    def validate(self, text: str) -> bool:
        if text is None:
            return False
        text = TextPreprocessor.lemmatize(text)
        return self.model.predict([text])
