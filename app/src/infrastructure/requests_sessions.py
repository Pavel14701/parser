# -*- coding: utf-8 -*-

from contextlib import asynccontextmanager

from aiohttp import ClientSession


class SessionManager:

    def __init__(self):
        self.sessions: dict[int, ClientSession] = {}

    async def create_session(self) -> str:
        session = ClientSession()
        session_id = id(session)
        self.sessions[session_id] = session
        return session_id

    async def close_session(self, session_id: str) -> None:
        session: ClientSession
        if session := self.sessions.pop(session_id, None):
            await session.close()

    async def close_all_sessions(self) -> None:
        for session_id, session in self.sessions.items():
            await session.close()
        self.sessions.clear()

    @asynccontextmanager
    async def manage_sessions(self):
        try:
            session_id = await self.create_session()
            yield self
        finally:
            await self.close_session(session_id) 