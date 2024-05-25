from base import BaseSpamDetector


class MixedAbcDetector(BaseSpamDetector):
    def __init__(self):
        super().__init__()

    async def _validate(self, text: str) -> bool:
        pass
