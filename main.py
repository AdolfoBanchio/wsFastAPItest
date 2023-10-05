# fastapi app that creates games and players

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from models import db
import crud
from pony.orm import db_session
from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from fastapi import WebSocket, WebSocketDisconnect
import asyncio

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
games_with_pending_updates = set()

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("game.html", "r") as html_file:
        return HTMLResponse(content=html_file.read())

@app.post("/game/", status_code=201)
async def create_game(game_name: str, min_players: int, max_players: int):
    """
    Create a game with the given parameters
    :param game_name: name of the game
    :param min_players: minimum number of players
    :param max_players: maximum number of players
    :param password: password to join the game
    :return: the game created
    """
    with db_session:
        game = crud.create_game(game_name, min_players, max_players)
        return game.to_dict()

@app.get("/game/{game_id}")
async def get_game(game_id: int):
    """
    Get a game with the given id
    :param game_id: id of the game
    :return: the game
    """
    with db_session:
        game = crud.get_game(game_id)
        if game:
            return game
        else:
            raise HTTPException(status_code=404, detail="Game not found")
        

@app.post("/player", status_code=201)
async def create_player(player_name: str, game_id: int):
    """
    Create a player with the given parameters
    :param player_name: name of the player
    :param game_id: id of the game
    :return: the player created
    """
    with db_session:
        player = crud.create_player(player_name, game_id)
        games_with_pending_updates.add(game_id) 
        return player.to_dict()

async def send_pending_updates():
    while True:
        await asyncio.sleep(5)  # Adjust the interval as needed
        with db_session:
            try:
                for game_id in games_with_pending_updates:
                    game = crud.get_game(game_id)
                    if game:
                        await broadcast_game_update(game_id, game)
                    
                        games_with_pending_updates.remove(game_id)
            except Exception:
                        pass

connected_websockets = set()

async def broadcast_game_update(game_id: int, game: dict):
    for websocket in connected_websockets:
        await websocket.send_json({"game": game})

@app.websocket("/ws/game/{game_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: int):
    await websocket.accept()
    connected_websockets.add(websocket)
    while True:
        try:
            await websocket.receive_text()
        except WebSocketDisconnect:
            break
        finally:
            connected_websockets.remove(websocket)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(send_pending_updates())

# Connect to the database
db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)