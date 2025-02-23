# -*- coding: utf-8 -*-

from typing import Optional
from dataclasses import dataclass, asdict


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
    headers: dict[str, str]