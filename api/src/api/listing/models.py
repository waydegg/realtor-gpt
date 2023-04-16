from enum import Enum
from typing import List
from uuid import UUID

from pydantic import BaseModel, Field


class City(Enum):
    SAN_FRANCISCO = "san_francisco"


class State(Enum):
    CA = "california"


class ListingSearchBody(BaseModel):
    min_price: float | None = Field(
        None,
        title="Minimum Price",
        description="The minimum price of units in an apartment listing",
    )
    max_price: float = Field(
        None,
        title="Maximum Price",
        description="The maxium price of units in an apartment listing",
    )
    min_beds: float = Field(
        None,
        title="Minimum Beds",
        description="The minimum number of beds a unit can have in this listing. Beds are in increments of 0.5. An apartment with 0 beds is a studio apartment.",
    )
    max_beds: float = Field(
        None,
        title="Maximum Beds",
        description="The maximum number of beds a unit can have in this listing. Beds are in increments of 0.5. An apartment with 0 beds is a studio apartment.",
    )
    min_baths: float = Field(
        None,
        title="Minimum Baths",
        description="The minimum number of baths a unit can have in this listing. Baths are in increments of 0.5.",
    )
    max_baths: float = Field(
        None,
        title="Maximum Baths",
        description="The maximum number of baths a unit can have in this listing. Baths are in increments of 0.5.",
    )
    min_lat: float = Field(
        None,
        title="Minimum Latitude",
        description="The minimum latitude listings can be located at.",
        example=37.674378000701516,
    )
    max_lat: float = Field(
        None,
        title="Maximum Latitude",
        description="The maximum latitude listings can be located at.",
        example=37.839953487775084,
    )
    min_lng: float = Field(
        None,
        title="Minimum Longitude",
        description="The minimum longitude listings can be located at.",
        example=-122.60590481125952,
    )
    max_lng: float = Field(
        None,
        title="Maximum Longitude",
        description="The maximum longitude listings can be located at.",
        example=-122.29519771897436,
    )


class Platform(Enum):
    ZILLOW = "zillow"
    CRAIGSLIST = "craigslist"
    APARTMENTS = "apartments"


class Listing(BaseModel):
    id: UUID
    platform: Platform
    platform_url: str
    latitude: float
    longitude: float
    price: float
    area: float | None
    beds: float | None
    baths: float | None
    available: bool | None
    description: str | None
    address_line_1: str
    postal_code: str
    city: City
    state: State
    listing_images: List[str]
    address_images: List[str]
