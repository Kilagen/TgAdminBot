import typing as tp
from abc import ABC, abstractmethod


class BaseSpamDetector(ABC):
    def __init__(self):
        self._next: tp.Optional[BaseSpamDetector] = None

    async def __call__(self, text: str) -> bool:
        if self.validate(text):
            return True
        if self._next is not None:
            return await self._next(text)
        return False

    @abstractmethod
    def validate(self, text: str) -> bool:
        pass

    def set_next(self, next_detector: 'BaseSpamDetector') -> 'BaseSpamDetector':
        self._next = next_detector
        return next_detector
