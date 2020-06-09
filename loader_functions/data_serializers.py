import json
import sys
sys.path.append('.')

from mechanics import colors
from mechanics.render_functions import RenderOrder
from mechanics.entity import Entity
from mechanics.map_utils import GameMap
from mechanics.game_states import GameStates
from mechanics.game_messages import MessageLog, Message

from loader_functions.initialize_new_game import get_game_variables, get_constants
player, entities, game_map, message_log, game_state = get_game_variables(get_constants())

from components.ai import BasicMonster, ConfusedMonster, Apprentice
from components.equipment import Equipment, EquipmentSlots
from components.equippable import Equippable
from components.level import Level
from components.inventory import Inventory
from components.fighter import Fighter
from components.item import Item
from components.stairs import Stairs

def serializeEntity(entity:Entity, mode='python'):
    if not (entity == None):
        base_dict = {
            'x': entity.x,
            'y': entity.y,
            'char': entity.char,
            'color': entity.color,
            'name': entity.name,
            'blocks': entity.blocks,
            'render_order': serializeRenderOrder(entity.render_order),
            'fighter': serializeFighter(entity.fighter),
            'ai': serializeAi(entity.ai),
            'item': serializeItem(entity.item),
            'inventory': serializeInventory(entity.inventory),
            'stairs': serializeStairs(entity.stairs),
            'level': serializeLevel(entity.level),
            'equipment': serializeEquipment(entity.equipment),
            'equippable': serializeEquippable(entity.equippable)
        }

        if (mode == 'json'):
            return json.dumps(base_dict, indent=4)
        else:
            return base_dict
    else:
        return None

def serializeFighter(fighter:Fighter, mode='python'):
    if not (fighter == None):
        base_dict = {
            'base_max_hp': fighter.base_max_hp,
            'max_hp': fighter.max_hp,
            'hp': fighter.hp,
            'base_defense': fighter.base_defense,
            'defense': fighter.defense,
            'base_power': fighter.base_power,
            'power': fighter.power,
            'xp': fighter.xp,
        }

        if (mode == 'json'):
            return json.dumps(base_dict, indent=4)
        else:
            return base_dict
    else:
        return None

def serializeInventory(inventory:Inventory, mode='python'):
    if not (inventory == None):
        items = []
        for item in inventory.items:
            items.append(serializeEntity(item))
        
        base_dict = {
            'capacity': inventory.capacity,
            'items': items
        }
        
        if (mode == 'json'):
            return json.dumps(base_dict, indent=4)
        else:
            return base_dict
    else:
        return None

def serializeLevel(level:Level, mode='python'):
    if not (level == None):
        base_dict = {
            'current_level': level.current_level,
            'current_xp': level.current_xp,
            'level_up_base': level.level_up_base,
            'level_up_factor': level.level_up_factor,
            'experience_to_next_level': level.experience_to_next_level
        }

        if (mode == 'json'):
            return json.dumps(base_dict, indent=4)
        else:
            return base_dict
    else:
        return None

def serializeEquipment(equipment:Equipment, mode='python'):
    if not (equipment == None):
        base_dict = {
            'main_hand': serializeEntity(equipment.main_hand),
            'off_hand': serializeEntity(equipment.off_hand),
            'dual_wield': serializeEntity(equipment.dual_wield),
            'head': serializeEntity(equipment.head),
            'peitoral': serializeEntity(equipment.peitoral),
            'calca': serializeEntity(equipment.calca),
            'bota': serializeEntity(equipment.bota),
            'max_hp_bonus': equipment.max_hp_bonus,
            'power_bonus': equipment.power_bonus,
            'defense_bonus': equipment.defense_bonus,
        }

        if (mode == 'json'):
            return json.dumps(base_dict, indent=4)
        else:
            return base_dict
    else:
        return None

def serializeEquippable(equippable:Equippable, mode='python'):
    if not (equippable == None):
        base_dict = {
            'slot': serializeEquipmentSlots(equippable.slot),
            'power_bonus': equippable.power_bonus,
            'defense_bonus': equippable.defense_bonus,
            'max_hp_bonus': equippable.max_hp_bonus
        }

        if (mode == 'json'):
            return json.dumps(base_dict, indent=4)
        else:
            return base_dict
    else:
        return None

def serializeItem(item:Item, mode='python'):
    if not (item == None):
        base_dict = {
            'use_function': str(item.use_function),
            'quantity': item.quantity,
            'targeting': item.targeting,
            'targeting_message': item.targeting_message,
            'kwargs': item.function_kwargs
        }

        if (mode == 'json'):
            return json.dumps(base_dict, indent=4)
        else:
            return base_dict
    else:
        return None

def serializeStairs(stairs:Stairs, mode='python'):
    if not (stairs == None):
        base_dict = {
            'floor': stairs.floor
        }

        if (mode == 'json'):
            return json.dumps(base_dict, indent=4)
        else:
            return base_dict
    else:
        return None

def serializeAi(ai, mode='python'):
    if not (ai == None):
        if (type(ai) == BasicMonster):
            base_dict = {}
        elif (type(ai) == ConfusedMonster):
            base_dict = {
                'previous_ai': ai.previous_ai,
                'number_of_turns': ai.number_of_turns,
            }
        elif (type(ai) == Apprentice):
            base_dict = {
                'cooldown': ai.cooldown,
                'attr': ai.attr
            }
        else:
            return TypeError

        if (mode == 'json'):
            return json.dumps(base_dict, indent=4)
        else:
            return base_dict
    else:
        return None

def serializeRenderOrder(render_order:RenderOrder, mode='python'):
    base_dict = {
        'name': render_order.name,
        'value': render_order.value
    }

    if (mode == 'json'):
        return json.dumps(base_dict, indent=4)
    else:
        return base_dict

def serializeEquipmentSlots(equipment_slot:EquipmentSlots, mode='python'):
    base_dict = {
        'name': equipment_slot.name,
        'value': equipment_slot.value
    }
    
    if (mode == 'json'):
        return json.dumps(base_dict, indent=4)
    else:
        return base_dict

def serializeGameMap(game_map:GameMap, mode='python'):
    if not (game_map == None):
        base_dict = {
            'width': game_map.width,
            'height': game_map.height,
            'dungeon_level': game_map.dungeon_level,
            'explored': game_map.explored,
            'transparent': game_map.transparent.tolist(),
            'walkable': game_map.walkable.tolist()
        }

        if (mode == 'json'):
            return json.dumps(base_dict, indent=4)
        else:
            return base_dict
    else:
        return None

def serializeMessage(message:Message, mode='python'):
    if not (message == None):
        base_dict = {
            'text': message.text,
            'color': message.color
        }

        if (mode == 'json'):
            return json.dumps(base_dict, indent=4)
        else:
            return base_dict
    else:
        return None

def serializeMessageLog(message_log:MessageLog, mode='python'):
    if not (message_log == None):
        messages = []
        for message in message_log.messages:
            messages.append(serializeMessage(message))

        base_dict = {
            'messages': messages,
            'x': message_log.x,
            'width': message_log.width,
            'height': message_log.height,
        }

        if (mode == 'json'):
            return json.dumps(base_dict, indent=4)
        else:
            return base_dict
    else:
        return None

def serializeGameState(game_state:GameStates, mode='python'):
    if not (game_state == None):
        base_dict = {
            'name': game_state.name,
            'value': game_state.value
        }

        if (mode == 'json'):
            return json.dumps(base_dict, indent=4)
        else:
            return base_dict
    else:
        return None