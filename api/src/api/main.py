import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import FileResponse, JSONResponse

from .clients import database
from .geocode.routes import router as geocode_router
from .listing.routes import router as listing_router
from .settings import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://chat.openai.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(listing_router)
app.include_router(geocode_router)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


### STATIC


@app.get("/logo.png")
async def get_logo():
    return FileResponse("assets/logo.png", media_type="image/png")


@app.get("/.well-known/ai-plugin.json")
async def get_plugin_manifest():
    with open("ai-plugin.json") as f:
        text = f.read()
        text = text.replace("PLUGIN_HOSTNAME", settings.PLUGIN_HOSTNAME)
        data = json.loads(text)
        return JSONResponse(content=data)


@app.get("/.well-known/openapi.yaml")
async def get_plugin_spec():
    openapi_schema_json = get_openapi(
        title="AI Real Estate Agent",
        description="Get stats for apartment listings in San Francisco, California",
        version="v1",
        routes=[*app.routes, *listing_router.routes],
    )
    # openapi_schema_yaml = yaml.dump(openapi_schema_json)

    # return Response(content=openapi_schema_yaml, media_type="application/x-yaml")

    return openapi_schema_json


### DATA


# @app.get("/listings")
# async def get_listings():
#     ...
#
#
# @app.get("/addresses")
# async def get_addresses():
#     ...
