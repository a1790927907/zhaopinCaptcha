from typing import List
from pydantic import BaseModel, Field


class CaptchaRequestModel(BaseModel):
    url: str = Field(..., description="需要访问的智联招聘公司页面的url")


class NetworkCookieEntity(BaseModel):
    name: str = Field(..., description="cookie name", example="acw_sc__v3")
    value: str = Field(..., description="cookie value", example="xxx")


class CaptchaResponseModel(BaseModel):
    content: str = Field(..., description="智联招聘公司页面html", example="text")
    cookies: List[NetworkCookieEntity] = Field(..., description="cookie info")
    url: str = Field(..., description="页面url", example="xxx")
