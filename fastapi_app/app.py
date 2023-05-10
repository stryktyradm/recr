from main.routes import router as main_router
from fastapi import FastAPI


def include_router(app):
    app.include_router(main_router, prefix="", include_in_schema=False)


def start_application():
    app = FastAPI()
    include_router(app)
    return app


app = start_application()
