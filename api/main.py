from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

players_lst = []
players_scores = {}
max_players = 2
battle_permissions = {}


class PlayerScore(BaseModel):
    name: str
    score: float


class PlayerName(BaseModel):
    name: str


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

@app.get("/reset")
def reset():
    # ПОМНИТЕ: ГЛОБАЛЬНЫЕ ПРЕМЕННЫЕ - ЗЛО! ЭТУ СТРОКУ НАПИСАЛ ПРОФЕССИОНАЛЬНЫЙ ГОВНОКОДЕР, НЕ СТОИТ ПОВТОРЯТЬ ЭТО ДОМА!
    global players_lst, players_scores, max_players, battle_permissions 
    players_scores = {}
    players_lst = []
    battle_permissions = {}


@app.get("/players")
def players():
    return players_lst


@app.post("/session")
def session(player: PlayerName):
    if len(players_lst) < max_players and not player.name in players_lst:
        players_lst.append(player.name)

    """ip_adess = request.client.host
       if ip_adess not in players_lst and len(players_lst) < 4:
            pass
       elif ip_adess in players_lst and len(players_lst) == 4:
            return 'ready'
       else:
            return 'wait'"""


@app.post("/post_score")
def post_score(score: PlayerScore):
    players_scores[score.name] = score.score


@app.post("/post_permission")
def post_permission(player: PlayerName):
    battle_permissions[player.name] = 1


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

