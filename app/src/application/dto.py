# -*- coding: utf-8 -*-

from typing import Optional
from dataclasses import dataclass, asdict
from decimal import Decimal


@dataclass(slots=True)
class Filters:
    agency: Optional[str]
    address: Optional[str]


@dataclass(slots=True)
class Cookies:
    consent: Optional[str]
    hasAuth: Optional[str]
    authToken: Optional[str]
    realt_user: Optional[str]

    def to_dict(self):
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass(slots=True)
class RequestParam:
    url: str
    headers: Optional[dict[str, str]]

@dataclass(slots=True)
class DbSearchFilters:
    min_price_usd: Optional[int] = None
    max_price_usd: Optional[int] = None
    build_type: Optional[str] = None
    year_of_build: Optional[int] = None
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
    region: Optional[str] = None
    city: Optional[str] = None
    street: Optional[str] = None
    house_number: Optional[str] = None
    city_region: Optional[str] = None
    micro_region: Optional[str] = None