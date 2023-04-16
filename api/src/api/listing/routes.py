from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from fastpg.core import Connection

from api.datastore.pinecone import PineconeDataStore
from api.dependencies import get_conn
from api.models.api import (QueryRequest, QueryResponse)
from api.utils import filter_null_params

from .models import Listing
from .service import get_many

# from api.datastore.factory import get_datastore


router = APIRouter(prefix="/listings")

datastore = PineconeDataStore()


@router.get(
    "/search",
    summary="Search though a database of apartment listings in San Francisco, California.",
    description="Query an external api that contains a bunch of attrbutes on apartment listings in San Francisco, California. DO NOT DO ANY MATH WHEN ENTERING THE LATITUDE OR LONGITUDE. There should be no '+' or '-' charagers in the lat/long query parameters.",
    response_description="An array of apartment listings",
    response_model=List[Listing],
)
async def get_listings(
    # client: AsyncClient = Depends(get_client),
    conn: Connection = Depends(get_conn),
    # **kwargs
    *,
    # data: ListingSearchBody = Body(...)
    min_price: float
    | None = Query(
        None,
        title="Minimum Price",
        description="The minimum price of units in an apartment listing",
    ),
    max_price: float
    | None = Query(
        None,
        title="Maximum Price",
        description="The maxium price of units in an apartment listing",
    ),
    min_beds: float
    | None = Query(
        None,
        title="Minimum Beds",
        description="The minimum number of beds a unit can have in this listing. Beds are in increments of 0.5. An apartment with 0 beds is a studio apartment.",
    ),
    max_beds: float
    | None = Query(
        None,
        title="Maximum Beds",
        description="The maximum number of beds a unit can have in this listing. Beds are in increments of 0.5. An apartment with 0 beds is a studio apartment.",
    ),
    min_baths: float
    | None = Query(
        None,
        title="Minimum Baths",
        description="The minimum number of baths a unit can have in this listing. baths are in increments of 0.5.",
    ),
    max_baths: float
    | None = Query(
        None,
        title="Maximum Baths",
        description="The maximum number of baths a unit can have in this listing. baths are in increments of 0.5.",
    ),
    min_lat: float
    | None = Query(
        None,
        title="Minimum Latitude",
        description="The minimum latitude listings can be located at. The value must be a single, floating point number with no mathematical operations appended to it.",
        example=37.674378000701516,
        # regex=r"^\d+\.\d+(?<!\+)\"?$",
    ),
    max_lat: float
    | None = Query(
        None,
        title="Maximum Latitude",
        description="The maximum latitude listings can be located at. The value must be a single, floating point number with no mathematical operations appended to it.",
        example=37.839953487775084,
        # regex=r"^\d+\.\d+(?<!\+)\"?$",
    ),
    min_lng: float
    | None = Query(
        None,
        title="Minimum Longitude",
        description="The minimum longitude listings can be located at. The value must be a single, floating point number with no mathematical operations appended to it.",
        example=-122.60590481125952,
        # regex=r"^\d+\.\d+(?<!\+)\"?$",
    ),
    max_lng: float
    | None = Query(
        None,
        title="Maximum Longitude",
        descripjion="The maximum longitude listings can be located at. The value must be a single, floating point number with no mathematical operations appended to it.",
        max_lng=-122.29519771897436,
        # regex=r"^\d+\.\d+(?<!\+)\"?$",
    ),
):
    params = {
        "min_price": min_price,
        "max_price": max_price,
        "min_beds": min_beds,
        "max_beds": max_beds,
        "min_baths": min_baths,
        "max_baths": max_baths,
        "min_lat": min_lat,
        "max_lat": max_lat,
        "min_lng": min_lng,
        "max_lng": max_lng,
    }
    params = filter_null_params(params)

    recs = await get_many(conn, **params)

    listings = []
    for rec in recs:
        listing = Listing(**rec)
        listings.append(listing)

    return listings


@router.post(
    "/query",
    summary="Semantically search through descriptions of apartment listings",
    description="Query a vector store of embeded descriptions of apartmetns and get the nearest similarity listings based on the query.",
    response_description="An array of apartment listings",
    response_model=QueryResponse,
)
async def query_main(
    request: QueryRequest = Body(...),
):
    try:
        results = await datastore.query(
            request.queries,
        )
        return QueryResponse(results=results)
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal Service Error")
