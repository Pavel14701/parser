# -*- coding: utf-8 -*-

from typing import Optional

from app.src.domain import entities
from app.src.application import interfaces
from app.src.application import dto


class SaveObjectInteractor:
    def __init__(
        self,
        parser_gateway: interfaces.HttpParser,
        data_extractor: interfaces.DataExtractor,
        save_gateway: interfaces.SaveObject,
        db_session: interfaces.DbSession,
    ) -> None:
        self. _parser_gateway = parser_gateway
        self._data_extractor = data_extractor
        self._save_gateway = save_gateway
        self._db_session = db_session

    async def save_object(
            self,
            cookies: Optional[dto.Cookies], 
            request_params: dto.RequestParam,
            filters: dto.Filters
        ) -> entities.ObjectDm:
        html_data = await self._parser_gateway.get_data(request_params, filters, cookies)
        object_dm = await self._data_extractor.extract_data(html_data)
        self._save_gateway.save(object_dm)
        self._db_session.commit()