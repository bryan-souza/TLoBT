import mechanics.colors as colors
from mechanics.game_states import GameStates
from mechanics.menus import inventory_menu, level_up_menu, character_screen
from enum import Enum

class RenderOrder(Enum):
    STAIRS = 1
    CORPSE = 2
    ITEM = 3
    ACTOR = 4

def get_names_under_mouse(mouse_coordinates, entities, game_map):
    x, y = mouse_coordinates

    names = [entity.name for entity in entities
             if entity.x == x and entity.y == y and game_map.fov[entity.x, entity.y]]
    names = ', '.join(names)

    return names.capitalize()

def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color, string_color):
    #Renderizar uma barra
    bar_width = int(float(value) / maximum * total_width)

    #Renderizar o background primeiro
    panel.draw_rect(x, y, total_width, 1, None, bg=back_color)

    #Renderizar a barra
    if bar_width > 0:
        panel.draw_rect(x, y, bar_width, 1, None, bg=back_color)

    #Renderizar o texto centralizado e valores
    text = name + ': ' + str(value) + '/' + str(maximum)
    x_centered = x + int((total_width-len(text)) / 2)

    panel.draw_str(x_centered, y, text, fg=string_color, bg=None)

def render_all(con, panel, entities, player, game_map, fov_recompute, root_console, message_log, SCREEN_WIDTH, SCREEN_HEIGHT, BAR_WIDTH, PANEL_HEIGHT, PANEL_Y, mouse_coordinates, Colors, game_state):
    #Desenhar todos os pisos do mapa
    if fov_recompute:
        for x, y in game_map:
            wall = not game_map.transparent[x, y]

            if game_map.fov[x, y]:
                if wall:
                    con.draw_char(x, y, None, fg=None, bg=Colors.get('light_wall'))
                else:
                    con.draw_char(x, y, None, fg=None, bg=Colors.get('light_ground'))

                game_map.explored[x][y] = True
            elif game_map.explored[x][y]:
                if wall:
                    con.draw_char(x, y, None, fg=None, bg=Colors.get('dark_wall'))
                else:
                    con.draw_char(x, y, None, fg=None, bg=Colors.get('dark_ground'))

    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)

    #Desenhar todos os objetos da lista
    for entity in entities_in_render_order:
        draw_entity(con, entity, game_map)

    root_console.blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0)

    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        if game_state == GameStates.SHOW_INVENTORY:
            inventory_title = 'Pressione o botao proximo ao item para usa-lo, ou Esc para cancelar.\n'
        else:
            inventory_title = 'Pressione o botao proximo ao item para larga-lo, ou Esc para cancelar.\n'

        inventory_menu(con, root_console, inventory_title, player, 50, SCREEN_WIDTH, SCREEN_HEIGHT)

    elif game_state == GameStates.LEVEL_UP:
        level_up_menu(con, root_console, 'Subiu de nível! Escolha um atributo para melhorar.', player, 40, SCREEN_WIDTH, SCREEN_HEIGHT)

    elif game_state == GameStates.CHARACTER_SCREEN:
        character_screen(root_console, player, 30, 10, SCREEN_WIDTH, SCREEN_HEIGHT)

    panel.clear(fg=colors.white, bg=colors.black)

    #Mostrar as mensagens do jogo, uma linha por vez
    y = 1
    for message in message_log.messages:
        panel.draw_str(message_log.x, y, message.text, bg=None, fg=message.color)
        y += 1

    render_bar(panel, 1, 1, BAR_WIDTH, 'HP', player.fighter.hp, player.fighter.max_hp, colors.light_red, colors.darker_red, colors.white)
    panel.draw_str(1, 3, 'Andar: {0}'.format(game_map.dungeon_level), fg=colors.white, bg=None)

    panel.draw_str(1, 0, get_names_under_mouse(mouse_coordinates, entities, game_map))

    root_console.blit(panel, 0, PANEL_Y, SCREEN_WIDTH, PANEL_HEIGHT, 0, 0)

def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)

def draw_entity(con, entity, game_map):
    if game_map.fov[entity.x, entity.y] or (entity.stairs and game_map.explored[entity.x][entity.y]):
        con.draw_char(entity.x, entity.y, entity.char, entity.color, bg=None)

def clear_entity(con, entity):
    #Apagar o caractere que representa esse objeto
    con.draw_char(entity.x, entity.y, ' ', entity.color, bg=None)
