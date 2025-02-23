# -*- coding: utf-8 -*-

from typing import Optional, Union
from decimal import Decimal
from dataclasses import dataclass


@dataclass(slots=True)
class Geo:
    latitude: Decimal
    longitude: Decimal


@dataclass(slots=True)
class Address:
    region: str
    city: str
    street: str
    house_number: str
    city_region: Optional[str]
    micro_region: Optional[str]
    geo: Geo


@dataclass(slots=True)
class Chars:
    build_type: str
    year_of_build: int
    m2_price: int
    floor: Optional[int]
    floor_numb: Optional[int]
    rooms: int
    separated_rooms: int
    all_separated_rooms: bool
    area: float
    kitchen_area: float
    bath_area: Optional[float] 
    rooms_area: Union[list[float]|float|None]
    repair: Optional[str]
    balcony: str
    number_balcony: Optional[str]


@dataclass(slots=True)
class ObjectDm:
    active: bool
    id: int
    url: str
    address: str
    address_desc: Address 
    title: str
    price: int
    description: str
    pictures: Optional[list[str]]
    chars: Chars

