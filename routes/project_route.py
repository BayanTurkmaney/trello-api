from fastapi import APIRouter,status,Depends
from schemas.projects import ProjectModel
from schemas.board import BoardModel
from fastapi_jwt_auth import AuthJWT
from fastapi.exceptions import HTTPException
from models.models import User,Project,Board
from settings.database import Base,session,engine
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse,Response
project_router=APIRouter(
    prefix='/project',tags=['project']
)

session=session(bind=engine)

@project_router.get('/')
async def hello():
   return {"message":"welcom at project"}

#list all project
@project_router.get('/all')
async def get_all_projects(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    current_user=Authorize.get_jwt_subject()
    user=session.query(User).filter(User.email==current_user).first()
    if user.is_admin :
        projects=session.query(Project).all()
        return jsonable_encoder(projects)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not allowed to carry out request")

#get specific project
@project_router.get('/all/{id}')
async def get_project(id:int,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    current_user=Authorize.get_jwt_subject()
    user=session.query(User).filter(User.email==current_user).first()
    if user.is_admin :
        project = session.query(Project).filter(Project.id==id).first()
        return jsonable_encoder(project)

#get user's projects
@project_router.get('/user/{user_id}/projects')
async def get_user_projects(user_id:int,Authorize:AuthJWT=Depends()):
    try:
      Authorize.jwt_required()
    except Exception as e:
        raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
    current_user=Authorize.get_jwt_subject()
    user=session.query(User).filter(User.email==current_user).first()
    if user.is_admin :
            user=session.query(User).filter(User.id==user_id).first()
            projects= user.projects
            return jsonable_encoder(projects)
    
#get specific user project
@project_router.get('/user/{user_id}/projects/{project_id}')
async def get_single_user_prject(user_id:int,project_id:int,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    current_user=Authorize.get_jwt_subject()
    user=session.query(User).filter(User.id==user_id).first()
    if user.is_admin:
        projects=user.projects
        for project in projects:
            if project.id==project_id:
                return jsonable_encoder(project)
#create project
@project_router.post('/create',status_code=status.HTTP_201_CREATED)
async def add_project(pro:ProjectModel,Authorize:AuthJWT=Depends()):
    try:
      Authorize.jwt_required()
    except Exception as e:
        raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
    current_user=Authorize.get_jwt_subject()

    # print(current_user)
    user= session.query(User).filter(User.email==current_user).first()
    if user.is_admin:
            new_project=Project(
                title=pro.title,
                project_code=pro.project_code,
                start_date=pro.start_date,
                end_date=pro.end_date     
            )

            new_project.user=user

            session.add(new_project)
            session.commit()
            response={
                "id": new_project.id,
                "title":new_project.title,
                "project_code":new_project.project_code,
                "start_date":new_project.start_date,
                "end_date":new_project.end_date, 
            }

            return jsonable_encoder(response)
    else:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
             detail="User not allowed to carry out request")

#update project
@project_router.put('/update/{id}')
async def update_pro(id:int,pro:ProjectModel,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")

    current_user=Authorize.get_jwt_subject()

    print(current_user)
    user= session.query(User).filter(User.email==current_user).first()
    if user.is_admin:
        project_to_update=session.query(Project).filter(Project.id==id).first()
        project_to_update.title=pro.title,
        project_to_update.start_date=pro.start_date,
        project_to_update.end_date=pro.end_date
        project_to_update.project_code=pro.project_code,

        session.commit()
        response={
            "id":project_to_update.id,
            "title":project_to_update.title,
            "project_code":project_to_update.project_code,
            "start_date":project_to_update.start_date,
            "end_date":project_to_update.end_date
        }

        return jsonable_encoder(response)
    
    else:
           raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
             detail="User not allowed to carry out request")
             
#delete project
@project_router.delete('/delete/{id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_pro(id:int,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
    current_user=Authorize.get_jwt_subject()

    print(current_user)
    user= session.query(User).filter(User.email==current_user).first()
    if user.is_admin:
        deleted_project=session.query(Project).filter(Project.id==id).first()
        print("*********************",deleted_project)
        session.delete(deleted_project)
        session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)


    else:
           raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
             detail="User not allowed to carry out request")




