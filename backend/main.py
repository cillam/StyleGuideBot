from contextlib import AsyncExitStack

from fastapi import FastAPI

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


app.mount("/bot", sub_application_style_guide)


# /docs endpoint is defined by FastAPI automatically
# /openapi.json returns a json object automatically by FastAPI