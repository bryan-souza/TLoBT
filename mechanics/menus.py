__all__= ["menu", "inventory_menu", "main_menu", "messsage_box", "level_up_menu", "character_screen"]

import tdl
import textwrap
import mechanics.colors as colors

def menu(con, root, header, options, width, SCREEN_WIDTH, SCREEN_HEIGHT):
    if len(options) > 26: raise ValueError('Nao se pode haver um menu com mais de 26 opcoes')

    #Calcular a altura total para o cabecalh
    header_wrapped = textwrap.wrap(header, width)
    header_height = len(header_wrapped)
    height = len(options) + header_height

    #Criar um novo console que representa a janela de menu
    window = tdl.Console(width, height)

    #Mostrar cabecalho, com texto
    window.draw_rect(0, 0, width, height, None, fg=colors.white, bg=None)
    for i, line in enumerate(header_wrapped):
        window.draw_str(0, 0 + i, header_wrapped[i])

    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        window.draw_str(0, y, text, bg=None)
        y += 1
        letter_index += 1

    #Mostrar o conteudo da "janela" no console principal
    x = SCREEN_WIDTH // 2 - width // 2
    y = SCREEN_HEIGHT // 2 - height // 2
    root.blit(window, x, y, width, height, 0, 0)

def inventory_menu(con, root, header, player, inventory_width, SCREEN_WIDTH, SCREEN_HEIGHT):
    #Mostrar um menu com cada item do inventario como uma opcao
    if len(player.inventory.items) == 0:
        options = ['O inventario esta vazio']
    else:
        options = []

        for item in player.inventory.items:
            if player.equipment.main_hand == item:
                options.append('{0} (na mao direita)'.format(item.name))
            elif player.equipment.off_hand == item:
                options.append('{0} (na mao esquerda)'.format(item.name))
            else:
                options.append(item.name)

    menu(con, root, header, options, inventory_width, SCREEN_WIDTH, SCREEN_HEIGHT)

def main_menu(con, root_console, background_image, SCREEN_WIDTH, SCREEN_HEIGHT):
    background_image.blit_2x(root_console, 0, 0)

    title = 'THE LEGEND OF BETA TEST'
    center = (SCREEN_WIDTH - len(title)) // 2
    root_console.draw_str(center, SCREEN_HEIGHT // 2 - 4, title, bg=None, fg=colors.light_yellow)

    title = 'By B:/ryan/_Souza'
    center = (SCREEN_WIDTH - len(title)) // 2
    root_console.draw_str(center, SCREEN_HEIGHT - 2, title, bg=None, fg=colors.light_yellow)

    menu(con, root_console, '', ['Novo Jogo', 'Carregar Jogo', 'Sair'], 24, SCREEN_WIDTH, SCREEN_HEIGHT)

def level_up_menu(con, root, header, player, menu_width, SCREEN_WIDTH, SCREEN_HEIGHT):
    options = ['Constituicao (+20 HP, atual: {0})'.format(player.fighter.max_hp),
               'Forca (+1 de Ataque, atual: {0})'.format(player.fighter.power),
               'Defesa (+1 de Defesa, atual: {0})'.format(player.fighter.defense)]

    menu(con, root, header, options, menu_width, SCREEN_WIDTH, SCREEN_HEIGHT)

def character_screen(root_console, player, character_screen_width, character_screen_height, SCREEN_WIDTH, SCREEN_HEIGHT):
    window = tdl.Console(character_screen_width, character_screen_height)

    window.draw_rect(0, 0, character_screen_width, character_screen_height, None, fg=colors.white, bg=None)

    window.draw_str(0, 1, 'Informações do Personagem')
    window.draw_str(0, 2, 'Nivel: {0}'.format(player.level.current_level))
    window.draw_str(0, 3, 'Experiencia: {0}'.format(player.level.current_xp))
    window.draw_str(0, 4, 'Proximo nivel em {0}'.format((player.level.experience_to_next_level - player.level.current_xp)) + ' xp')
    window.draw_str(0, 6, 'HP Maximo: {0}'.format(player.fighter.max_hp))
    window.draw_str(0, 7, 'Ataque: {0}'.format(player.fighter.power))
    window.draw_str(0, 8, 'Defesa: {0}'.format(player.fighter.defense))

    x = SCREEN_WIDTH // 2 - character_screen_width // 2
    y = SCREEN_HEIGHT // 2 - character_screen_height // 2
    root_console.blit(window, x, y, character_screen_width, character_screen_height, 0, 0)

def messsage_box(con, root_console, header, width, SCREEN_WIDTH, SCREEN_HEIGHT):
    menu(con, root_console, header, [], width, SCREEN_WIDTH, SCREEN_HEIGHT)
