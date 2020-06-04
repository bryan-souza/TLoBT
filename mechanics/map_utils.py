import tcod
import random
from mechanics import colors
from tdl.map import Map
from random import randint
from components.item import Item
from components.fighter import Fighter
from components.ai import BasicMonster, Apprentice
from components.inventory import Inventory
from components.stairs import Stairs
from components.equipment import EquipmentSlots
from components.equippable import Equippable
from mechanics.entity import Entity
from mechanics.item_functions import heal, cast_fireball, cast_lightning
from mechanics.special_item_functions import cast_confuse
from mechanics.render_functions import RenderOrder
from mechanics.game_messages import Message
from mechanics.random_utils import from_dungeon_level, random_choice_from_dict

class GameMap(Map):
    def __init__(self, width, height, dungeon_level=1):
        super().__init__(width, height)
        self.explored = [[False for y in range(height)] for x in range(width)]

        self.dungeon_level = dungeon_level

class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_X = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return (center_X, center_y)

    def intersect(self, other):
        #Retorna 'True' caso uma sala se interceccionar com outra
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

def make_bsp(game_map, player, entities):
    room_list = []

    # Mappers
    bsp = tcod.bsp.BSP(0, 0, game_map.width - 1, game_map.height - 1)
    bsp.split_recursive(5, 8, 8, 1.0, 1.0)

    for node in bsp.inverted_level_order():
        if not node.children:
            for x in range(node.x, (node.x + node.width)):
                for y in range(node.y, (node.y + node.height)):
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

def next_floor(player, message_log, dungeon_level, constants):
    game_map = GameMap(constants['MAP_WIDTH'], constants['MAP_HEIGHT'], dungeon_level)
    entities = [player]

    make_bsp(game_map, player, entities)

    player.fighter.heal(player.fighter.max_hp // 2)

    message_log.add_message(Message('Voce para um momento para descansar, e recuperar suas forcas.', colors.light_violet))

    return game_map, entities

def place_entities(room, entities, dungeon_level):
    #Pega um numero aleatorio de monstros
    MAX_MONSTERS_PER_ROOM = from_dungeon_level([[2, 1], [3, 4], [5, 6]], dungeon_level)
    MAX_ITEMS_PER_ROOM = from_dungeon_level([[1, 1], [2, 4]], dungeon_level)

    number_of_monsters = randint(0, MAX_MONSTERS_PER_ROOM)
    number_of_items = randint(0, MAX_ITEMS_PER_ROOM)

    monster_chances = {
        'orc': 80,
        'troll': from_dungeon_level([[15, 3], [30, 5], [60, 7]], dungeon_level),
        'apprentice': from_dungeon_level([[5, 2], [10, 4], [20, 6]], dungeon_level)
    }

    item_chances = {
        'healing_potion': 35,
        'sword': from_dungeon_level([[5, 4]], dungeon_level),
        'shield': from_dungeon_level([[15, 8]], dungeon_level),
        'helmet': from_dungeon_level([[25, 3]], dungeon_level),
        'lightning_scroll': from_dungeon_level([[25, 4]], dungeon_level),
        'fireball_scroll': from_dungeon_level([[25, 6]], dungeon_level),
        'confusion_scroll': from_dungeon_level([[10, 2]], dungeon_level),
        'peitoral': from_dungeon_level([[30, 5]], dungeon_level),
        'calca': from_dungeon_level([[20, 6]], dungeon_level),
        'bota': from_dungeon_level([[10, 1]], dungeon_level)
    }

    for i in range(number_of_monsters):
        #Escolhe uma localizacao aleatoria na sala
        x = randint(room.x1 + 2, room.x2 - 2)
        y = randint(room.y1 + 2, room.y2 - 2)

        if not any([entity for entity in entities if entity.x == x and entity.y == y]):
            monster_choice = random_choice_from_dict(monster_chances)

            if monster_choice == 'apprentice':
                fighter_component = Fighter(hp=16, defense=1, power=0, xp=150)
                ai_component = Apprentice()
                inventory_component = Inventory(1)

                monster = Entity(x, y, 'a', colors.white, 'Aprendiz', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component, inventory=inventory_component)

            elif monster_choice == 'orc':
                fighter_component = Fighter(hp=20, defense=0, power=4, xp=35)
                ai_component = BasicMonster()

                monster = Entity(x, y, 'o', colors.desaturated_green, 'Orc', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)

            elif monster_choice == 'troll':
                fighter_component = Fighter(hp=30, defense=2, power=8, xp=100)
                ai_component = BasicMonster()

                monster = Entity(x, y, 'T', colors.darker_green, 'Troll', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)

            entities.append(monster)

    for i in range(number_of_items):
        x = randint(room.x1 + 2, room.x2 - 2)
        y = randint(room.y1 + 2, room.y2 - 2)

        if not any([entity for entity in entities if entity.x == x and entity.y == y]):
            item_choice = random_choice_from_dict(item_chances)

            if item_choice == 'healing_potion':
                item_component = Item(use_function=heal, amount=40)
                item = Entity(x, y, '!', colors.violet, 'Pocao de Cura', render_order=RenderOrder.ITEM, item=item_component)

            elif item_choice == 'sword':
                equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=3)
                item = Entity(x, y, '/', colors.sky, 'Espada Curta', equippable=equippable_component)

            elif item_choice == 'shield':
                equippable_component = Equippable(EquipmentSlots.OFF_HAND, defense_bonus=4)
                item = Entity(x, y, '[', colors.darker_orange, 'Escudo do Homem Pobre', equippable=equippable_component)

            elif item_choice == 'helmet':
                equippable_component = Equippable(EquipmentSlots.HEAD, defense_bonus=1)
                item = Entity(x, y, '^', colors.darker_green, 'Elmo', equippable=equippable_component)

            elif item_choice == 'calca':
                equippable_component = Equippable(EquipmentSlots.CALCA, max_hp_bonus=5)
                item = Entity(x, y, 'V', colors.yellow, 'Calca', equippable=equippable_component)

            elif item_choice == 'peitoral':
                equippable_component = Equippable(EquipmentSlots.PEITORAL, defense_bonus=3)
                item = Entity(x, y, 'H', colors.light_pink, 'Peitoral', equippable=equippable_component)

            elif item_choice == 'bota':
                equippable_component = Equippable(EquipmentSlots.BOTA, defense_bonus=1)
                item = Entity(x, y, 'p', colors.black, 'Bota', equippable=equippable_component)

            elif item_choice == 'fireball_scroll':
                item_component = Item(use_function=cast_fireball, targeting=True, targeting_message=Message(
                    'Clique com o botao esquerdo para selecionar um piso alvo, Clique com o botao direito ou pressione Esc para cancelar', colors.light_cyan), damage=25, radius=3)
                item = Entity(x, y, '#', colors.red, 'Pergaminho da Bola de Fogo', render_order=RenderOrder.ITEM, item=item_component)

            elif item_choice == 'confusion_scroll':
                item_component = Item(use_function=cast_confuse, targeting=True, targeting_message=Message(
                    'Clique com o botao esquerdo para confundir o monstro alvo, Clique com o botao direito ou pressione Esc para cancelar', colors.light_cyan))
                item = Entity(x, y, '#', colors.light_pink, 'Pergaminho da Confusao', render_order=RenderOrder.ITEM, item=item_component)

            else:
                item_component = Item(use_function = cast_lightning, damage=40, maximum_range=5)
                item = Entity(x, y, '#', colors.yellow, 'Pergaminho de Raio', render_order=RenderOrder.ITEM, item=item_component)

            entities.append(item)
