from fastapi import FastAPI
from interfaces.api.init import router

app = FastAPI(title="Ivanov API")

app.include_router(router)
