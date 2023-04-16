from typing import List, Optional, Union

from pydantic import BaseModel


class Properties(BaseModel):
    accuracy: Optional[str]
    address: Optional[str]
    category: Optional[str]
    maki: Optional[str]
    wikidata: Optional[str]
    short_code: Optional[str]
    landmark: Optional[bool]
    tel: Optional[str]


class Geometry(BaseModel):
    type: str
    coordinates: List[float]
    interpolated: Optional[bool]
    omitted: Optional[bool]


class RoutablePoints(BaseModel):
    points: Optional[List[dict]]


class Feature(BaseModel):
    id: str
    type: str
    place_type: List[str]
    relevance: float
    address: Optional[str]
    properties: Properties
    text: str
    place_name: str
    matching_text: Optional[str]
    matching_place_name: Optional[str]
    text_language: Optional[str]
    place_name_language: Optional[str]
    language: Optional[str]
    language_language: Optional[str]
    bbox: Optional[List[float]]
    center: List[float]
    geometry: Geometry
    context: Optional[List[dict]]
    routable_points: Optional[RoutablePoints]


class GeocodingApiResponse(BaseModel):
    type: Optional[str]  # Make type field optional
    query: Optional[List[Union[str, float]]]  # Make query field optional
    features: Optional[List[Feature]]  # Make features field optional
    attribution: Optional[str]  # Make attribution field optional
