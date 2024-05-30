from base import BaseSpamDetector

import numpy as np

from .util import TextPreprocessor


class MixedAbcDetector(BaseSpamDetector):
    def __init__(self):
        super().__init__()

    def validate(self, text: str) -> bool:
        stats = TextPreprocessor.predict(text)
        if sum(word_stat['lang_switch_count'] >= 2 for word_stat in stats) > 4:
            # so far works fine
            # (even with sum(...) > 0, but removed for lower FP count)
            return True
        if np.mean([word_stat['max'] - word_stat['min'] for word_stat in stats] or [0]) > 60:
            # TODO find better heuristic
            return True
        return False
