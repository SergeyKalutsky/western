
from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/ip_check")
def read_root(request: Request):
    client_host = request.client.host
    return {"client_host": client_host}


@app.get("/session")
def session():
    return {"Hello": "World"}



# Создать сессию(2 игрока)
# Если сесси нет, она создается
# Если есть и только 1 игрок, то подключается
# Только когда все игроки готовы
# 

