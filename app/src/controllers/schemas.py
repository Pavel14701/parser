# -*- coding: utf-8 -*-

from typing import Any, Optional
from decimal import Decimal
from dataclasses import asdict
from uuid import UUID

from pydantic import BaseModel, ValidationInfo, field_validator

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

    class Config:
        json_encoders = {
            Decimal: lambda v: float(v)
        }

class SearchObjectSchema(BaseModel):
    id: str 
    title: str 
    price_usd: int
    region: str
    city: str 
    street: str 
    house_number: str
    area: float 
    living_area: float
    kitchen_area: float 
    floor: int 
    floors_numb: int

    @field_validator('area', 'living_area', 'kitchen_area', mode='wrap')
    def validate_fields(cls, value: Any, info: ValidationInfo) -> float:
        try:
            return float(value)
        except (ValueError, TypeError) as e:
            raise ValueError("Field must be convertible to float") from e

    @classmethod
    def from_dataclass(cls, data: 'SearchResultsDm') -> 'SearchObjectSchema':
        data_dict = asdict(data)
        if isinstance(data_dict['id'], UUID):
            data_dict['id'] = str(data_dict['id'])
        return cls(**data_dict)
