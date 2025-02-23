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


class DataExtracorGateway(interfaces.DataExtractor):
    def __init__(self) -> None:
        pass

    async def extract_data(self, data: str) -> entities.ObjectDm:
        results = await asyncio.gather(
            self._find_title(data),
            self._find_prices(data),
            self._find_params(data),
            self._find_description(data),
            self._find_photos(data)
        )
        title, prices, params, description, photos = results
        return {
            "title": title,
            "prices": prices,
            "params": params,
            "description": description,
            "photos": photos
        }

    async def _find_title(self, data:str) -> str:
        soup = BeautifulSoup(data, 'lxml')
        return soup.find('h1')
        
    async def _find_prices(self, data:str) -> tuple:
        soup = BeautifulSoup(data, 'lxml')
        if dirty_byn_str := soup.find('h2', class_='text-h2'):
            price_byn_str:str = dirty_byn_str.text
            price_byn_str = price_byn_str.strip()
            price_byn = int(re.sub(r'\D', '', price_byn_str))
        if dirty_usd_str := soup.find('span', class_='text-subhead'):
            price_usd_str:str = dirty_usd_str.text
            price_usd_str = price_usd_str.strip()
            price_usd = int(re.sub(r'\D', '', price_usd_str))
        return (price_byn, price_usd)

    async def _find_params(self, data: str) -> dict[str, str]:
        soup = BeautifulSoup(data, 'lxml')
        li_elements = soup.select('ul.w-full.-my-1 > li')
        parameters = {}
        for li in li_elements:
            dirty_param_name: str = li.find('span').text
            param_name = dirty_param_name.strip()
            if ext_param_value := li.find('p'):
                dirty_param_value: str = ext_param_value.text
                param_value = dirty_param_value.strip()
                parameters[param_name] = param_value
        return {
            translit(k, 'ru', reversed=True).replace(' ', '_'): v
            for k, v in parameters.items()
        }

    async def _find_description(self, data:str) -> str:
        soup = BeautifulSoup(data, 'lxml')
        section = soup.find(
            name='section', 
            class_='bg-white flex flex-wrap md:p-6 my-4 rounded-md'
        )
        dirty_description: str = section.find(
            name='div', 
            class_='description_wrapper__tlUQE'
        ).text
        return dirty_description.strip()

    async def _find_photos(self, data:str) -> tuple[str]:
        soup = BeautifulSoup(data, 'lxml')
        swiper_wrapper = soup.find(
            name='div',
            class_='swiper-wrapper'
        )
        img_tags = swiper_wrapper.find_all('img')
        return (
            img['src'] for img in img_tags
            if 'src' in img.attrs and
            img['src'].endswith('.jpg')
        )
