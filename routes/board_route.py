from fastapi import APIRouter , status, Depends
from models.models import User,Project,Board
from schemas.board import BoardModel
from settings.database import Base,session,engine
from fastapi_jwt_auth import AuthJWT
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
board_router=APIRouter(prefix='/board',tags=['board'])

session=session(bind=engine)
@board_router.get('/')
async def hello():
   return {"message":"welcom at board"}


@board_router.get('/all')
async def get_all_boards(Authorize:AuthJWT=Depends()):
    try:
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    current_user=Authorize.get_jwt_subject()
    user=session.query(User).filter(User.email==current_user).first()
    if user.is_admin:
        boards=session.query(Board).all()
        return jsonable_encoder(boards)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not allowed to carry out request")
   
@board_router.get('/all/{board_id}')
async def get_all_boards(board_id:int,Authorize:AuthJWT=Depends()):
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
        board=session.query(Board).filter(Board.id==board_id).first()
        return jsonable_encoder(board)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not allowed to carry out request")

@board_router.get('/proboards')
async def get_boards_by_project(pro_id:int,Authorize:AuthJWT=Depends()):
    try:
        # print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    current_user=Authorize.get_jwt_subject()
    user=session.query(User).filter(User.email==current_user).first()
    
    if user.is_admin:
        projects=user.projects
        # print("********************************",projects)
        for project in projects:
            if project.id==pro_id:
                # print("*******************************",project)
                boards=project.boards
                # print("********************************",boards)
                return jsonable_encoder(boards)
            
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not allowed to carry out request")
    
@board_router.get('/userboards')   
async def get_boards_by_user(Authorize:AuthJWT=Depends()):
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
        boards=user.boards
        return jsonable_encoder(boards)
        
@board_router.post('/create',status_code=status.HTTP_201_CREATED)
async def add_board(board:BoardModel,pro_id:int, Authorize:AuthJWT=Depends()):
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
                    new_board=Board(
                        title=board.title
                    )
                    new_board.user_id=user.id
                    new_board.proj_id=pro_id
                    session.add(new_board)
                    session.commit()
                    response={
                        "id":new_board.id,
                        "title":new_board.title,
                        "created by":new_board.user,
                        "pro_id":new_board.project
                    }
                    return jsonable_encoder(response)
        # else:
        #     print('you can not do this request')


@board_router.put('/update/{id}')
async def update_board(pro_id:int,id:int,board:BoardModel,Authorize:AuthJWT=Depends()):
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
                        board_to_update=session.query(Board).filter(Board.id==id).first()
                        board_to_update.title=board.title

                        session.commit()
                        response={
                            "id":board_to_update.id,
                            "title":board_to_update.title,
                        }

                        return jsonable_encoder(response)
            
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not allowed to carry out request")


@board_router.delete('/delete/{id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_board(pro_id:int,id:int,Authorize:AuthJWT=Depends()):
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
                        board_deleted=session.query(Board).filter(Board.id==id).first()
                        session.delete(board_deleted)

                        session.commit()
                        return Response(status_code=status.HTTP_204_NO_CONTENT)
            
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not allowed to carry out request")

