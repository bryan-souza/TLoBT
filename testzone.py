# Make sure 'arial10x10.png' is in the same directory as this script.
import tcod
import random
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from components.equipment import Equipment, EquipmentSlots
from components.equippable import Equippable
from components.stairs import Stairs
from mechanics.entity import Entity
from mechanics.map_utils import GameMap, Rect, place_entities
from mechanics.render_functions import RenderOrder

def make_bsp(game_map, player, entities):
    room_list = []

    # Mappers
    bsp = tcod.bsp.BSP(0, 0, game_map.width - 1, game_map.height - 1)
    bsp.split_recursive(5, 8, 8, 1.0, 1.0)

    for node in bsp.inverted_level_order():
        if not node.children:
            for x in range(node.x, (node.x + node.width + 1)):
                for y in range(node.y, (node.y + node.height + 1)):
                    if (x == node.x or x == node.x + node.width) or (y == node.y or y == node.y + node.height):
                        game_map.walkable[x, y] = False
                        game_map.transparent[x, y] = False
                    else:
                        game_map.walkable[x, y] = True
                        game_map.transparent[x, y] = True

            last_room_x = random.randint(node.x + 1, node.x + node.width - 1)
            last_room_y = random.randint(node.y + 1, node.y + node.height - 1)

        else:
            valid = False
            while (valid == False):
                if (node.horizontal):
                    door_x = random.randint((node.x + 1), (node.x + node.width - 1))
                    door_y = node.position
                else:
                    door_x = node.position
                    door_y = random.randint((node.y + 1), (node.y + node.height - 1))

                if ((game_map.walkable[door_x + 1, door_y] and game_map.walkable[door_x - 1, door_y]) or (game_map.walkable[door_x, door_y + 1] and game_map.walkable[door_x, door_y - 1])):
                    valid = True
                    game_map.walkable[door_x, door_y] = True
                    game_map.transparent[door_x, door_y] = True
        
        if (len(room_list) == 0):
            player.x = random.randint(node.x + 1, node.x + node.width - 1)
            player.y = random.randint(node.y + 1, node.y + node.height - 1)
        
        room = Rect(node.x, node.y, node.width, node.height)
        place_entities(room, entities, game_map.dungeon_level)

        room_list.append(room)
    
    stairs_component = Stairs(game_map.dungeon_level + 1)
    down_stairs = Entity(last_room_x, last_room_y, '>', (255, 255, 255), 'Escadas', render_order=RenderOrder.STAIRS, stairs=stairs_component)
    entities.append(down_stairs)