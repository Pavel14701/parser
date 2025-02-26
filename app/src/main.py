#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dishka import make_async_container
from dishka.integrations import fastapi as fastapi_integration
from fastapi import FastAPI

from app.src.config import Config
from app.src.controllers.http import Controllers
from app.src.ioc import AppProvider

config = Config()
container = make_async_container(AppProvider(), context={Config: config})

def get_fastapi_app() -> FastAPI:
    app = FastAPI()
    controller = Controllers()
    app.include_router(controller.router)
    fastapi_integration.setup_dishka(container, app)
    return app