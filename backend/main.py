from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from core.configs import settings
from api.v1.api import api_router


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    allow_credentials=True
)

app.contact = {
    "name": "E-mail",
    "email": "josereinaldo.pessoal@gmail.com",
}

app.license_info = {
    "name": "MIT License",
    "url": "https://opensource.org/licenses/MIT",
}

app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=4000, log_level="info", reload=True)