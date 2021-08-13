import os

from sqlalchemy import create_engine

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')

engine = create_engine(SQLALCHEMY_DATABASE_URI)
connection = engine.connect()

print(engine)
