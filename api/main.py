
from fastapi import FastAPI, Request

app = FastAPI()

players_lst = []


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/players")
def players():
    return {"playes": players_lst}


@app.get("/session")
def session(request: Request):
    ip_adess = request.client.host
    if ip_adess not in players_lst and len(players_lst) < 4:
        players_lst.append(ip_adess)
    elif ip_adess in players_lst and len(players_lst) == 4:
        return 'ready'
    else:
        return 'wait'


# Создать сессию(2 игрока)
# Если сесси нет, она создается
# Если есть и только 1 игрок, то подключается
# Только когда все игроки готовы
#
