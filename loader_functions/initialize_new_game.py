# Components
from components.fighter import Fighter
from components.inventory import Inventory
from components.equipment import Equipment, EquipmentSlots
from components.equippable import Equippable
from components.level import Level

# Mechanics
from mechanics import colors
from mechanics.entity import Entity
from mechanics.render_functions import RenderOrder
from mechanics.map_utils import GameMap, make_bsp
from mechanics.game_messages import MessageLog
from mechanics.game_states import GameStates


def get_constants():
    WINDOW_TITLE = 'TLoBT'

    SCREEN_WIDTH = 80
    SCREEN_HEIGHT = 50

    BAR_WIDTH = 20
    PANEL_HEIGHT = 7
    PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT

    MESSAGE_X = BAR_WIDTH + 2
    MESSAGE_WIDTH = SCREEN_WIDTH - BAR_WIDTH - 2
    MESSAGE_HEIGHT = PANEL_HEIGHT - 1

    MAP_WIDTH = 80
    MAP_HEIGHT = 43

    ROOM_MAX_SIZE = 12
    ROOM_MIN_SIZE = 6
    MAX_ROOMS = 32

    FOV_ALGORITHM = 'DIAMOND'
    FOV_LIGHT_WALLS = True
    FOV_RADIUS = 10

    MAX_MONSTERS_PER_ROOM = 3
    MAX_ITEMS_PER_ROOM = 2

    Colors = {
        'dark_wall': (0, 0, 100),
        'dark_ground': (50, 50, 150),
        'light_wall': (130, 110, 50),
        'light_ground': (200, 180, 50)
    }

    constants = {
        'WINDOW_TITLE': WINDOW_TITLE,
        'SCREEN_WIDTH': SCREEN_WIDTH,
        'SCREEN_HEIGHT': SCREEN_HEIGHT,
        'BAR_WIDTH': BAR_WIDTH,
        'PANEL_HEIGHT': PANEL_HEIGHT,
        'PANEL_Y': PANEL_Y,
        'MESSAGE_X': MESSAGE_X,
        'MESSAGE_WIDTH': MESSAGE_WIDTH,
        'MESSAGE_HEIGHT': MESSAGE_HEIGHT,
        'MAP_WIDTH': MAP_WIDTH,
        'MAP_HEIGHT': MAP_HEIGHT,
        'ROOM_MAX_SIZE': ROOM_MIN_SIZE,
        'ROOM_MIN_SIZE': ROOM_MIN_SIZE,
        'MAX_ROOMS': MAX_ROOMS,
        'FOV_ALGORITHM': FOV_ALGORITHM,
        'FOV_LIGHT_WALLS': FOV_LIGHT_WALLS,
        'FOV_RADIUS': FOV_RADIUS,
        'MAX_MONSTERS_PER_ROOM': MAX_MONSTERS_PER_ROOM,
        'MAX_ITEMS_PER_ROOM': MAX_ITEMS_PER_ROOM,
        'Colors': Colors
    }

    return constants


def get_game_variables(constants):
    fighter_component = Fighter(hp=100, defense=1, power=2)
    inventory_component = Inventory(26)
    level_component = Level()
    equipment_component = Equipment()
    player = Entity(0, 0, '@', colors.white, 'Player',
                    blocks=True, render_order=RenderOrder.ACTOR,
                    fighter=fighter_component, inventory=inventory_component,
                    level=level_component, equipment=equipment_component)

    entities = [player]

    equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=2)
    adaga = Entity(0, 0, '-', colors.sky, 'Adaga Simples',
                   equippable=equippable_component)
    player.inventory.add_item(adaga)
    player.equipment.toggle_equip(adaga)

    game_map = GameMap(constants['MAP_WIDTH'], constants['MAP_HEIGHT'])
    make_bsp(game_map, player, entities)

    message_log = MessageLog(
        constants['MESSAGE_X'], constants['MESSAGE_WIDTH'], constants['MESSAGE_HEIGHT'])

    game_state = GameStates.PLAYERS_TURN

    return player, entities, game_map, message_log, game_state
