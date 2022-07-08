from typing import Dict
from pydantic import Field
from src.main.extractorServer.frame.response.model import BaseResponse


class SettingsResponse(BaseResponse):
    result: Dict[str, str] = Field(..., description="settings response")
