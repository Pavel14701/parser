# -*- coding: utf-8 -*-

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from app.src.config import DbConfig


def new_session_maker(config: DbConfig) -> async_sessionmaker[AsyncSession]:
    database_uri = "postgresql+psycopg://{login}:{password}@{host}:{port}/{database}".format(
        login=config.login,
        password=config.password,
        host=config.host,
        port=config.port,
        database=config.database,
    )
    engine = create_async_engine(
        database_uri,
        pool_size=15,
        max_overflow=15,
        connect_args={
            "connect_timeout": 5,
        },
    )
    return async_sessionmaker(engine, class_=AsyncSession, autoflush=False, expire_on_commit=False)