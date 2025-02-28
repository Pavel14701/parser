# -*- coding: utf-8 -*-

from typing import Optional, List
from decimal import Decimal
from dataclasses import dataclass, field

@dataclass(slots=True)
class Address:
    region: str
    city: str
    street: str
    house_number: str
    latitude: Decimal
    longitude: Decimal
    city_region: Optional[str] = field(default=None)
    micro_region: Optional[str] = field(default=None)

@dataclass(slots=True)
class Price:
    price_byn: int
    price_usd: int
    price_m2: Optional[int] = field(default=None)

@dataclass(slots=True)
class Chars:
    build_type: str
    year_of_build: int
    rooms: int
    separated_rooms: int
    all_separated_rooms: bool
    bath: str
    area: Decimal
    living_area: Decimal
    kitchen_area: Decimal
    balcony: str
    floor: Optional[int] = field(default=None)
    floors_numb: Optional[int] = field(default=None)
    repair: Optional[str] = field(default=None)
    number_balcony: Optional[str] = field(default=None)

@dataclass(slots=True)
class ObjectDm:
    #Adress
    region: str
    city: str
    street: str
    house_number: str
    latitude: Decimal
    longitude: Decimal
    #Price
    price_byn: int
    price_usd: int
    #Chars
    build_type: str
    year_of_build: int
    rooms: int
    separated_rooms: int
    all_separated_rooms: bool
    bath: str
    area: Decimal
    living_area: Decimal
    kitchen_area: Decimal
    balcony: str
    #Object
    active: bool
    title: str
    description: str
    #Adress with None
    city_region: Optional[str] = field(default=None)
    micro_region: Optional[str] = field(default=None)
    #Price with None
    price_m2: Optional[int] = field(default=None)
    #Chars with None
    floor: Optional[int] = field(default=None)
    floors_numb: Optional[int] = field(default=None)
    repair: Optional[str] = field(default=None)
    number_balcony: Optional[str] = field(default=None)
    #Object with None
    pictures: List[Optional[str]] = field(default_factory=[])
    id: Optional[str] = field(default=None)
    url: Optional[str] = field(default=None)


@dataclass
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
