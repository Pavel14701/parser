# -*- coding: utf-8 -*-

from aiohttp import ClientSession
from typing import TypeVar

T = TypeVar('T', bound=ClientSession)