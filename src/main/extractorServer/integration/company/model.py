from typing import Optional
from typing_extensions import Literal
from pydantic import BaseModel, Field
from src.main.extractorServer.frame.response.model import BaseResponse


class CompanyInfoResult(BaseModel):
    content: str = Field(..., description="页面html", example="<div></div>")
    type: Literal['internal', 'external'] = Field(
        ..., description="internal代表直接根据cookie获取, external代表是从captcha验证码服务获取", example="internal"
    )
    cookie: str = Field(..., description="cookie info", example="a=1; b=2")


class CompanyInfoResponse(BaseResponse):
    result: Optional[CompanyInfoResult] = Field(default=None, description="company info result")
