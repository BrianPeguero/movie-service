from app.schemas.movie import MovieIn, MovieOut, MovieUpdate
from app.models.movie import Movie
from sqlalchemy.orm import Session


def add_movie(db:Session, payload: MovieIn):
    movie = Movie(
        name=payload.name,
        plot=payload.plot,
        genres=payload.genres,
        casts_id=payload.casts_id
    )

    db.add(movie)
    db.commit()
    db.refresh()

    return movie

def get_all_movies(db:Session):

    movies = db.query(Movie).all()

    for movie in movies:
        print(movie.id)
    
    return movies

def get_movie(db:Session, id):

    movie=db.query(Movie).filter(Movie.id==id).first()

    return movie

def update_movie(db:Session, id: int, payload: MovieIn):
    movie = db.query(Movie).filter(Movie.id==id).fist()

    movie=payload.dict()

    db.commit()
    db.refresh()

    return movie