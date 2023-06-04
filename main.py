import os
import uvicorn
import datetime

from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Coords, Level, Pereval, PerevalImages
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


app = FastAPI()
load_dotenv()

base_dir = os.path.abspath(os.path.dirname(__file__))
fstr_db_host = os.getenv('FSTR_DB_HOST')
fstr_db_port = os.getenv('FSTR_DB_PORT')
fstr_db_login = os.getenv('FSTR_DB_LOGIN')
fstr_db_pass = os.getenv('FSTR_DB_PASS')

database_url =f'postgresql://{fstr_db_login}:{fstr_db_pass}@{fstr_db_host}:{fstr_db_port}/fstr'

engine = create_engine(database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@app.get("/")
def hello():
    return 'Привет'


def create_user(db, user_data):
    user = User(email=user_data['email'], fam=user_data['fam'], otc=user_data['otc'],
                name=user_data['name'], phone=user_data['phone'])
    db.add(user)
    return user


def create_coords(db, coords_data):
    coords = Coords(latitude=coords_data['latitude'], longitude=coords_data['longitude'],
                    height=coords_data['height'])
    db.add(coords)
    return coords


def create_level(db, level_data):
    level = Level(winter=level_data['winter'], summer=level_data['summer'],
                  autumn=level_data['autumn'], spring=level_data['spring'])
    db.add(level)
    return level


def create_perevalImages(db, pereval, images_data):
    images = []
    for image_data in images_data:
        image = PerevalImages(image_name=image_data['data'], title=image_data['title'], pereval=pereval)
        db.add(image)
        images.append(image)
    return images


def create_pereval(db, pereval_data):
    user = create_user(db, pereval_data['user'])
    coords = create_coords(db, pereval_data['coords'])
    level = create_level(db, pereval_data['level'])

    add_time = datetime.datetime.strptime(pereval_data['add_time'], '%Y-%m-%d %H:%M:%S')

    pereval = Pereval(
        beautyTitle=pereval_data['beauty_title'],
        title=pereval_data['title'],
        other_titles=pereval_data['other_titles'],
        connect=pereval_data['connect'],
        add_time=add_time,
        coords=coords,
        user=user,
        level=level
    )

    db.add(pereval)
    db.commit()
    db.refresh(pereval)

    images = create_perevalImages(db, pereval, pereval_data['images'])
    pereval.images = images
    db.commit()

    return pereval


@app.post("/submitData")
def submit_data(data: dict):
    try:
        db = SessionLocal()
        try:
            pereval_data = data.get('pereval')
            pereval = create_pereval(db, pereval_data)
            response_data = {
                "status": 200,
                "message": None,
                "id": pereval.id
            }

            return JSONResponse(content=jsonable_encoder(response_data))

        finally:
            db.close()
    except Exception as e:
        response_data = {
            "status": 500,
            "message": "Ошибка подключения к базе данных",
            "id": None
        }
        raise HTTPException(status_code=500, detail=response_data)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    uvicorn.run(app, host="127.0.0.1", port=8000)
