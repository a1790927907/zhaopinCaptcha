import aiohttp

from typing import Type
from src.main.extractorServer.config import Settings
from src.main.extractorServer.exception import ExtractorServerException
from src.main.extractorServer.external.captcha.model import CaptchaRequestModel, CaptchaResponseModel


class Application:
    def __init__(self, settings: Type[Settings]):
        self.settings = settings

    @staticmethod
    def wrapper_response(response: dict):
        return CaptchaResponseModel(**response)

    @staticmethod
    async def get_company_info_response_callback(res: aiohttp.ClientResponse):
        result: dict = await res.json()
        if res.status != 200:
            raise ExtractorServerException("过验证码 或 获取公司数据失败, 原因: {}".format(
                result.get("message") or "未知原因"
            ), error_code=400)
        return result["result"]

    async def get_company_info(self, request_info: dict) -> CaptchaResponseModel:
        request_info = CaptchaRequestModel(**request_info)
        result = await self.settings.session.post(
            self.settings.extract_info_url,
            json=request_info.dict(), func=self.get_company_info_response_callback,
            ssl=False, timeout=120
        )
        return self.wrapper_response(result)
