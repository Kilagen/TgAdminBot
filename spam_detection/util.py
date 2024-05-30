import re
import numpy as np
from natasha import Doc, MorphVocab, Segmenter, NewsEmbedding, NewsMorphTagger

segmenter = Segmenter()
morph_vocab = MorphVocab()

emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)


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

    @staticmethod
    def ru2eng(message: str):
        mapping = {
            'a': 'а',
            'c': 'с',
            'o': 'о',
            't': 'т',
            'k': 'к',
            'u': 'и',
            'x': 'х',
            'e': 'е',
            'b': 'в',
            'm': 'м',
            'h': 'н',
            'p': 'р',
            'y': 'у'
        }
        translation_table = str.maketrans(mapping)

        return message.translate(translation_table)

    @staticmethod
    def lemmatize(message: str):
        message = TextPreprocessor.lower(message)
        message = TextPreprocessor.remove_html_tags(message)
        message = TextPreprocessor.ru2eng(message)

        doc = Doc(message)
        doc.segment(segmenter)
        doc.tag_morph(morph_tagger)
        doc.tokens = [token for token in doc.tokens if token.text.isalpha()]
        for token in doc.tokens:
            token.lemmatize(morph_vocab)
        return ' '.join(token.lemma for token in doc.tokens)

