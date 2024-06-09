import typing as tp
import json
import os

from spam_detection import MixedAbcDetector, LogRegDetector

detector = MixedAbcDetector()
detector.set_next(LogRegDetector())


def read_text_messages(fpath) -> tp.Iterable:
    for message in json.load(open(fpath, 'r'))["messages"]:
        text = ''.join(entity["text"] for entity in message["text_entities"])
        if text != "":
            yield text


def validate_model():
    folder_path = os.path.dirname(os.path.abspath(__file__)) + "/./validation/chat_dumps"
    for file in os.listdir(folder_path):
        if file.endswith('.json'):
            fpath = folder_path + "/" + file
            total_count = 0
            false_positives = []
            for message in read_text_messages(fpath):
                total_count += 1
                if detector(message):
                    false_positives.append(message)
            print(len(false_positives), "/", total_count)
            print(false_positives)


if __name__ == '__main__':
    validate_model()
