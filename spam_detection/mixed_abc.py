from base import BaseSpamDetector

import re
import numpy as np


class TextPreprocessor:
    def __init__(self):
        pass

    @staticmethod
    def remove_html_tags(text: str):
        # Define a regex pattern for HTML tags
        html_tag_pattern = re.compile(r'<[^>]+>')

        # Substitute HTML tags with an empty string
        cleaned_text = html_tag_pattern.sub('', text)
        return cleaned_text

    @staticmethod
    def lower(text: str):
        return text.lower()

    @staticmethod
    def get_word_stats(alphas: list[int]):
        arr = np.array(alphas)
        return {
            'std': arr.std(),
            'min': arr.min(),
            'max': arr.max(),
            'mean': arr.mean(),
            'count': arr.size,
            'diff': sum(np.abs(arr[1:] - arr[:-1]) ** 2, start=0),
            'lang_switch_count': sum(np.abs(arr[1:] - arr[:-1]) > 200, start=0)
        }

    @staticmethod
    def get_msg_stats(message: str):
        stats = []
        buffer = []
        for i in message:
            if str.isalpha(i):
                buffer.append(ord(i))
            elif buffer:
                stats.append(TextPreprocessor.get_word_stats(buffer))
                buffer = []
        if buffer:
            stats.append(TextPreprocessor.get_word_stats(buffer))
        return stats

    @staticmethod
    def predict(message: str):
        message = TextPreprocessor.lower(message)
        message = TextPreprocessor.remove_html_tags(message)
        stats = TextPreprocessor.get_msg_stats(message)
        return stats


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
