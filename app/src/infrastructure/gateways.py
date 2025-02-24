# -*- coding: utf-8 -*-

import asyncio
import re
from typing import Optional

from aiohttp import ClientSession
from transliterate import translit
from bs4 import BeautifulSoup

from app.src.application import interfaces
from app.src.application import dto
from app.src.domain import entities


class HttpParserGateway(interfaces.HttpParser):

    def __init__(self, request_session: ClientSession) -> None:
        self._request_session = request_session

    async def get_data(
            self,
            cookies: Optional[dto.Cookies], 
            request_params: dto.RequestParam,
        ) -> str:
        async with self._request_session.get(
            url=request_params.url,
            headers=request_params.headers, 
            cookies = cookies.to_dict()
        ) as response:
            if response.status == 200:
                return await response.text()
            else:
                await response.raise_for_status()


