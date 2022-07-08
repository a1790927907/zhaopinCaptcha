from typing import Type
from src.main.extractorServer.config import Settings
from src.main.extractorServer.external.captcha.application import Application as CaptchaApplication


class Application:
    def __init__(self, settings: Type[Settings]):
        self.settings = settings
        self.captcha_app = CaptchaApplication(self.settings)


application = Application(Settings)
