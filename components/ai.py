from random import randint
from mechanics.entity import Entity
from mechanics.render_functions import RenderOrder
from mechanics import colors
from mechanics.item_functions import cast_lightning, cast_fireball
from mechanics.game_messages import Message
from components.item import Item
from components.inventory import Inventory

class BasicMonster:
    def take_turn(self, target, game_map, entities):
        results = []

        monster = self.owner

        if game_map.fov[monster.x, monster.y]:
            if monster.distance_to(target) >= 2:
                monster.move_towards(target.x, target.y, game_map, entities)

            elif target.fighter.hp > 0:
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)

        else:
            random_x = monster.x + randint(0, 2) - 1
            random_y = monster.y + randint(0, 2) - 1

            if random_x != monster.x and random_y != monster.y:
                monster.move_towards(random_x, random_y, game_map, entities)

        return results

class ConfusedMonster:
    def __init__(self, previous_ai, number_of_turns=10):
        self.previous_ai = previous_ai
        self.number_of_turns = number_of_turns

    def take_turn(self, target, game_map, entities):
        results = []

        if self.number_of_turns > 0:
            random_x = self.owner.x + randint(0, 2) - 1
            random_y = self.owner.y + randint(0, 2) - 1

            if random_x != self.owner.x and random_y != self.owner.y:
                self.owner.move_towards(random_x, random_y, game_map, entities)

            self.number_of_turns -= 1
        else:
            self.owner.ai = self.previous_ai
            results.append({'message': Message('O {0} nao esta mais confuso!'.format(self.owner.name))})

        return results

class Apprentice:
    def __init__(self, cooldown=0, attr=None):
        self.cooldown = cooldown
        self.attr = attr
        chance = randint(0, 100)

        if chance > 49:
            #Criar Mago do Relampago
            self.attr = 'lightning'

        else:
            #Criar Mago Bola de Fogo
            self.attr = 'fireball'


    def take_turn(self, target, game_map, entities):
        results = []
        monster = self.owner

        if self.attr == 'lightning':
            monster.color = colors.light_cyan
            item_component = Item(use_function=cast_lightning, damage=6, maximum_range=6)
            item = Entity(monster.x, monster.y, '#', colors.yellow, 'Pergaminho de Raio', render_order=RenderOrder.ITEM, item=item_component)
            monster.inventory.items.append(item)

        else:
            monster.color = colors.red
            if target is not None and game_map.fov[monster.x, monster.y]:
                item_component = Item(use_function=cast_fireball, target_x=target.x, target_y=target.y, damage=6, radius=3)
                item = Entity(monster.x, monster.y, '#', colors.red, 'Pergaminho da Bola de Fogo', render_order=RenderOrder.ITEM, item=item_component)
                monster.inventory.items.append(item)

        if self.cooldown == 0: #Modo Ofensivo
            if game_map.fov[monster.x, monster.y]:
                if monster.distance_to(target) >= 5:
                    monster.move_towards(target.x, target.y, game_map, entities)

                elif target.fighter.hp > 0:
                    attack_results = monster.inventory.use(monster.inventory.items[0], entities=entities, game_map=game_map)
                    results.extend(attack_results)
                    self.cooldown = 3

        else: #Modo Defensivo
            random_x = monster.x + randint(0, 2) - 1
            random_y = monster.y + randint(0, 2) - 1

            if random_x != monster.x and random_y != monster.y:
                monster.move_towards(random_x, random_y, game_map, entities)

            self.cooldown -= 1

        return results
