import json
import sys
import numpy
import inspect
from mechanics import colors
from mechanics import entity, equipment_slots, game_messages, render_functions, item_functions, special_item_functions, map_utils
from components import ai, equipment, equippable, fighter, inventory, item, level, stairs

# DEBUG
# data = {}
# with open('savegame.json', 'r') as savegame:
#     data = json.load(savegame)

def serialize(data):
    # Obter nome da classe geradora
    class_name = data.__class__.__name__
    if (class_name == 'function'): # Caso especial: use_function
        class_name = data.__name__

    # Obter os atributos da classe
    attrs = inspect.getmembers(data, lambda a:not(inspect.isroutine(a)))
    new_attrs = [a for a in attrs if not(a[0].startswith('__') and a[0].endswith('__'))]
    class_args = {}
    for attr in new_attrs:
        k, v = attr
        class_args.update({k:v})

    # Dicionario de saída
    serial_args = {}
    # Inserir o nome da classe/função
    serial_args.update({'class_name': class_name})

    # Casos especiais
    # Geralmente são classes com @property
    if (class_name == 'RenderOrder' or class_name == 'EquipmentSlots' or class_name == 'GameStates'): # Classes tipo EnumMeta
        # Remover a propriedade name
        class_args.pop('name')
    elif (class_name == 'Equipment'):  # Classes tipo Equipment
        class_args.pop('defense_bonus')
        class_args.pop('power_bonus')
        class_args.pop('max_hp_bonus')
    elif (class_name == 'Fighter'): # Classes tipo Fighter
        class_args.pop('max_hp')
    elif (class_name == 'Level'): # Classe tipo Level
        class_args.pop('experience_to_next_level')
    elif (class_name == 'GameMap'): # Classe tipo GameMap
        class_args.pop('_Map__buffer')
        class_args.pop('_order')

    for k, v in class_args.items():
        try:
            json.dumps({k:v}) # Checar se o valor é dumpável
            # Se sim, adicionar ao novo dicionario
            serial_args.update({k:v})

        except TypeError: # Erro: objeto não dumpável, serializar
            if not ((k == '__objclass__') or (k == 'owner') or (k == 'map_c')):
                if (type(v) == list):
                    new_list = []
                    for item in v:
                        new_item = serialize(item)
                        new_list.append(new_item)
                    
                    new_v = new_list

                elif (type(v) == numpy.ndarray):
                    new_v = v.tolist()
                else:
                    new_v = serialize(v)

                serial_args.update({k:new_v})

    return serial_args

def deserialize(data:dict):
    modules = [
        entity, 
        equippable, 
        equipment, 
        equipment_slots, 
        game_messages, 
        map_utils, 
        render_functions, 
        item_functions,
        special_item_functions,
        ai,
        equipment, 
        equippable, 
        fighter,
        inventory,
        item,
        level,
        stairs
    ]

    # Checar por itens deserializaveis
    for k, v in data.items():
        if ((type(v) == dict) and (len(v) > 0) and not(k == 'function_kwargs')): # Significa que é um objeto, deserializar
            new_v = deserialize(v)
            data.update({k:new_v})
        
        elif ((type(v) == list) and (data['class_name'] == 'Inventory' or data['class_name'] == 'MessageLog')): # Caso especial: inventário
            new_v = []
            for it in v:
                new_v.append(deserialize(it)) # Deserializar cada item do inventário
            
            data.update({k:new_v})
            
    for m in modules:
        try: # Encontrar classe geratriz
            base_class = getattr(m, data['class_name'])
            if (data['class_name'] == 'GameMap'): # Resolver os decorators do Map
                game_map = base_class(data['width'], data['height'], data['dungeon_level']) # Instanciar classe
                game_map.explored = data['explored'] # Atualizar blocos explorados
                walk = data['walkable']
                transp = data['transparent']
                for x in range(len(walk)):
                    for y in range(len(walk[x])):
                        game_map.walkable[x, y] = walk[x][y] # Setar blocos andaveis
                        game_map.transparent[x, y] = transp[x][y] # Setar blocos transparentes
                    
                return game_map

            data.pop('class_name')
            break
        except:
            pass
    
    return base_class(**data)