# -*- coding: utf-8 -*-

from pydantic import BaseModel, Field


class ResultObject(BaseModel):
    floor: int