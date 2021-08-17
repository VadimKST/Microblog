from sqlalchemy import (MetaData, Table, Column, Integer, String, Text, Boolean,
                        DateTime, ForeignKey, CheckConstraint, sql)

metadata = MetaData()

user = Table('user', metadata,
             Column('id', Integer(), primary_key=True),
             Column('username', String(50), nullable=False, unique=True),
             Column('email', String(50), nullable=False, unique=True),
             Column('password', String(), nullable=False),
             )

user_details = Table('user_details', metadata,
                     Column('user_id', ForeignKey("user.id"), primary_key=True),
                     Column('name', String(150), nullable=False),
                     Column('surname', String(150), nullable=False),
                     Column('patronymic', String(150)),
                     Column('city', String(100)),
                     Column('age', Integer()),
                     Column('about_me', Text()),
                     CheckConstraint('age > 16', name='age_check')
                     )

post = Table('post', metadata,
             Column('id', Integer(), primary_key=True),
             Column('post_title', String(200), nullable=False),
             Column('post_slug', String(200), nullable=False),
             Column('content', Text(), nullable=False),
             Column('published', Boolean(), default=sql.expression.false()),
             Column('created_on', DateTime(), server_default=sql.func.now()),
             Column('updated_on', DateTime(), server_default=sql.func.now(), onupdate=sql.func.now()),
             Column('user_id', ForeignKey("user.id"))
             )
