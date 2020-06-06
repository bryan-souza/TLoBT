from mechanics.equipment_slots import EquipmentSlots


class Equipment(object):
    """Um equipamento e suas propriedades"""
    def __init__(self, bota=None, calca=None, peitoral=None, head=None, main_hand=None, off_hand=None, dual_wield=None):
        self.main_hand = main_hand
        self.off_hand = off_hand
        self.dual_wield = dual_wield
        self.head = head
        self.peitoral = peitoral
        self.calca = calca
        self.bota = bota

    @property
    def max_hp_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.max_hp_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.max_hp_bonus

        if self.dual_wield and self.dual_wield.equippable:
            bonus += self.dual_wield.equippable.max_hp_bonus

        if self.bota and self.bota.equippable:
            bonus += self.bota.equippable.max_hp_bonus

        if self.head and self.head.equippable:
            bonus += self.head.equippable.max_hp_bonus

        if self.peitoral and self.peitoral.equippable:
            bonus += self.peitoral.equippable.max_hp_bonus

        if self.calca and self.calca.equippable:
            bonus += self.calca.equippable.max_hp_bonus

        return bonus

    @property
    def power_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.power_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.power_bonus

        if self.bota and self.bota.equippable:
            bonus += self.bota.equippable.power_bonus

        if self.dual_wield and self.dual_wield.equippable:
            bonus += self.dual_wield.equippable.power_bonus

        if self.head and self.head.equippable:
            bonus += self.head.equippable.power_bonus

        if self.calca and self.calca.equippable:
            bonus += self.calca.equippable.power_bonus

        if self.peitoral and self.peitoral.equippable:
            bonus += self.peitoral.equippable.power_bonus
        return bonus

    @property
    def defense_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.defense_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.defense_bonus

        if self.dual_wield and self.dual_wield.equippable:
            bonus += self.dual_wield.equippable.defense_bonus

        if self.bota and self.bota.equippable:
            bonus += self.bota.equippable.defense_bonus

        if self.head and self.head.equippable:
            bonus += self.head.equippable.defense_bonus

        if self.peitoral and self.peitoral.equippable:
            bonus += self.peitoral.equippable.defense_bonus

        if self.calca and self.calca.equippable:
            bonus += self.calca.equippable.defense_bonus
        return bonus

    def toggle_equip(self, equippable_entity):
        results = []

        slot = equippable_entity.equippable.slot

        if slot == EquipmentSlots.MAIN_HAND:
            if self.dual_wield == equippable_entity:
                self.dual_wield = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.dual_wield:
                    results.append({'dequipped': self.dual_wield})

            if self.main_hand == equippable_entity:
                self.main_hand = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.main_hand:
                    results.append({'dequipped': self.main_hand})

                self.main_hand = equippable_entity
                results.append({'equipped': equippable_entity})

        elif slot == EquipmentSlots.OFF_HAND:
            if self.dual_wield == equippable_entity:
                self.dual_wield = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.dual_wield:
                    results.append({'dequipped': self.dual_wield})

            if self.off_hand == equippable_entity:
                self.off_hand = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.off_hand:
                    results.append({'dequipped': self.off_hand})

                self.off_hand = equippable_entity
                results.append({'equipped': equippable_entity})

        elif slot == EquipmentSlots.DUAL_WIELD:
            if self.main_hand == equippable_entity:
                self.main_hand = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.main_hand:
                    results.append({'dequipped': self.main_hand})

            if self.off_hand == equippable_entity:
                self.off_hand = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.off_hand:
                    results.append({'dequipped': self.off_hand})

            if self.dual_wield == equippable_entity:
                self.dual_wield = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.dual_wield:
                    results.append({'dequipped': self.dual_wield})

                self.dual_wield = equippable_entity
                results.append({'equipped': equippable_entity})

        elif slot == EquipmentSlots.HEAD:
            if self.head == equippable_entity:
                self.head = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.head:
                    results.append({'dequipped': self.head})

                self.head = equippable_entity
                results.append({'equipped': equippable_entity})

        elif slot == EquipmentSlots.CALCA:
            if self.calca == equippable_entity:
                self.calca = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.calca:
                    results.append({'dequipped': self.calca})

                self.calca = equippable_entity
                results.append({'equipped': equippable_entity})

        elif slot == EquipmentSlots.PEITORAL:
            if self.peitoral == equippable_entity:
                self.peitoral = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.peitoral:
                    results.append({'dequipped': self.peitoral})

                self.peitoral = equippable_entity
                results.append({'equipped': equippable_entity})

        elif slot == EquipmentSlots.BOTA:
            if self.bota == equippable_entity:
                self.bota = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.bota:
                    results.append({'dequipped': self.bota})

                self.bota = equippable_entity
                results.append({'equipped': equippable_entity})

        return results
