# -*- coding: utf-8 -*-

from os import environ as env

from pydantic import BaseModel, Field


class DbConfig(BaseModel):
    host: str = Field(alias='DB_HOST')
    port: int = Field(alias='DB_PORT')
    login: str = Field(alias='DB_USER')
    password: str = Field(alias='DB_PASSWORD')
    database: str = Field(alias='DB_DB')


class Config(BaseModel):
    db_config: DbConfig = Field(default_factory=lambda: DbConfig(**env))