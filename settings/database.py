from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
engine=create_engine('postgresql://bana:pos123@localhost/proj_nmng',)

Base=declarative_base()
session=sessionmaker()

