# -*- coding: utf-8 -*-

from typing import Optional

from app.src.domain import entities
from app.src.application import interfaces
from app.src.application import dto


class SaveObject:
    def __init__(
        self,
        parser_gateway: interfaces.HttpParser,
        save_gateway: interfaces.SaveObject,
        db_session: interfaces.DBSession,
    ) -> None:
        self. _parser_gateway = parser_gateway
        self._save_gateway = save_gateway
        self._db_session = db_session

    async def save_object(
            self,
            cookies: Optional[dto.Cookies], 
            request_params: dto.RequestParam,
            filters: dto.Filters
        ) -> entities.ObjectDm:
        _object = await self._parser_gateway.get_data(request_params, filters, cookies)
        object_dm = 
        self._save_gateway.save(object_dm)