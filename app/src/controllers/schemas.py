

from pydantic import BaseModel, Field


class ResultObject(BaseModel):
    floor: int = Field()