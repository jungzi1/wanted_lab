import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware

from company.models import Base
from company.urls import include_routers as company_routers
from config.database import engine

Base.metadata.create_all(bind=engine)
app = FastAPI()


def create_app():
    app = FastAPI(
        title="ADOC API",
        description="ADOC API",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        middleware=[
            Middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
        ],
        swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    )

    company_routers(app)

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
