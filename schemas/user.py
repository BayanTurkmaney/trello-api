from pydantic import BaseModel
from typing import Optional,List
from .task import TaskModel

class signUpModel(BaseModel):
    id: Optional[int]
    name: str
    email: str
    password: str
    is_admin: Optional[bool]
    role: Optional[str]="DEVELOPER"
    # assigned_tasks:List[TaskModel]=[]

    class Config:
        orm_mode=True
        schema_extra={
            'example':{
                "name":"ali",
                "email":"ali@gmail.com",
                "password":"ali123",
                "is_admin":False,
                "role":"DEVELOPER"
            }
        }

class UserModel(BaseModel):
    id: Optional[int]
    name: str
    email: str
    password: str
    is_admin: Optional[bool]
    role: Optional[str]="DEVELOPER"
    

    class Config:
        orm_mode=True
        schema_extra={
            'example':{
                "name":"ali",
                "email":"ali@gmail.com",
                "password":"ali123",
                "is_admin":False,
                "role":"DEVELOPER"
            }
        }

class Settings(BaseModel):
    authjwt_secret_key:str='f37c397f953f7e39c3a6fb0851258b12bc5f5579a3b2edd76c3352bddce3154b'

class LogInModel(BaseModel):
    email:str
    password:str


