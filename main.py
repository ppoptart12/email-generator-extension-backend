from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from OpenAI_script import extensionEmailGenerator
from schemas import (email_schema)
from dotenv import load_dotenv
import os
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)


if os.path.exists(".env"):
    load_dotenv(".env")

app = FastAPI()

MODEL_NAME = 'GmailCopilot'
MODEL_VERSION = 'v24.08.01'

chrome_extension_url = f"chrome-extension://{os.environ["EXTENSION_ID"]}"

origins = [
    chrome_extension_url
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,  # type: ignore
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)  # type: ignore
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,  # type: ignore
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )


@app.get('/health')
def route_health(request: Request):
    res = dict()
    res['GmailCopilot'] = MODEL_VERSION
    res['apiVersion'] = MODEL_NAME + ':' + MODEL_VERSION
    res['statusCode'] = 200
    res['status'] = 'ok'
    res['error'] = None,
    res['message'] = "Gmail Copilot",
    res['isOk'] = True
    return JSONResponse(content=res, status_code=200)


@app.post("/generate_email/")
async def manage_request(user_request: email_schema):
    email_agent = extensionEmailGenerator()

    email = email_agent.generate_email(message=user_request.user_prompt)

    if email:
        return JSONResponse(content=email, status_code=200)
    else:
        return {"error": "Invalid request parameters"}
