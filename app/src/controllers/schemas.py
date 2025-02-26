# -*- coding: utf-8 -*-

from typing import Optional
from decimal import Decimal
from dataclasses import asdict

from pydantic import BaseModel

from app.src.domain.entities import ObjectDm, SearchResultsDm


class LocationSchema(BaseModel):
    region: Optional[str] = None
    city: Optional[str] = None
    street: Optional[str] = None
    house_number: Optional[str] = None
    city_region: Optional[str] = None
    micro_region: Optional[str] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None


class PriceSchema(BaseModel):
    price_byn: Optional[int] = None
    price_usd: Optional[int] = None
    price_m2: Optional[int] = None


class FlatCharsSchema(BaseModel):
    build_type: Optional[str] = None
    year_of_build: int
    floor: Optional[int] = None
    floors_numb: Optional[int] = None
    rooms: Optional[int] = None
    separated_rooms: Optional[int] = None
    all_separated_rooms: Optional[bool] = None
    area: Optional[Decimal] = None
    living_area: Optional[Decimal] = None
    kitchen_area: Optional[Decimal] = None
    repair: Optional[str] = None
    balcony: Optional[str] = None
    number_balcony: Optional[str] = None
    bath: Optional[str] = None


class ObjectBaseSchema(BaseModel):
    active: Optional[bool] = None
    id: Optional[str] = None
    url: Optional[str] = None
    title: Optional[str] = None

class ObjectSchema(
    ObjectBaseSchema, 
    FlatCharsSchema, 
    PriceSchema,
    LocationSchema
):
    description: Optional[str] = None
    pictures: list[Optional[str]]

    @classmethod
    def from_dataclass(cls, data: 'ObjectDm') -> 'ObjectSchema':
        return cls(**asdict(data))


class SearchObjectSchema:
    id: str 
    title: str 
    price_usd: int
    region: str
    city: str 
    street: str 
    house_number: str
    area: Decimal 
    living_area: Decimal
    kitchen_area: Decimal 
    floor: int 
    floors_numb: int

    @classmethod
    def from_dataclass(cls, data: 'SearchResultsDm') -> 'SearchObjectSchema':
        return cls(**asdict(data))