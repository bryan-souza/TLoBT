__all__ = ["kill_player","kill_monster"]

import mechanics.colors as colors
from mechanics.game_states import *
from mechanics.render_functions import *
from mechanics.game_messages import *

def kill_player(player):
    player.char = '%'
    player.color = colors.dark_red

    return Message('Voce morreu!', colors.red), GameStates.PLAYER_DEAD

def kill_monster(monster):
    death_message = Message('{0} morreu!'.format(monster.name.capitalize()), colors.orange)

    monster.char = '%'
    monster.color = colors.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'restos de ' + monster.name
    monster.render_order = RenderOrder.CORPSE

    return death_message
