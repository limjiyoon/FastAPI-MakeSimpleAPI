from fastapi import FastAPI
from fastapi_makesimpleapi.simple_controller import router


app = FastAPI()
app.include_router(router)
