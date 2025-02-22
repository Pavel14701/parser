# -*- coding: utf-8 -*-

from typing import Generic

from aiohttp import ClientSession

from app.src.infrastructure.types import T


class SessionManager(Generic[T]):

    def __init__(self):
        self.sessions: list[ClientSession] = []

    async def create_session(self) -> ClientSession:
        session = ClientSession()
        self.sessions.append(session)
        return session

    async def close_all_sessions(self) -> None:
        for session in self.sessions:
            if not session.closed:
                await session.close()
        self.sessions = []


def new_request_session_maker() -> SessionManager[ClientSession]:
    return SessionManager()