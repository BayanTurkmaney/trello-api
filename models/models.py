
import sys, os
# sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# import manage
# from database import *
from settings.database import Base, session
from sqlalchemy.orm import relationship

from sqlalchemy import Integer, String, Boolean, Column, ForeignKey,DateTime,Table
from sqlalchemy_utils import ChoiceType
from typing  import List

class Association(Base):
    __tablename__='asscociation_table'
    id=Column(Integer,primary_key=True,)
    user_id=Column(Integer,ForeignKey('users.id'),)
    task_id=Column(Integer,ForeignKey('tasks.id'))
    
    def __repr__(self):
        return f"<Association {self.user_id}>"

class User(Base):
    
    ROLES=(
        ('CEO','ceo'),
        ('ANALYST','analyst'),
        ('TECHNICAL','technical'),
        ('TEAM_LEADER','team_leader'),
        ('DEVELOPER','developer'),
        ('GRAPHICAL_DESIGNER','graphical_designer'),
        ('UI_UX_DESIGNER','ui_ux_designer'),
        ('DIGITAL_MARKETING_SPECIALIST','digital_mareketing_specialist'),
        ('CONTENT_EDITOR','content_editor'),
        ('MOBILE__APP_DEVELOPER','mobile_app_developer'),
    )
    __tablename__="users"
    id=Column(Integer,primary_key=True)
    name=Column(String,nullable=False)
    email=Column(String,unique=True)
    password=Column(String,nullable=False)
    is_admin=Column(Boolean,default=False)
    role=Column(ChoiceType(choices=ROLES),default="DEVELOPER")
    projects=relationship('Project',back_populates='user', cascade="all,delete")
    boards=relationship('Board',back_populates='user',cascade="all,delete")
    tasks=relationship('Task',back_populates='user',cascade="all,delete")
    assigned_tasks=relationship('Task',secondary="asscociation_table",back_populates='assigned_users')


    def __repr__(self):
        return f"<User {self.name}>"

class Project(Base):
    __tablename__="projects"
    id=Column(Integer,primary_key=True)
    title=Column(String,nullable=False)
    project_code=Column(String(6),unique=True)
    start_date=Column(String,nullable=False)
    end_date=Column(String,nullable=False)
    user_id=Column(Integer,ForeignKey('users.id',ondelete="CASCADE"),)
    user=relationship('User',back_populates='projects')
    boards=relationship('Board',back_populates='project',cascade="all,delete")

    def __repr__(self):
        return f"<Project {self.title}>"

class Board(Base):
    __tablename__="boards"
    id=Column(Integer,primary_key=True)
    title=Column(String,nullable=False)
    user_id=Column(Integer,ForeignKey('users.id',ondelete="CASCADE"))
    user=relationship('User',back_populates='boards')
    proj_id=Column(Integer,ForeignKey('projects.id',ondelete="CASCADE"))
    project=relationship('Project',back_populates='boards')
    tasks=relationship('Task',back_populates='board',cascade="all,delete")

    def __repr__(self):
        return f"<Board {self.title}>"

class Task(Base):
    STATUSES=(
        ('TO_BE_DONE','to_be_done'),
        ('DOING','doing'),
        ('DONE','done'),)
    __tablename__="tasks"
    id=Column(Integer,primary_key=True)
    title=Column(String,nullable=False)
    labels=Column(Integer,nullable=False)
    start_date=Column(DateTime,nullable=False)
    end_date=Column(DateTime,nullable=False)
    status=Column(ChoiceType(choices=STATUSES),default="TO_BE_DONE")
    created_by=Column(Integer,ForeignKey('users.id',ondelete="CASCADE"))
    board_id=Column(Integer,ForeignKey('boards.id',ondelete="CASCADE"))
    board=relationship('Board',back_populates='tasks',cascade="all,delete")
    user=relationship('User',back_populates='tasks')
    assigned_users=relationship('User',secondary="asscociation_table",back_populates='assigned_tasks')

   

    def __repr__(self):
        return f"<Task {self.title}>"


