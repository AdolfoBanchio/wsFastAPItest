from pony.orm import Database,Required, Set, Optional, PrimaryKey

db = Database()

class Game(db.Entity):

    """
    Represent a game
    """

    id = PrimaryKey(int, auto=True)
    name = Required(str)
    min_players = Required(int)
    max_players = Required(int)
    state = Required(int, default=0)  # 0 = waiting, 1 = playing, 2 = finished
    play_direction = Optional(bool)  # true = clockwise
    turn_owner = Optional(int)
    players = Set('Player', reverse="game")

    def to_dict_with_players(self):
        game_dict = {
            'id': self.id,
            'name': self.name,
            'min_players': self.min_players,
            'max_players': self.max_players,
            'state': self.state,
            'play_direction': self.play_direction,
            'turn_owner': self.turn_owner,
            'players': [player.to_dict() for player in self.players]
        }
        return game_dict


class Player(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    table_position = Optional(int)
    role = Optional(int)  # enum(humano,infectado,laCosa)
    alive = Optional(bool, default=True)
    quarantine = Optional(bool, default=False)
    game = Required("Game", reverse="players")
    owner = Required(bool, default=False)

