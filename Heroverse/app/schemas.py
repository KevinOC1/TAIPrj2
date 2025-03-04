from pydantic import BaseModel
from typing import Optional

class ComicBase(BaseModel):
    title: str
    image_url: str
    price: float
    stock: int

class ComicCreate(ComicBase):
    pass

class Comic(ComicBase):
    id: int

    class Config:
        from_attributes = True

class ComicUpdate(BaseModel):
    price: Optional[float] = None
    stock: Optional[int] = None