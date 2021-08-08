from pydantic import BaseModel
from fastapi import FastAPI, Request

app = FastAPI()

players_lst = []

players_scores = {}

max_players = 2

battle_permissions = {}



def dict_sort(d):
    list_d = list(d.items())
    list_d.sort(key=lambda i: i[1])
    list_d = list(list_d.__reversed__())

    top = {}
    for i in range(len(list_d)):
        top[str(i+1)] = list_d[i]
    return top




@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/players")
def players():
    return players_lst

class PlayerName(BaseModel):
    Name:str



@app.post("/session")
def session(request: Request, player: PlayerName):
    ip_adess = request.client.host
    if len(players_lst) < max_players and not player.Name in players_lst:
        players_lst.append(player.Name)

    """if ip_adess not in players_lst and len(players_lst) < 4:
        pass
    elif ip_adess in players_lst and len(players_lst) == 4:
        return 'ready'
    else:
        return 'wait'"""




class PlayerScore(BaseModel):
    Name:str
    Score:float


@app.post("/post_score")
def post_score(score: PlayerScore):
    players_scores[score.Name] = score.Score

@app.post("/post_permission")
def post_permission(player: PlayerName):
    battle_permissions[player.Name] = 1

@app.get("/get_scores")
def get_scores():
    return players_scores

@app.get("/score_sort")
def score_sort():
    if len(players_scores.keys()) == max_players:
        return dict_sort(players_scores).items()

@app.get("/get_permissions")
def get_permissions():
    return battle_permissions


# Создать сессию(2 игрока)
# Если сесси нет, она создается
# Если есть и только 1 игрок, то подключается
# Только когда все игроки готовы
#
