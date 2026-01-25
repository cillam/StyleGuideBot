from contextlib import AsyncExitStack
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware


from backend.style_guide import lifespan_mechanism, sub_application_style_guide

description = """
StyleGuideBot app is a FastAPI application that supports the following endpoints:
* bot/health
* bot/query
* /docs
* /openapi.json
* bot/docs
* bot/openapi.json
"""


async def main_lifespan(app: FastAPI):
    async with AsyncExitStack() as stack:
        # Manage the lifecycle of sub_app
        await stack.enter_async_context(
            lifespan_mechanism(sub_application_style_guide)
        )
        yield


app = FastAPI(lifespan=main_lifespan, description=description)


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000", 
        "https://prod.d353zsakgfdtx.amplifyapp.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/bot", sub_application_style_guide)