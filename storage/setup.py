import os
from storage.config import STORAGE_PATH
DATA_PATH = STORAGE_PATH / "data.sqlite"

def setup():
    os.makedirs(STORAGE_PATH, exist_ok=True)
    DATA_PATH.touch(exist_ok=True)


if __name__ == "__main__":
    setup()
