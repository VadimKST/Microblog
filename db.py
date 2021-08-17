import os

import databases
from sqlalchemy import create_engine

DATABASE_URL = os.environ.get('DATABASE_URI')

database = databases.Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
