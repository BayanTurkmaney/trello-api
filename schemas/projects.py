from pydantic import BaseModel
from typing import Optional
from datetime import  date

class ProjectModel(BaseModel):
    id: Optional[int]
    title:str
    project_code:str
    start_date: date
    end_date: date
    user_id: Optional[int]

    class Config:
        orm_mode=True
        schema_extra={
            'example':{
                "title":"pro1",
                "project_code":"FF0201",
                "start_date":12-1-2022,
                "end_date":10-2-2022
            }
        }
