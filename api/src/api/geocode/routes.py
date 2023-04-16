import json

from fastapi import APIRouter, Depends, Query
from httpx import AsyncClient

from api.dependencies import get_client
from api.settings import settings
from api.utils import filter_null_params

from .models import GeocodingApiResponse

router = APIRouter(prefix="/geocode")


min_lng = -122.60590481125952
max_lng = -122.29519771897436
min_lat = 37.674378000701516
max_lat = 37.839953487775084


@router.get(
    "/forward_search",
    summary="The forward geocoding query type allows you to look up a single location by name and returns its geographic coordinates.",
    description="",
    response_description="The API response for a forward geocoding query returns a GeoJSON feature collection in Mapbox Geocoding Response format.",
    response_model=GeocodingApiResponse,
)
async def geocode_forward_search(
    client: AsyncClient = Depends(get_client),
    *,
    search_text: str = Query(
        ...,
        title="Search Text",
        description="The feature you’re trying to look up. This could be an address of a business, a point of interest name, a neighborhood name, etc. This should never be an address to an actual apartment listing. When searching for points of interest, it can also be a category name (for example, “coffee shop”). The search text should be expressed as a URL-encoded UTF-8 string, and must not contain the semicolon character (either raw or URL-encoded). Your search text should only be a few words. Use the proximity query param if you need to look up features near some listing.",
        examples={
            "coffee shops": {
                "summary": "Look for coffe shops. If specifying near a location, use the proximity query parameter to specify that location's LatLong.",
                "value": "coffee shops",
            }
        },
    ),
    proximity: str
    | None = Query(
        None,
        title="LatLong Center",
        description="Bias the response to favor results that are closer to this location. Provided as two comma-separated coordinates in longitude,latitude order. Typically you would input that LatLong of a listing here to find whatever points of interest are around it.",
        example="37.766311,-122.443408",
    ),
):
    params = {
        "access_token": settings.MAPBOX_TOKEN,
        "bbox": f"{min_lng},{min_lat},{max_lng},{max_lat}",
        "proximity": proximity,
        "limit": 3,
    }
    params = filter_null_params(params)

    res = await client.get(
        f"https://api.mapbox.com/geocoding/v5/mapbox.places/{search_text}.json",
        params=params,
    )
    data = json.loads(res.content.decode())
    feature_collection = GeocodingApiResponse(**data)

    return feature_collection
