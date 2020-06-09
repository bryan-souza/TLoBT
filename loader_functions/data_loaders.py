import shelve
import json
import os
from loader_functions.data_serializers import serializeEntity, serializeGameMap, serializeMessageLog, serializeGameState
from mechanics.map_utils import GameMap


def save_game(player, entities, game_map, message_log, game_state):
    with open('savegame.json', 'w') as savegame:
        entity_list = []
        for entity in entities:
            entity_list.append(serializeEntity(entity))
        
        json.dump({
            'player_index': entities.index(player),
            'entities': entity_list,
            'game_map': serializeGameMap(game_map),
            'message_log': serializeMessageLog(message_log),
            'game_state': serializeGameState(game_state)
            }, savegame, indent=4)
            
        # data_file['player_index'] = entities.index(player)
        # data_file['entities'] = entities 
        # data_file['game_map'] = game_map
        # data_file['message_log'] = message_log
        # data_file['game_state'] = game_state


def load_game():
    if not os.path.isfile('savegame.dat'):
        raise FileNotFoundError

    with shelve.open('savegame', 'r') as data_file:
        player_index = data_file['player_index']
        entities = data_file['entities']
        game_map = data_file['game_map']
        message_log = data_file['message_log']
        game_state = data_file['game_state']

    player = entities[player_index]

    return player, entities, game_map, message_log, game_state
