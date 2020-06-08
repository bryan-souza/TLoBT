import tdl
import sys
import mechanics.colors as colors
from tcod import image_load
from loader_functions.initialize_new_game import get_constants, get_game_variables
from loader_functions.data_loaders import load_game, save_game
from mechanics.menus import main_menu, messsage_box
from mechanics.game_states import GameStates
from mechanics.render_functions import render_all, clear_all
from mechanics.entity import Entity
from mechanics.input_handlers import handle_main_menu, handle_keys, handle_mouse
from mechanics.game_messages import Message
from mechanics.death_functions import kill_monster, kill_player
from mechanics.entity import get_blocking_entities_at_location
from mechanics.map_utils import next_floor


def main():
    constants = get_constants()

    sys.path.append("..")
    tdl.set_font('images/arial10x10.png', greyscale=True, altLayout=True)

    root_console = tdl.init(
        constants['SCREEN_WIDTH'], constants['SCREEN_HEIGHT'], constants['WINDOW_TITLE'])
    con = tdl.Console(constants['SCREEN_WIDTH'], constants['SCREEN_HEIGHT'])
    panel = tdl.Console(constants['SCREEN_WIDTH'], constants['PANEL_HEIGHT'])

    player = None
    entities = []
    game_map = None
    message_log = None
    game_state = None

    show_main_menu = True
    show_load_error_message = False

    main_menu_background_image = image_load('images/menu_background.png')

    while not tdl.event.is_window_closed():
        for event in tdl.event.get():
            if event.type == 'KEYDOWN':
                user_input = event
                break
        else:
            user_input = None

        if show_main_menu:
            main_menu(con, root_console, main_menu_background_image,
                      constants['SCREEN_WIDTH'], constants['SCREEN_HEIGHT'])
            if show_load_error_message:
                messsage_box(con, root_console, 'Jogo salvo nao encontrado!',
                             50, constants['SCREEN_WIDTH'], constants['SCREEN_HEIGHT'])
            tdl.flush()

            action = handle_main_menu(user_input)

            new_game = action.get('new_game')
            load_saved_game = action.get('load_game')
            exit_game = action.get('exit')

            if show_load_error_message and (new_game or load_saved_game or exit_game):
                show_load_error_message = False
            elif new_game:
                player, entities, game_map, message_log, game_state = get_game_variables(
                    constants)
                game_state = GameStates.PLAYERS_TURN

                show_main_menu = False
            elif load_saved_game:
                try:
                    player, entities, game_map, message_log, game_state = load_game()
                    show_main_menu = False
                except FileNotFoundError:
                    show_load_error_message = True
            elif exit_game:
                break

        else:
            root_console.clear()
            con.clear()
            panel.clear()
            play_game(player, entities, game_map, message_log,
                      game_state, root_console, con, panel, constants)

            show_main_menu = True


def play_game(player, entities, game_map, message_log, game_state, root_console, con, panel, constants):
    sys.path.append("..")
    tdl.set_font('images/arial10x10.png', greyscale=True, altLayout=True)

    fov_recompute = True

    mouse_coordinates = (0, 0)

    previous_game_state = game_state

    targeting_item = None

    while not tdl.event.is_window_closed():
        if fov_recompute:
            game_map.compute_fov(player.x, player.y, fov=constants['FOV_ALGORITHM'],
                                 radius=constants['FOV_RADIUS'], light_walls=constants['FOV_LIGHT_WALLS'])

        render_all(con, panel, entities, player, game_map, fov_recompute, root_console, message_log,
                   constants['SCREEN_WIDTH'], constants['SCREEN_HEIGHT'], constants['BAR_WIDTH'], constants['PANEL_HEIGHT'], constants['PANEL_Y'], mouse_coordinates, constants['Colors'], game_state)
        tdl.flush()

        clear_all(con, entities)

        fov_recompute = False

        for event in tdl.event.get():
            if event.type == 'KEYDOWN':
                user_input = event
                break
            elif event.type == 'MOUSEMOTION':
                mouse_coordinates = event.cell
            elif event.type == 'MOUSEDOWN':
                user_mouse_input = event
                break
        else:
            user_input = None
            user_mouse_input = None

        if not (user_input or user_mouse_input):
            continue

        action = handle_keys(user_input, game_state)
        mouse_action = handle_mouse(user_mouse_input)

        move = action.get('move')
        pickup = action.get('pickup')
        show_inventory = action.get('show_inventory')
        drop_inventory = action.get('drop_inventory')
        inventory_index = action.get('inventory_index')
        take_stairs = action.get('take_stairs')
        level_up = action.get('level_up')
        show_character_screen = action.get('show_character_screen')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        left_click = mouse_action.get('left_click')
        right_click = mouse_action.get('right_click')

        player_turn_results = []

        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy

            # NOCLIP AQUI
            if game_map.walkable[destination_x, destination_y]:
                target = get_blocking_entities_at_location(
                    entities, destination_x, destination_y)

                if target:
                    attack_results = player.fighter.attack(target)
                    player_turn_results.extend(attack_results)
                else:
                    player.move(dx, dy)
                    fov_recompute = True

            game_state = GameStates.ENEMY_TURN

        elif pickup and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if (entity.item) and (entity.x == player.x and entity.y == player.y):
                    pickup_results = player.inventory.add_item(entity)
                    player_turn_results.extend(pickup_results)
                    break
            else:
                message_log.add_message(
                    Message('Nao ha nada aqui para ser pegado', colors.yellow))

        if show_inventory:
            previous_game_state = game_state
            game_state = GameStates.SHOW_INVENTORY

        if drop_inventory:
            previous_game_state = game_state
            game_state = GameStates.DROP_INVENTORY

        if inventory_index is not None and previous_game_state != GameStates.PLAYER_DEAD and inventory_index < len(player.inventory.items):
            item = player.inventory.items[inventory_index]

            if game_state == GameStates.SHOW_INVENTORY:
                player_turn_results.extend(player.inventory.use(
                    item, entities=entities, game_map=game_map))
            elif game_state == GameStates.DROP_INVENTORY:
                player_turn_results.extend(player.inventory.drop_item(item))

        if take_stairs and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.stairs and entity.x == player.x and entity.y == player.y:
                    game_map, entities = next_floor(
                        player, message_log, entity.stairs.floor, constants)
                    fov_recompute = True
                    con.clear()
                    break
            else:
                message_log.add_message(
                    Message('Nao ha uma escadaria aqui.', colors.yellow))

        if level_up:
            if level_up == 'hp':
                player.fighter.base_max_hp += 20
                player.fighter.hp += 20
            elif level_up == 'str':
                player.fighter.base_power += 1
            elif level_up == 'def':
                player.fighter.base_defense += 1

            game_state = previous_game_state

        if show_character_screen:
            previous_game_state = game_state
            game_state = GameStates.CHARACTER_SCREEN

        if game_state == GameStates.TARGETING:
            if left_click:
                target_x, target_y = left_click

                item_use_results = player.inventory.use(
                    targeting_item, entities=entities, game_map=game_map, target_x=target_x, target_y=target_y)
                player_turn_results.extend(item_use_results)
            elif right_click:
                player_turn_results.append({'targeting_cancelled': True})

        if exit:
            if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY, GameStates.CHARACTER_SCREEN):
                game_state = previous_game_state
            elif game_state == GameStates.TARGETING:
                player_turn_results.append({'targeting_cancelled': True})
            else:
                save_game(player, entities, game_map, message_log, game_state)
                return True

        if fullscreen:
            tdl.set_fullscreen(not tdl.get_fullscreen())

        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')
            item_added = player_turn_result.get('item_added')
            item_consumed = player_turn_result.get('consumed')
            item_dropped = player_turn_result.get('item_dropped')
            equip = player_turn_result.get('equip')
            targeting = player_turn_result.get('targeting')
            targeting_cancelled = player_turn_result.get('targeting_cancelled')
            xp = player_turn_result.get('xp')

            if message:
                message_log.add_message(message)

            if dead_entity:
                if dead_entity == player:
                    messsage, game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)

                message_log.add_message(message)

            if item_added:
                entities.remove(item_added)

                game_state = GameStates.ENEMY_TURN

            if item_consumed:
                game_state = GameStates.ENEMY_TURN

            if item_dropped:
                entities.append(item_dropped)

                game_state = GameStates.ENEMY_TURN

            if equip:
                equip_results = player.equipment.toggle_equip(equip)

                for equip_result in equip_results:
                    equipped = equip_result.get('equipped')
                    dequipped = equip_result.get('dequipped')

                    if equipped:
                        message_log.add_message(
                            Message('Voce equipou o(a) {0}'.format(equipped.name)))

                    if dequipped:
                        message_log.add_message(
                            Message('Voce desequipou o(a) {0}'.format(dequipped.name)))

                game_state = GameStates.ENEMY_TURN

            if targeting:
                previous_game_state = GameStates.PLAYERS_TURN
                game_state = GameStates.TARGETING

                targeting_item = targeting

                message_log.add_message(targeting_item.item.targeting_message)

            if targeting_cancelled:
                game_state = previous_game_state

                message_log.add_message(Message('Cancelado'))

            if xp:
                leveled_up = player.level.add_xp(xp)
                message_log.add_message(
                    Message('Voce ganhou {0} pontos de experiencia.'.format(xp)))

                if leveled_up:
                    message_log.add_message(Message(
                        'Suas habilidades de batalha melhoraram! Voce atingiu o nivel {0}'.format(
                            player.level.current_level) + '!',
                        colors.yellow))
                    previous_game_state = game_state
                    game_state = GameStates.LEVEL_UP

        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(
                        player, game_map, entities)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')

                        if message:
                            message_log.add_message(message)

                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            else:
                                message = kill_monster(dead_entity)

                            message_log.add_message(message)

                    if game_state == GameStates.PLAYER_DEAD:
                        break

            else:
                game_state = GameStates.PLAYERS_TURN


if __name__ == '__main__':
    main()
