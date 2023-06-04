import uvicorn

from fastapi import FastAPI

from models import Base, User, Coords, Level, Pereval, PerevalImages

app = FastAPI()


@app.get("/")
def hello():
    return 'Привет'


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)


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