# -*- coding: utf-8 -*-

from typing import Optional

from app.src.domain.entities import ObjectDm, SearchResultsDm 
from app.src.application import interfaces
from app.src.application import dto


class SaveObjectInteractor:
    def __init__(
        self,
        save_gateway: interfaces.SaveObject,
        db_session: interfaces.DbSession,
        uuid_generator: interfaces.UUIDGenerator
    ) -> None:
        self._save_gateway = save_gateway
        self._db_session = db_session
        self._uuid_generator = uuid_generator

    async def __call__(self, object_dm: ObjectDm) -> None:
        object_dm.id = str(self._uuid_generator())
        await self._save_gateway.save(object_dm)
        await self._db_session.commit()


class GetObjectInteractor:
    def __init__(
        self,
        read_gateway: interfaces.ReadObject
    ) -> None:
        self._read_gateway = read_gateway

    async def __call__(self, id: int) -> Optional[ObjectDm]:
        return await self._read_gateway.read_by_id(id)


class UpdateObjectInteractor:
    def __init__(
        self,
        update_gateway: interfaces.UpdateObject,
        db_session: interfaces.DbSession,
    ) -> None:
        self._update_gateway = update_gateway
        self._db_session = db_session

    async def __call__(self, data: ObjectDm, url: str) -> None:
        await self._update_gateway.update_by_url(data, url)
        await self._db_session.commit()


class DeleteObjectInteractor:
    def __init__(
        self,
        delete_gateway: interfaces.DeleteObject,
        db_session: interfaces.DbSession,
    ) -> None:
        self._delete_gateway = delete_gateway
        self._db_session = db_session

    async def __call__(self, url: str) -> None:
        await self._delete_gateway.delete_by_url(url)
        await self._db_session.commit()

class FindObjectsInteractor:
    def __init__(
        self,
        search_gateway: interfaces.FindObjects
    ) -> None:
        self._search_gateway = search_gateway

    async def __call__(self, params: dto.DbSearchFilters)  -> list[Optional[SearchResultsDm]]:
        return await self._search_gateway.search_objects(params)


class DataParserInteractor:
    def __init__(
        self,
        parser_gateway: interfaces.HttpParser,
        data_extractor: interfaces.DataExtractor,
    ) -> None:
        self. _parser_gateway = parser_gateway
        self._data_extractor = data_extractor

    async def __call__(
        self,
        cookies: Optional[dto.Cookies], 
        filters: Optional[dto.Filters],
        request_params: dto.RequestParam
    ) -> ObjectDm:
        html_data = await self._parser_gateway.get_data(request_params, filters, cookies)
        return await self._data_extractor.extract_data(html_data)