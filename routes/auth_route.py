from fastapi import APIRouter,status,Depends
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from werkzeug.security import generate_password_hash,check_password_hash
from schemas.user import LogInModel,signUpModel
from models.models import User
from fastapi.encoders import jsonable_encoder
from settings.database import session,engine
from fastapi.responses import Response

auth_router=APIRouter(
    prefix='/auth',
    tags=['auth']
)
session=session(bind=engine)

@auth_router.get('/')
async def hello():
   return {"message":"welcom at auth"}

@auth_router.get('/users/{id}')
async def get_user(id:int,Authorize:AuthJWT=Depends()):
  try:
    Authorize.jwt_required()
  except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
  current_user=Authorize.get_jwt_subject()
  n_user=session.query(User).filter(User.email==current_user).first()
  if n_user.is_admin :
        user=session.query(User).filter(User.id==id).first()
        response={
                    "id":user.id,
                      "name":user.name,
                      "email":user.email,
                      "password":user.password,
                      "is_admin":user.is_admin,
                      "role":user.role,
                      "created task":user.tasks,
                      "assignrd tasks":user.assigned_tasks,
                      "projects":user.projects,
                      "created tasks":user.tasks,
                      "boards":user.boards
        }
        return jsonable_encoder(response)

  else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not allowed to carry out request")

@auth_router.get('/users')
async def get_all_users(Authorize:AuthJWT=Depends()):
  try:
    Authorize.jwt_required()
  except Exception as e:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid token"
    )
  current_user=Authorize.get_jwt_subject()
  n_user=session.query(User).filter(User.email==current_user).first()
  if n_user.is_admin:
     users=session.query(User).all()
     return jsonable_encoder(users)
  else:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not allowed to carry out request")

@auth_router.get('/refresh')
async def refresh_token(Authorize:AuthJWT=Depends()):
    try:
        print('######################################')
        Authorize.jwt_refresh_token_required()


    except Exception as e:
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="please provide a valid refresh token")
    current_user=Authorize.get_jwt_subject()
    print('current_user',current_user)
    access_token=Authorize.create_access_token(subject=current_user)
    print(access_token)
    return jsonable_encoder({"access":access_token})

@auth_router.post('/signup',status_code=status.HTTP_201_CREATED)
async def signUp(user:signUpModel):
    us_email=session.query(User).filter(User.email==user.email).first()
    if us_email is not None:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='email already exists'
      )
    us_name=session.query(User).filter(User.name==user.name).first()
    if us_name is not None:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='name already exists'
      )

    new_user=User(
      name=user.name,
      email=user.email,
      password=generate_password_hash(user.password),
      is_admin=user.is_admin,
      role=user.role
    )
    session.add(new_user)
    session.commit()
    response={
      "id":new_user.id,
      "name":new_user.name,
      "email":new_user.email,
      # "password":generate_password_hash(user.password),
      "is_admin":new_user.is_admin,
      "role":new_user.role
    }
    return jsonable_encoder(response)
   
    # return new_user

@auth_router.post('/login',status_code=200)
async def login(user:LogInModel,Authorize:AuthJWT=Depends()):
  print('**************************',user.email)
  print(user.password)
  us_name=session.query(User).filter(User.email==user.email).first()
  if us_name and check_password_hash(us_name.password,user.password):
    access_token=Authorize.create_access_token(subject=us_name.email)
    refresh_token=Authorize.create_refresh_token(subject=us_name.email)
    print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&7',us_name.email)
    print(us_name.password)
    
    response={
      "access_token":access_token,
      "refresh_token":refresh_token,
      "data":{
        "id":us_name.id,
        "name":us_name.name,
        "email":us_name.email,
        "password":us_name.password,
        "is_admin":us_name.password,
        "role":us_name.role
      }
    }
    return jsonable_encoder(response)

  raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Invalid username or password'
  )

@auth_router.put('/update/{id}')
async def update_pro(id:int,user:signUpModel,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")

    current_user=Authorize.get_jwt_subject()

    print(current_user)
    n_user= session.query(User).filter(User.email==current_user).first()
    if n_user.is_admin:
        user_to_update=session.query(User).filter(User.id==id).first()
        user_to_update.name=user.name,
        user_to_update.email=user.email,
        user_to_update.password=user.password,
        user_to_update.role=user.role,

        session.commit()
        response={
            "id":user_to_update.id,
            "name":user_to_update.name,
            "email":user_to_update.email,
            # "password":user_to_update.password,
            "role":user_to_update.role
        }

        return jsonable_encoder(response)
    
    else:
           raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
             detail="User not allowed to carry out request")
             
@auth_router.delete('/users/delete/{id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id:int, Authorize:AuthJWT=Depends()):
  try:
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    Authorize.jwt_required()
  except Exception as e:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid token"
    )
  current_user=Authorize.get_jwt_subject()
  print("*****************current :",current_user)
  n_user=session.query(User).filter(User.email==current_user).first()
  print("*****************n-user :",n_user)
  if n_user.is_admin:
    deleted_user=session.query(User).filter(User.id==id).first()
    
    print("*****************deleted_user :",deleted_user)
    session.delete(deleted_user)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
  else:
        raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="User not allowed to do this request"
    )


