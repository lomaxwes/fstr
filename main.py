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