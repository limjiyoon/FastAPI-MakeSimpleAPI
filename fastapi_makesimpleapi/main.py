from fastapi import FastAPI
from fastapi_makesimpleapi.simple_controller import router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    return app


app = create_app()
