from fastapi import APIRouter,Depends,status
from schemas.task import TaskModel,AccociationModel,TaskUserModel
from fastapi_jwt_auth import AuthJWT
from fastapi.responses import Response
from fastapi.exceptions import HTTPException
from models.models import User,Project,Board,Task,Association
from settings.database import Base,session,engine
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse,Response
from typing import Optional,List
from schemas.user import signUpModel
task_router=APIRouter(
    prefix='/task',
    tags=['task']
)

session=session(bind=engine)

@task_router.get('/')
async def hello():
   return {"message":"welcom at task"}

@task_router.get('/all')                   
async def get_tasks_by_boards(board_id:int, pro_id:int,Authorize:AuthJWT=Depends()):
    try:
      Authorize.jwt_required()
    except Exception as e:
        raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
    current_user=Authorize.get_jwt_subject()
    user= session.query(User).filter(User.email==current_user).first()
    if user.is_admin:
            projects=user.projects
            for project in projects:
                if project.id==pro_id:
                    print("1111111111111111111111111111")
                    boards=project.boards
                    if boards is not None:
                        print("22222222222222222222222222222222")
                        for board in boards:
                            if board.id==board_id:
                                tasks=board.tasks
                                return jsonable_encoder(tasks)

@task_router.get('/usertasks/{id}') 
async def get_tasks_by_user(id:int,Authorize:AuthJWT=Depends()):
    try:
      Authorize.jwt_required()
    except Exception as e:
        raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
    current_user=Authorize.get_jwt_subject()
    user= session.query(User).filter(User.email==current_user).first()
    if user.is_admin:
            n_user=session.query(User).filter(User.id==id).first()
            tasks=n_user.tasks
            return jsonable_encoder(tasks)

@task_router.get('/userasigntasks/{id}') 
async def get_tasks_by_user(id:int,Authorize:AuthJWT=Depends()):
    try:
      Authorize.jwt_required()
    except Exception as e:
        raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
    current_user=Authorize.get_jwt_subject()
    user= session.query(User).filter(User.email==current_user).first()
    if user.is_admin:
        n_user= session.query(User).filter(User.id==id).first()
        assigned_tasks=n_user.assigned_tasks
        return jsonable_encoder(assigned_tasks)

@task_router.post('/create',status_code=status.HTTP_201_CREATED)
async def create_task(request:TaskUserModel,Authorize:AuthJWT=Depends()):
    try:
      Authorize.jwt_required()
    except Exception as e:
        raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
    assigned_users=[]
    current_user=Authorize.get_jwt_subject()
    user= session.query(User).filter(User.email==current_user).first()
    if user.is_admin:
        projects=user.projects
    for project in projects:
        if project.id==request.pro_id:
            boards=project.boards
            if boards is not None:
                for board in boards:
                    if board.id==request.board_id:
                        new_task=Task(
                            title=request.task.title,
                            labels=request.task.labels,
                            start_date=request.task.start_date,
                            end_date=request.task.end_date,
                            status=request.task.status,   
                        )        
                        new_task.user=user
                        new_task.board=board
                        new_task.assigned_users=assigned_users
                        # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",new_task) 
                        # print(request.users)
                        session.add(new_task)
                        session.commit()
                        t_id=new_task.id
                        
                        for u_id in request.users:
                            # print('***************************************',u_id)
                            new_acc=Association(
                                user_id=u_id,
                                task_id=t_id)
                            session.add(new_acc)
                            session.commit()
                            print("new acccccccccccccc uid",new_acc.user_id)
                            print("new acccccccccccccc tid",new_acc.task_id)
                            user=session.query(User).filter(User.id==u_id).first()
                            assigned_users.append(user)
                        # for x in assigned_users:
                        #     print("***************************************",x) 
                        response={
                            "id": new_task.id,
                            "title":new_task.title,
                            "labels":new_task.labels,
                            "start_date":new_task.start_date,
                            "end_date":new_task.end_date,
                            "status":new_task.status,
                            "created by":new_task.user,
                            "assigned users":new_task.assigned_users,                            
                            "board_id":new_task.board_id 
                        }
                        return jsonable_encoder(response) 

@task_router.put('/update/{id}')
async def update_task(id:int,pro_id:int,board_id:int,task:TaskModel,Authorize:AuthJWT=Depends()):
    try:
      Authorize.jwt_required()
    except Exception as e:
        raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
    current_user=Authorize.get_jwt_subject()
    user= session.query(User).filter(User.email==current_user).first()
    if user.is_admin:
            projects=user.projects
            for project in projects:
                if project.id==pro_id:
                    print("1111111111111111111111111111")
                    boards=project.boards
                    if boards is not None:
                        print("22222222222222222222222222222222")
                        for board in boards:
                            if board.id==board_id:
                                print("33333333333333333333333333333333333")
                                task_updated=session.query(Task).filter(Task.id==id).first()
                                task_updated.title=task.title,
                                task_updated.labels=task.labels,
                                task_updated.start_date=task.start_date,
                                task_updated.end_date=task.end_date,
                                task_updated.status=task.status
                                for us in task.assigned_users:
                                    task_updated.assigned_users.append(us)
                                session.commit()
                                print("77777777777777777777777777777777")
                                response={
                                    "id": task_updated.id,
                                    "title":task_updated.title,
                                    "labels":task_updated.labels,
                                    "start_date":task_updated.start_date,
                                    "end_date":task_updated.end_date,
                                    "status":task_updated.status,
                                    "user":task_updated.user,
                                    "assigned user":task_updated.assigned_users,
                                    "board_id":task_updated.board_id 
                                }
                                return jsonable_encoder(response)

@task_router.delete('/delete/{id}',status_code=status.HTTP_204_NO_CONTENT)
async def update_task(id:int,pro_id:int,board_id:int,Authorize:AuthJWT=Depends()):
    try:
      Authorize.jwt_required()
    except Exception as e:
        raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
    current_user=Authorize.get_jwt_subject()
    user= session.query(User).filter(User.email==current_user).first()
    if user.is_admin:
            projects=user.projects
            for project in projects:
                if project.id==pro_id:
                    print("1111111111111111111111111111")
                    boards = project.boards
                    if boards is not None:
                        print("22222222222222222222222222222222")
                        for board in boards:
                            if board.id==board_id:
                                task_deleted=session.query(Task).filter(Task.id==id).first()
                                session.delete(task_deleted)
                                session.commit()
                                return Response(status_code=status.HTTP_204_NO_CONTENT)
                                

# @task_router.post('/create',status_code=status.HTTP_201_CREATED)
# async def create_task(pro_id:int,board_id:int,task:TaskModel,Authorize:AuthJWT=Depends()):
#     try:
#       Authorize.jwt_required()
#     except Exception as e:
#         raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
#     current_user=Authorize.get_jwt_subject()
#     user= session.query(User).filter(User.email==current_user).first()
#     projects=user.projects
#     for project in projects:
#         if project.id==pro_id:
#             boards=project.boards
#             if boards is not None:
#                 for board in boards:
#                     if board.id==board_id:
#                         new_task=Task(
#                             title=task.title,
#                             labels=task.labels,
#                             start_date=task.start_date,
#                             end_date=task.end_date,
#                             status=task.status,   
#                         )        
#                         new_task.user=user
#                         new_task.board=board
                        
#                         # for x in users:
#                         #     new_task.assigned_users.append(x.dict())    

#                         assigned_users=[]
#                         related_users=task.assigned_users

#                         for us in related_users:
#                             # print(us.assigned_tasks)
#                             assigned_users.append(us.dict())
                        
#                         session.add(new_task)
#                         session.commit()
#                         response={
#                             "id": new_task.id,
#                             "title":new_task.title,
#                             "labels":new_task.labels,
#                             "start_date":new_task.start_date,
#                             "end_date":new_task.end_date,
#                             "status":new_task.status,
#                             "created by":new_task.user,
#                             "assigned users":new_task.assigned_users,                            
#                             "board_id":new_task.board_id 
#                         }
#                         return jsonable_encoder(response) 