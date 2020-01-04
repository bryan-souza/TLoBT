__all__ = ["GameMap","Rect","create_room","create_h_tunnel","create_v_tunnel",
"make_map","next_floor","place_entities"]

import mechanics.colors as colors
from tdl.map import Map
from random import randint
from components.item import *
from components.fighter import *
from components.ai import *
from components.inventory import *
from components.stairs import *
from components.equipment import *
from components.equippable import *
from mechanics.entity import *
from mechanics.item_functions import *
from mechanics.render_functions import *
from mechanics.game_messages import *
from mechanics.random_utils import *

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

def create_room(game_map, room):
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            game_map.walkable[x, y] = True
            game_map.transparent[x, y] = True

def create_h_tunnel(game_map, x1, x2, y):
    for x in range(min(x1, x2), max(x1, x2) + 1):
        game_map.walkable[x, y] = True
        game_map.transparent[x, y] = True

def create_v_tunnel(game_map, y1, y2, x):
    for y in range(min(y1, y2), max(y1, y2) + 1):
        game_map.walkable[x, y] = True
        game_map.transparent[x, y] = True

def make_map(game_map, MAX_ROOMS, ROOM_MIN_SIZE, ROOM_MAX_SIZE,
MAP_WIDTH, MAP_HEIGHT, player, entities):

    rooms = []
    num_rooms = 0

    center_of_last_room_x = None
    center_of_last_room_y = None

    for r in range(MAX_ROOMS):
        #Largura e altura aleatorias
        w = randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        h = randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        #Posicao aleatoria dentro do limite do mapa
        x = randint(0, MAP_WIDTH - w - 1)
        y = randint(0, MAP_HEIGHT - h - 1)

        #A classe "Rect" torna mais facil trabalhar com retangulos
        new_room = Rect(x, y, w, h)

        #Percorrer as outras salas e checar se elas se interceptam com essa
        for other_room in rooms:
            if new_room.intersect(other_room):
                break
        else:
            #Isso significa que a sala é valida
            #"Pintar" sala no mapa
            create_room(game_map, new_room)

            #coordenadas centrais da sala
            (new_x, new_y) = new_room.center()

            center_of_last_room_x = new_x
            center_of_last_room_y = new_y

            if num_rooms == 0:
                #essa é a primeira sala, onde o player spawna
                player.x = new_x
                player.y = new_y
            else:
                #todas as outras salas
                #conectadas por tuneis

                #coordenadas centrais da sala anterior
                (prev_x, prev_y) = rooms[num_rooms - 1].center()

                #gerar um numero aleatorio (0, 1)
                if randint(0, 1) == 1:
                    #primeiro criar o tunel horizontal e depois o vertical
                    create_h_tunnel(game_map, prev_x, new_x, prev_y)
                    create_v_tunnel(game_map, prev_y, new_y, new_x)
                else:
                    #fazer o contrario
                    create_v_tunnel(game_map, prev_y, new_y, prev_x)
                    create_h_tunnel(game_map, prev_x, new_x, new_y)

            place_entities(new_room, entities, game_map.dungeon_level)

            #finalmente, adicionar a lista de salas
            rooms.append(new_room)
            num_rooms += 1

    stairs_component = Stairs(game_map.dungeon_level + 1)
    down_stairs = Entity(center_of_last_room_x, center_of_last_room_y, '>', colors.white, 'Escadas', render_order=RenderOrder.STAIRS, stairs=stairs_component)
    entities.append(down_stairs)

def next_floor(player, message_log, dungeon_level, constants):
    game_map = GameMap(constants['MAP_WIDTH'], constants['MAP_HEIGHT'], dungeon_level)
    entities = [player]

    make_map(game_map, constants['MAX_ROOMS'], constants['ROOM_MIN_SIZE'],
             constants['ROOM_MAX_SIZE'], constants['MAP_WIDTH'],
             constants['MAP_HEIGHT'], player, entities)

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
        x = randint(room.x1 + 1, room.x2 - 1)
        y = randint(room.y1 + 1, room.y2 - 1)

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
        x = randint(room.x1 + 1, room.x2 - 1)
        y = randint(room.y1 + 1, room.y2 - 1)

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
