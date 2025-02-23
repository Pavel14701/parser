# -*- coding: utf-8 -*-

from typing import AsyncIterable, Iterable

from aiohttp import ClientSession
from dishka import Provider, Scope, provide, from_context
from sqlalchemy.orm import Session, sessionmaker

from app.src.config import Config
from app.src.infrastructure.database import new_session_maker
from app.src.infrastructure.requests_sessions import SessionManager


class AppProvider(Provider):

    @provide(scope=Scope.APP)
    def get_session_maker(
        self, 
        config: Config
    ) -> sessionmaker[Session]:
        return new_session_maker(config.db_config)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, 
        session_maker: sessionmaker[Session]
    ) -> AsyncIterable[Session]:
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