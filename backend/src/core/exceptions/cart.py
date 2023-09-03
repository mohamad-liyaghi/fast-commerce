class CartItemOwnerException(Exception):
    def __init__(self):
        self.message = "You cant add your own product to cart"
        super().__init__(self.message)


class CartItemQuantityException(Exception):
    def __init__(self):
        self.message = "You cant add more than 10 products to cart"
        super().__init__(self.message)


class CartItemNotFound(Exception):
    def __init__(self):
        self.message = "Product not found in cart"
        super().__init__(self.message)
