# -*- coding: utf-8 -*-

from typing import AsyncIterable

from aiohttp import ClientSession
from dishka import Provider, Scope, provide, AnyOf, from_context
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.src.config import Config
from app.src.application import interfaces
from app.src.application.interactors import (
    SaveObjectInteractor,
    GetObjectInteractor,
    FindObjectsInteractor
)
from app.src.infrastructure.database import new_session_maker
from app.src.infrastructure.requests_sessions import SessionManager
from app.src.infrastructure.gateways import ObjectsGateway 

class AppProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_session_maker(
        self, 
        config: Config
    ) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config.db_config)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, 
        session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AnyOf[AsyncSession, interfaces.DbSession]]:
        async with session_maker() as session:
            yield session

    @provide(scope=Scope.APP)
    def get_reuest_session_maker(
        self
    ) -> SessionManager:
        return SessionManager()

    @provide(scope=Scope.REQUEST)
    async def get_client_session(
        self,
        session_maker: SessionManager
    ) -> AsyncIterable[ClientSession]:
        async with session_maker as session:
            yield session

    object_gateway = provide(
        ObjectsGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[
            interfaces.SaveObject, 
            interfaces.ReadObject, 
            interfaces.FindObjects
        ]
    )

    get_object_interactor = provide(GetObjectInteractor, scope=Scope.REQUEST)
    create_new_object_interactor = provide(SaveObjectInteractor, scope=Scope.REQUEST)
    find_objects_interactor = provide(FindObjectsInteractor, scope=Scope.REQUEST)