from components.ai import ConfusedMonster
from mechanics.game_messages import Message
from mechanics import colors

def cast_confuse(*args, **kwargs):
    #Feitico de confusao
    entities = kwargs.get('entities')
    game_map = kwargs.get('game_map')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not game_map.fov[target_x, target_y]:
        results.append({'consumed': False, 'message': Message('Voce nao pode almejar um alvo fora do seu campo de visao', colors.yellow)})

        return results

    for entity in entities:
        if entity.x == target_x and entity.y == target_y and entity.ai:
            confused_ai = ConfusedMonster(entity.ai, 10)

            confused_ai.owner = entity
            entity.ai = confused_ai

            results.append({'consumed': True, 'message': Message('O {0} ficou confuso!'.format(entity.name), colors.light_green)})
            break

    else:
        results.append({'consumed': False, 'message': Message('Nao ha um alvo valido nessa localizacao', colors.yellow)})

    return results