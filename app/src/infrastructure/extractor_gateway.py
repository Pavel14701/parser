# -*- coding: utf-8 -*-

import contextlib
from typing import Optional
import asyncio
import re
from decimal import Decimal

from transliterate import translit
from bs4 import BeautifulSoup
from aiohttp import ClientSession

from app.src.application import interfaces
from app.src.application import dto
from app.src.domain import entities


class HttpParserGateway(interfaces.HttpParser):

    def __init__(self, request_session: ClientSession) -> None:
        self._request_session = request_session

    async def get_data(
            self,
            request_params: dto.RequestParam,
            cookies: Optional[dto.Cookies], 
            filters: Optional[dto.Filters]
        ) -> str:
        with contextlib.suppress(Exception):
            cookies = cookies.to_dict()
        async with self._request_session.get(
            url=request_params.url,
            headers=request_params.headers or None, 
            cookies = cookies or None
        ) as response:
            if response.status == 200:
                return await response.text()
            else:
                await response.raise_for_status()


class DataExtracorGateway(interfaces.DataExtractor):
    
    async def extract_data(self, data: str, request_param: dto.RequestParam) -> entities.ObjectDm:
        results = await asyncio.gather(
            self._find_title(data),
            self._find_prices(data),
            self._find_params(data),
            self._find_description(data),
            self._find_photos(data),
            self._find_geo(data)
        )
        title, prices, params, description, photos, geo = results
        print(geo.street)
        return entities.ObjectDm(
            url=request_param.url,
            build_type=params.build_type,
            year_of_build=params.year_of_build,
            floor=params.floor,
            floors_numb=params.floors_numb,
            rooms=params.rooms,
            separated_rooms=params.separated_rooms,
            all_separated_rooms=params.all_separated_rooms,
            area=params.area,
            living_area=params.living_area,
            kitchen_area=params.kitchen_area,
            repair=params.repair,
            balcony=params.balcony,
            number_balcony=params.number_balcony,
            bath=params.bath,
            price_byn=prices.price_byn,
            price_usd=prices.price_usd,
            price_m2=prices.price_usd//params.area,
            region=geo.region,
            street=geo.street,
            house_number=geo.house_number,
            city_region=geo.city_region,
            city=geo.city,
            micro_region=geo.micro_region,
            latitude=geo.latitude,
            longitude=geo.longitude,
            active=True,
            title=title,
            description=description,
            pictures=photos
            )

    async def _find_title(self, data:str) -> str:
        soup = BeautifulSoup(data, 'lxml')
        return soup.find('h1').text
        
    async def _find_prices(self, data:str) -> entities.Price:
        soup = BeautifulSoup(data, 'lxml')
        if dirty_byn_str := soup.find('h2', class_='text-h2'):
            price_byn_str:str = dirty_byn_str.text
            price_byn_str = price_byn_str.strip()
            price_byn = int(re.sub(r'\D', '', price_byn_str))
        else:
            price_byn = None
        if dirty_usd_str := soup.find('span', class_='text-subhead'):
            price_usd_str:str = dirty_usd_str.text
            price_usd_str = price_usd_str.strip()
            price_usd = Decimal(re.sub(r'\D', '', price_usd_str))
        else:
            price_usd = None
        return entities.Price(
            price_byn=price_byn,
            price_usd=price_usd
        )

    async def _find_params(self, data: str) -> entities.Chars:
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
        params: dict[str, str] = {
            translit(k, 'ru', reversed=True).replace(' ', '_'): v
            for k, v in parameters.items()
        }
        pattern = r'[^\d.]'
        if params["Etazh_/_etazhnost'"]:
            floor, floors_number = map(
                lambda x: int(x.strip()),
                params.get("Etazh_/_etazhnost'").split('/')
            )
        rooms = int(params.get("Kolichestvo_komnat"))
        separated_rooms = int(params.get("Razdel'nyh_komnat", 1))
        return entities.Chars(
            build_type=params.get("Tip_doma"),
            year_of_build=int(params.get("God_postrojki")),
            floor=floor,
            floors_numb=floors_number,
            rooms=rooms,
            separated_rooms=separated_rooms,
            all_separated_rooms=rooms==separated_rooms,
            area=Decimal(self.clean_param(params.get("Ploschad'_obschaja"), pattern)).quantize(Decimal('1.00')),
            living_area=Decimal(self.clean_param(params.get("Ploschad'_zhilaja"), pattern)).quantize(Decimal('1.00')),
            kitchen_area=Decimal(self.clean_param(params.get("Ploschad'_kuhni"), pattern)).quantize(Decimal('1.00')),
            bath=params.get("Sanuzel"),
            balcony=params.get("Balkon"),
            repair=params.get("Remont")
        )

    def clean_param(self, value, pattern, default='0'):
        return re.sub(pattern, '', str(value)) if value is not None else default

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

    async def _find_geo(self, data:str) -> entities.Address:
        soup = BeautifulSoup(data, 'lxml')
        ul_element = soup.find('ul', class_='w-full mb-0.5 -my-1')
        address_info = {}
        for li in ul_element.find_all('li', class_='relative py-1'):
            if span := li.find('span', class_='text-basic'):
                key = span.text.strip()
                if value := li.find('a') or li.find('p'):
                    address_info[key] = value.text.strip()
        address_info = {
            translit(k, 'ru', reversed=True).replace(' ', '_'):
            v for k, v in address_info.items()
        }
        print(address_info)
        latitude, longitude = map(
            lambda x: x.strip(),
            address_info.get("Koordinaty").split(', ')
        )
        return entities.Address(
            house_number=address_info.get("Nomer_doma"),
            street=address_info.get("Ulitsa"),
            region=address_info.get("Oblast'"),
            city=address_info.get("Naselennyj_punkt"),
            city_region=address_info.get("Rajon_goroda"),
            micro_region=address_info.get("Mikrorajon"),
            latitude=Decimal(latitude).quantize(Decimal('1.0000000')),
            longitude=Decimal(longitude).quantize(Decimal('1.0000000'))
        )