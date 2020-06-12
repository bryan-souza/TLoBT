import shelve
import json
import os
import sys
sys.path.append('.')
from loader_functions.data_serializers import serialize, deserialize
from loader_functions.initialize_new_game import get_constants, get_game_variables
from mechanics.map_utils import GameMap


def save_game(player, entities, game_map, message_log, game_state):
    with open('savegame.json', 'w') as savegame:
        entity_list = []
        for entity in entities:
            entity_list.append(serialize(entity))
        
        json.dump({
            'player_index': entities.index(player),
            'entities': entity_list,
            'game_map': serialize(game_map),
            'message_log': serialize(message_log),
            'game_state': serialize(game_state)
            }, savegame, indent=4)

def load_game():
    if not os.path.isfile('savegame.json'):
        raise FileNotFoundError

    with open('savegame.json', 'r') as savegame:
        data = json.load(savegame)
        
        player_index = data['player_index']
        entities = [deserialize(entity) for entity in data['entities']]
        game_map = deserialize(data['game_map'])
        message_log = deserialize(data['message_log'])
        game_state = deserialize(data['game_state'])

    player = entities[player_index]

    return player, entities, game_map, message_log, game_state

# load_game()
# player, entities, game_map, message_log, game_state = get_game_variables(get_constants())
# save_game(player, entities, game_map, message_log, game_state)