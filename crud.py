# file with functions to create a game and a player
import models
from pony.orm import db_session

def create_game(name, min_players, max_players):
    """
    Create a game with the given parameters
    :param name: name of the game
    :param min_players: minimum number of players
    :param max_players: maximum number of players
    :param password: password to join the game
    :return: the game created
    """
    with db_session:
        game = models.Game(name=name, min_players=min_players, max_players=max_players)
    
    return game
    
def get_game(game_id):
    """
    Get a game with the given id
    :param game_id: id of the game
    :return: the game
    """
    with db_session:
        game = models.Game.get(id=game_id)
    response = game.to_dict_with_players()
    # order players by id
    response['players'].sort(key=lambda x: x['id']) 
    return response 
def create_player(name, game_id):
    """
    Create a player with the given parameters
    :param name: name of the player
    :param game_id: id of the game
    :return: the player created
    """
    with db_session:
        game = models.Game[game_id]
        player = models.Player(name=name, game=game)
    
    return player