from fastapi import FastAPI
from routes.auth_route import auth_router
from routes.project_route import project_router
from routes.board_route import board_router
from routes.task_route import task_router
from fastapi_jwt_auth import AuthJWT
from fastapi.middleware.cors import CORSMiddleware
from schemas.user import Settings

# if need models
'''
import sys, os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,os.path.join(ROOT_DIR, './models'))
sys.path.insert(0,os.path.join(ROOT_DIR, './config'))
'''


@AuthJWT.load_config
def get_config():
    return Settings()


app = FastAPI()
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(project_router)
app.include_router(board_router)
app.include_router(task_router)


@app.get('/')
async def hello():
    return {"message": "welcome at home"}
