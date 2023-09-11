class InappropriateOrderStatus(Exception):
    def __init__(self, message="Inappropriate order status were given"):
        self.message = message
        super().__init__(self.message)
