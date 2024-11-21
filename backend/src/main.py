from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .uno.app import create_app as create_uno


(uno, load_uno, save_uno) = create_uno()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, Any]:
    load_uno()
    yield
    save_uno()


app = FastAPI(docs_url=None, redoc_url=None,
              openapi_url=None, lifespan=lifespan)

app.add_middleware(CORSMiddleware, allow_origins=["*"])

app.mount("/uno", uno)
