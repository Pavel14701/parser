# -*- coding: utf-8 -*-

from typing import Optional
from dataclasses import dataclass


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


@dataclass(slots=True)
class RequestParam:
    url: str
    headers: str