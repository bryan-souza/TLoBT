from mechanics import colors
from mechanics.game_messages import Message

def heal(*args, **kwargs):
    #I NEED HEALING - Genji
    entity = args[0]
    amount = kwargs.get('amount')

    results = []

    if entity.fighter.hp == entity.fighter.max_hp:
        results.append({'consumed': False, 'message': Message('Sua vida ja esta completa!', colors.yellow)})
    else:
        entity.fighter.heal(amount)
        results.append({'consumed': True, 'message': Message('Suas feridas se cicatrizam aos poucos', colors.green)})

    return results

def cast_lightning(*args, **kwargs):
    #Feitico de raio
    caster = args[0]
    entities = kwargs.get('entities')
    game_map = kwargs.get('game_map')
    damage = kwargs.get('damage')
    maximum_range = kwargs.get('maximum_range')

    results = []

    target = None
    closest_distance = maximum_range + 1

    for entity in entities:
        if entity.fighter and entity != caster and game_map.fov[entity.x, entity.y]:
            distance = caster.distance_to(entity)

            if distance < closest_distance:
                target = entity
                closest_distance = distance

    if target:
        results.append({'consumed': True, 'target': target, 'message': Message('Um raio atinge o {0} fazendo um barulho estrondoso! Levou {1} de dano!'.format(target.name, damage))})
        results.extend(target.fighter.take_damage(damage))
    else:
        results.append({'consumed': False, 'target': None, 'message': Message('Nao ha inimigo proximo o suficiente para atingir', colors.red)})

    return results

def cast_fireball(*args, **kwargs):
    #Feitico de bola de fogo
    entities = kwargs.get('entities')
    game_map = kwargs.get('game_map')
    damage = kwargs.get('damage')
    radius = kwargs.get('radius')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not game_map.fov[target_x, target_y]:
        results.append({'consumed': False, 'message': Message('Voce nao pode almejar um piso fora do seu campo de visao', colors.yellow)})

        return results

    results.append({'consumed': True, 'message': Message('A bola de fogo explode, queimando tudo no raio de {0} pisos!'.format(radius), colors.orange)})

    for entity in entities:
        if entity.distance(target_x, target_y) <= radius and entity.fighter:
            results.append({'message': Message('O {0} se queima, levando {1} de dano'.format(entity.name, damage), colors.orange)})
            results.extend(entity.fighter.take_damage(damage))

    return results
