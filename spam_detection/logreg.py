from base import BaseSpamDetector
from joblib import load

from .util import TextPreprocessor


class LogRegDetector(BaseSpamDetector):
    def __init__(self):
        super().__init__()
        self.model = load('spam_detection/models/tfidf_logerg.pipe')

    def validate(self, text: str) -> bool:
        if text is None:
            return False
        text = TextPreprocessor.lemmatize(text)
        return self.model.predict([text])
