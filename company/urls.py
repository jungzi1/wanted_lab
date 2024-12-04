from fastapi import FastAPI
from company.routes import get, post, put, delete


def include_routers(app: FastAPI):
    app.include_router(get.router, tags=["기업 정보 조회"], prefix="")
    app.include_router(post.router, tags=["기업 생성"], prefix="")
    app.include_router(put.router, tags=["기업 정보 수정"], prefix="")
    app.include_router(delete.router, tags=["기업 정보 삭제"], prefix="")
