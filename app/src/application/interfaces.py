# -*- coding: utf-8 -*-

from typing import Protocol, Optional
from abc import abstractmethod

from app.src.domain import entities 
from app.src.application.dto import DbSearchFilters

class HttpParser(Protocol):

    @abstractmethod
    async def get_data(self, url: str) -> str:
        ...


class DataExtractor(Protocol):

    @abstractmethod
    async def extract_data(self, data: str) -> entities.ObjectDm:
        ...


class SaveObject(Protocol):

    @abstractmethod
    async def save(self, object: entities.ObjectDm) -> None:
        ...


class FindObjects(Protocol):

    @abstractmethod
    async def save(self, object: DbSearchFilters) -> tuple[entities.SearchResultsDm, ...]:
        ...


class ReadObject(Protocol):

    @abstractmethod
    async def read_by_uuid(self, uuid: str) -> Optional[entities.ObjectDm]:
        ...


class HttpParser(Protocol):

    @abstractmethod
    async def get_data(self, url: str) -> str:
        ...


class DbSession(Protocol):

    @abstractmethod
    async def commit(self) -> None:
        ...

    @abstractmethod
    async def flush(self) -> None:
        ...