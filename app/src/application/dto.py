# -*- coding: utf-8 -*-

from typing import Optional
from dataclasses import dataclass

@dataclass(slots=True)
class Filters:
    agency: Optional[str]
    address: Optional[str]
    

@dataclass(slots=True)
class Cookies:
    consent: str
    hasAuth: str
    authToken: str
    realt_user: str


@dataclass(slots=True)
class RequestParam:
    url: str
    headers: str