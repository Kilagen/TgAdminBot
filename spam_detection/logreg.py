from base import BaseSpamDetector
from joblib import load


class LogRegDetector(BaseSpamDetector):
    def __init__(self):
        super().__init__()
        self.model = load('spam_detection/models/logreg.model')
        self.vectorizer = load('spam_detection/models/logreg.vectorizer')

    async def _validate(self, text: str) -> bool:
        if text is None:
            return False
        text = text.lower()
        return self.model.predict(self.vectorizer.transform([text]))