import aiohttp

from pyquery import PyQuery
from typing import Type, Dict, cast
from typing_extensions import Literal
from src.main.extractorServer.config import Settings
from src.main.extractorServer.exception import ExtractorServerException
from src.main.extractorServer.external.application import application as external_app
from src.main.extractorServer.operator.base.application import Application as BaseApplication


class Application(BaseApplication):
    def __init__(self, settings: Type[Settings]):
        super().__init__(settings)
        self.core_cookies: Dict[str, str] = {}

    @property
    def cookies(self):
        _cookies = ["{}={}".format(name, value) for name, value in self.core_cookies.items()]
        return "; ".join(_cookies)

    def reset_cookie(self):
        self.core_cookies = {}

    async def get_and_reset_core_cookies(self, url: str):
        result = await external_app.captcha_app.get_company_info({"url": url})
        for cookie in result.cookies:
            self.core_cookies[cookie.name] = cookie.value
        return result

    async def get_cookies(self, url: str):
        if not self.cookies:
            await self.get_and_reset_core_cookies(url)
        return self.cookies

    @staticmethod
    def is_company_page(text: str) -> bool:
        selector = PyQuery(text)
        return bool(selector(".mian-company"))

    @staticmethod
    async def get_company_info_response_callback(res: aiohttp.ClientResponse):
        response = await res.text()
        return response

    async def get_company_info(
            self, url: str, *, retry_time: int = 0, result_type: Literal['internal', 'external'] = "internal"
    ):
        """
        直接通过cookie获取html页面 出现验证码的话 至多会尝试解两次验证码
        :param url:
        :param retry_time:
        :param result_type:
        :return:
        """
        cookies = await self.get_cookies(url)
        response: str = await self.settings.session.get(
            url, headers={
                "cookie": cookies
            }, func=self.get_company_info_response_callback, ssl=False, timeout=20
        )
        if not self.is_company_page(response):
            if retry_time <= 1:
                self.reset_cookie()
                result = await self.get_company_info(url, retry_time=retry_time + 1, result_type="external")
            else:
                raise ExtractorServerException(
                    "重试获取cookie达到最大次数 均为无效cookie 检查captcha server是否出现问题", error_code=400
                )
        else:
            result = {"content": response, "type": result_type, "cookie": self.cookies}
        return result

    async def _extract(self, url: str):
        result = await self.get_company_info(
            url, result_type=cast(Literal['internal', 'external'], "internal" if self.cookies else "external")
        )
        return result

    async def extract(self, url: str):
        result = await self._extract(url)
        return {
            "result": result
        }
