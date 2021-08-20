from pydantic import BaseModel
from typing import Optional


class ModelBaseDto(BaseModel):
    id: Optional[int]

    class Config:
        orm_mode = True