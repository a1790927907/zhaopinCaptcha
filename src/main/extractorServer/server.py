from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from src.main.extractorServer.config import Settings
from src.main.extractorServer.config import tags_metadata
from src.main.extractorServer.model import SettingsResponse
from src.main.extractorServer.integration.company.router import router_app as company_router_app


app = FastAPI(docs_url="/zhaopin/company/docs", redoc_url="/zhaopin/company/re_doc", title="漓")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Store Derivation Docs",
        version="1.0.0",
        description="漓",
        routes=app.routes,
        tags=tags_metadata
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
app.include_router(company_router_app)


@app.get(
    "/zhaopin/company/settings", response_model=SettingsResponse, name="获取settings配置", description="获取settings配置",
    tags=["settings"]
)
async def get_settings():
    return {
        "result": Settings.to_dict()
    }


if __name__ == '__main__':
    import uvicorn
    from uvicorn.config import LOGGING_CONFIG
    LOGGING_CONFIG["formatters"]["access"]["fmt"] = '%(asctime)s %(levelprefix)s %(client_addr)s - ' \
                                                    '"%(request_line)s" %(status_code)s'
    uvicorn.run(app, host="0.0.0.0", port=9500)
