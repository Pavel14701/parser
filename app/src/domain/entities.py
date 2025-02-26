# -*- coding: utf-8 -*-

from typing import Optional
from decimal import Decimal
from dataclasses import dataclass


@dataclass(slots=True)
class Address:
    region: str
    city: str
    street: str
    house_number: str
    city_region: Optional[str] = None
    micro_region: Optional[str] = None
    latitude: Decimal
    longitude: Decimal


@dataclass(slots=True)
class Price:
    price_byn: int
    price_usd: int
    price_m2: Optional[int] = None


@dataclass(slots=True)
class Chars:
    build_type: str
    year_of_build: int
    floor: Optional[int] = None
    floors_numb: Optional[int] = None
    rooms: int
    separated_rooms: int
    all_separated_rooms: bool
    area: Decimal
    living_area: Decimal
    kitchen_area: Decimal
    repair: Optional[str] = None
    balcony: str
    number_balcony: Optional[str] = None
    bath: str


@dataclass(slots=True)
class ObjectDm(Address, Price, Chars):
    active: bool
    id: Optional[str] = None
    url: Optional[str] = None
    title: str
    description: str
    pictures: list[Optional[str]]


@dataclass(slots=True)
class SearchResultsDm:
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