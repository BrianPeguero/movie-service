from sqlalchemy import Column, Integer, String, ARRAY
from app.db.pg_db import Base

class Movie(Base):
    __tablename__="movies"
    __table_args__ = {'schema': 'movies'}
    id=Column(Integer, primary_key=True)
    name=Column(String(50))
    plot=Column(String(250))
    genres=Column(ARRAY(String))
    casts_id=Column(ARRAY(Integer))