import mechanics.colors as colors
from mechanics.game_messages import Message


class Inventory:
    def __init__(self, capacity, items=None):
        self.capacity = capacity
        if (items == None):
            self.items = []
        else:
            self.items = items

    def add_item(self, item):
        results = []

        if len(self.items) >= self.capacity:
            results.append({
                'item_added': None,
                'message': Message('Voce nao pode carregar mais nada, seu inventario esta cheio!', colors.yellow)
            })
        else:
            results.append({
                'item_added': item,
                'message': Message('Voce pegou o {0}!'.format(item.name), colors.blue)
            })

            for it in self.items:
                # Item ja existente, apenas itens de uso unico sao stackaveis
                if (it.name == item.name) and not (it.equippable):
                    it.item.quantity += 1
                    break
            else:  # Item novo
                self.items.append(item)

        return results

    def use(self, item_entity, **kwargs):
        results = []

        item_component = item_entity.item

        if item_component.use_function is None:
            equippable_component = item_entity.equippable

            if equippable_component:
                results.append({'equip': item_entity})
            else:
                results.append({'message': Message(
                    'O {0} nao pode ser usado.'.format(item_entity.name), colors.yellow)})
        else:
            if item_component.targeting and not (kwargs.get('target_x') or kwargs.get('target_y')):
                results.append({'targeting': item_entity})
            else:
                kwargs = {**item_component.function_kwargs, **kwargs}
                item_use_results = item_component.use_function(
                    self.owner, **kwargs)

                for item_use_result in item_use_results:
                    if item_use_result.get('consumed'):
                        for item in self.items:
                            if (item.item.quantity > 1):  # Item stackado, remover um
                                item.item.quantity -= 1
                                break
                        else:  # Item sozinho, excluir
                            self.remove_item(item_entity)

                results.extend(item_use_results)

        return results

    def remove_item(self, item):
        self.items.remove(item)

    def drop_item(self, item):
        results = []

        if self.owner.equipment.main_hand == item or self.owner.equipment.off_hand == item:
            self.owner.equipment.toggle_equip(item)

        item.x = self.owner.x
        item.y = self.owner.y

        self.remove_item(item)
        results.append({'item_dropped': item, 'message': Message(
            'Voce largou o {0}'.format(item.name), colors.yellow)})

        return results
