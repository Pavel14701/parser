# -*- coding: utf-8 -*-

from typing import AsyncGenerator
from contextlib import asynccontextmanager

from aiohttp import ClientSession


class SessionManager:

    def __init__(self):
        self.sessions: dict[int, ClientSession] = {}

    async def create_session(self) -> tuple[int, ClientSession]:
        session = ClientSession()
        session_id = id(session)
        self.sessions[session_id] = session
        return session_id, session

    async def close_session(self, session_id: int) -> None:
        session: ClientSession
        if session := self.sessions.pop(session_id, None):
            await session.close()

    async def close_all_sessions(self) -> None:
        for session_id, session in self.sessions.items():
            await session.close()
        self.sessions.clear()

    @asynccontextmanager
    async def manage_sessions(self) -> AsyncGenerator[ClientSession, None]:
        session_id, session = await self.create_session()
        try:
            yield session
        finally:
            await self.close_session(session_id)
