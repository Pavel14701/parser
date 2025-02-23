# -*- coding: utf-8 -*-

from typing import Protocol, Optional
from abc import abstractmethod

from app.src.domain import entities 


class HttpParser(Protocol):

    @abstractmethod
    async def get_data(self, url: str) -> str:
        ...


class SaveObject(Protocol):

    @abstractmethod
    async def save(self, object: entities.ObjectDm) -> None:
        ...


class ReadObject(Protocol):

    @abstractmethod
    async def read_by_uuid(self, uuid: str) -> Optional[entities.ObjectDm]:
        ...


class HttpParser(Protocol):

    @abstractmethod
    async def get_data(self, url: str) -> str:
        ...


class DBSession(Protocol):

    @abstractmethod
    async def commit(self) -> None:
        ...

    @abstractmethod
    async def flush(self) -> None:
        ...