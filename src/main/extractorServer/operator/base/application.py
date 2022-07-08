from typing import Type
from src.main.extractorServer.config import Settings


class Application:
    def __init__(self, settings: Type[Settings]):
        self.settings = settings
