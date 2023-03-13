from pydantic import BaseModel
from typing import Optional
from datetime import  date

class BoardModel(BaseModel):
    id:Optional[int]
    title:str
    user_id:Optional[int]
    proj_id:Optional[int]

    class Config:
        orm_mode=True
        schema_extra={
            'example':{
                "title":"board1",
            }
        }
