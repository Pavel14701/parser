# -*- coding: utf-8 -*-

from typing import Protocol, Optional
from abc import abstractmethod
from uuid import UUID

from app.src.domain import entities 
from app.src.application.dto import DbSearchFilters, RequestParam, Cookies, Filters

class HttpParser(Protocol):

    @abstractmethod
    async def get_data(self, url: str) -> str:
        ...


class DataExtractor(Protocol):

    @abstractmethod
    async def extract_data(self, data: str, request_params: RequestParam) -> entities.ObjectDm:
        ...


class SaveObject(Protocol):

    @abstractmethod
    async def save(self, object: entities.ObjectDm) -> None:
        ...


class ReadObject(Protocol):

    @abstractmethod
    async def read_by_id(self, id: int) -> Optional[entities.ObjectDm]:
        ...


class UpdateObject(Protocol):

    @abstractmethod
    async def update_by_url(self, data: entities.ObjectDm, url: str) -> None:
        ...


class DeleteObject(Protocol):

    @abstractmethod
    async def delete_by_url(self, url: str) -> None:
        ...


class FindObjects(Protocol):

    @abstractmethod
    async def search_objects(self, object: DbSearchFilters) -> list[Optional[entities.SearchResultsDm]]:
        ...


class HttpParser(Protocol):

    @abstractmethod
    async def get_data(
        self,
        request_params: RequestParam,
        cookies: Optional[Cookies], 
        filters: Optional[Filters]
    ) -> str:
        ...


class DbSession(Protocol):

    @abstractmethod
    async def commit(self) -> None:
        ...

    @abstractmethod
    async def flush(self) -> None:
        ...


class UUIDGenerator(Protocol):
    def __call__(self) -> UUID:
        ...