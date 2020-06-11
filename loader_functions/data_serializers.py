import json
import sys
import numpy
import inspect

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