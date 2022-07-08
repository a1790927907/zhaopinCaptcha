from loguru import logger
from fastapi import APIRouter, Query, Response
from src.main.extractorServer.exception import ExtractorServerException
from src.main.extractorServer.integration.company.model import CompanyInfoResponse
from src.main.extractorServer.operator.application import application as operator_app


router_app = APIRouter(tags=["company"], prefix="/api/zhaopin/extract")


@router_app.get(
    "/company", response_model=CompanyInfoResponse, name="根据 公司页面url 获取对应页面的html",
    description="根据 公司页面url 获取对应页面的html"
)
async def extract_company_info(
        response: Response,
        url: str = Query(..., description="url", example="https://www.zhaopin.com/companydetail/CZ305638710.htm")
):
    try:
        result = await operator_app.company_app.extract(url)
        return result
    except ExtractorServerException as e:
        logger.error(e.message)
        message = e.message
        response.status_code = e.error_code
    except Exception as e:
        logger.exception(e)
        message = repr(e)
        response.status_code = 500
    return {
        "message": message
    }
