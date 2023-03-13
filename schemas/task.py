from pydantic import BaseModel
from typing import Optional,List
from datetime import  date
# from .user import signUpModel


class TaskModel(BaseModel):
    id:Optional[int]
    title:str
    labels:Optional[int]=1
    start_date:date
    end_date:date
    status:Optional[str]="TO_BE_DONE"
    created_by:Optional[int]
    board_id:Optional[int]
    # assigned_users:List[signUpModel]=None

    class Config:
        orm_mode=True
        schema_extra={
            'example':
            {
                "title":"task1",
                "labels":1,
                "start_date":"2022-1-12",
                "end_date":"2022-10-1",
                "status":"TO_BE_DONE",
            }
        }

class TaskUserModel(BaseModel):
    task:TaskModel
    board_id:int
    pro_id:int
    users:List[int]
    # assigned_users:List[signUpModel]=None

    class Config:
        orm_mode=True
        schema_extra={
            'example':
            {
                "task":{
                    "title":"task1",
                "labels":1,
                "start_date":"2022-1-12",
                "end_date":"2022-10-1",
                "status":"TO_BE_DONE",
                },
                "board_id":1,
                "pro_id":1,
                "users":[1,3]
            }
        }



class AccociationModel(BaseModel):
     user_id:Optional[int]
     task_id:Optional[int]
     class Config:
        orm_mode=True

     
        