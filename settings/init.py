from database import Base,engine
import models

def initdb():
    Base.metadata.create_all(bind=engine)


