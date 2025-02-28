# -*- coding: utf-8 -*-

from os import environ as env

from pydantic import BaseModel, Field


class AppConfig(BaseModel):
    title: str = Field(alias='APP_TITLE')
    version: str = Field(alias='APP_VERSION')
    openapi_url: str = Field(alias='APP_OPENAPI_URL')


class AppStaticConfig(BaseModel):
    url: str = Field(alias='STATIC_URL')
    directory: str = Field(alias='STATIC_DIRECTORY')
    name: str = Field(alias='STATIC_NAME')


class DbConfig(BaseModel):
    host: str = Field(alias='DB_HOST')
    port: int = Field(alias='DB_PORT')
    login: str = Field(alias='DB_USER')
    password: str = Field(alias='DB_PASSWORD')
    database: str = Field(alias='DB_DB')


class Config(BaseModel):
    app_config: AppConfig = Field(default_factory=lambda: AppConfig(**env))
    static_config: AppStaticConfig = Field(default_factory=lambda: AppStaticConfig(**env))
    db_config: DbConfig = Field(default_factory=lambda: DbConfig(**env))