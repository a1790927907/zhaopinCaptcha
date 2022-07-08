from typing import Type
from src.main.extractorServer.config import Settings
from src.main.extractorServer.operator.company.application import Application as CompanyApplication


class Application:
    def __init__(self, settings: Type[Settings]):
        self.settings = settings
        self.company_app = CompanyApplication(self.settings)


application = Application(Settings)
