class Item:
    def __init__(self, use_function=None, quantity=1, targeting=False, targeting_message=None, **kwargs):
        self.use_function = use_function
        self.quantity = quantity
        self.targeting = targeting
        self.targeting_message = targeting_message
        self.function_kwargs = kwargs
