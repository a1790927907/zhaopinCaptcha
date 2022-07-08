import os
import json
import asyncio
import aiohttp
from src.main.utils.custom_aiohttp_session import HoMuraSession


tags_metadata = [
    {
        "name": "company",
        "description": "智联招聘公司信息"
    },
    {
        "name": "settings",
        "description": "获取配置信息"
    }
]


class Settings:
    author: str = "zyh"
    version: str = "1.0.0"
    description: str = "别害怕, 男神在你身旁"
    captcha_server: str = os.getenv("CAPTCHA_SERVER", "http://localhost:9000")
    extract_info_url: str = captcha_server + "/api/zhaopin/company/info"
    session: HoMuraSession = HoMuraSession(
        aiohttp.ClientSession, retry_when=lambda x: not isinstance(x, asyncio.exceptions.TimeoutError), retry_interval=3
    )

    @classmethod
    def to_dict(cls):
        return {key: getattr(cls, key, None).__str__() for key, value in cls.__annotations__.items()}

    @classmethod
    def to_json(cls):
        return json.dumps(cls.to_dict(), ensure_ascii=False)
