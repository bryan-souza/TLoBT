from random import randint
import mechanics.colors as colors
from mechanics.game_messages import *

class Fighter:
    def __init__(self, hp, defense, power, xp=0):
        self.base_max_hp = hp
        self.hp = hp
        self.base_defense = defense
        self.base_power = power
        self.xp = xp

    @property
    def max_hp(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.max_hp_bonus
        else:
            bonus = 0

        return self.base_max_hp + bonus

    @property
    def power(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.power_bonus
        else:
            bonus = 0

        return self.base_power + bonus

    @property
    def defense(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.defense_bonus
        else:
            bonus = 0

        return self.base_defense + bonus

    def heal(self, amount):
        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def take_damage(self, amount):
        results = []

        self.hp -= amount

        if self.hp <= 0:
            results.append({'dead': self.owner, 'xp': self.xp})

        return results

    def attack(self, target):
        results = []

        dice = randint(0, 20)
        if dice < 19:
            damage = self.power - target.fighter.defense
        else:
            damage = (self.power - target.fighter.defense) * 2

        if damage > 0:
            if dice <= 19:
                results.append({'message': Message('{0} ataca {1}, causando {2} de dano'.format(self.owner.name.capitalize(), target.name, str(damage)))})
                results.extend(target.fighter.take_damage(damage))
            elif dice == 20:
                results.append({'message': Message('DANO CRITICO!!', colors.yellow)})
                results.append({'message': Message('{0} ataca {1}, causando {2} de dano'.format(self.owner.name.capitalize(), target.name, str(damage)), colors.yellow)})
            else:
                results.append({'message': Message('{0} erra o ataque!'.format(self.owner.name.capitalize()))})
        else:
            results.append({'message': Message('{0} ataca {1}, mas nao causa dano'.format(self.owner.name.capitalize(), target.name))})


        return results
