"""
    Model an Order, ShoppingCart
    Define methods for
    creating an order, retrieving specific order, retrieving all orders,
    updating an order
"""


class Order:
    """
        Define Order params
    """

    def __init__(self, item_name, item_price, item_id=0, item_quantity=1):
        """
            Initialize an order object
        """
        self.item_id = item_id
        self.item_name = item_name
        self.item_price = item_price
        self.item_quantity = item_quantity

    def __repr__(self):
        """
            Define how Order is represented in Terminal
        """
        return '{} - {} : {}'.format(
            self.item_id, self.item_name, self.item_price)


class ShoppingCart:
    """
        Define ShoppingCart methods
    """

    def __init__(self):
        """
            Initialize ShoppingCart object
        """
        self.cart = []
        self.order_count = 0

    def place_order(self, order_params):
        """
            Render order_params as Order object and
            save Order to 'db'
        """
        order = Order(order_params['item_name'], order_params['item_price'])
        order.item_id = self.order_count
        self.cart.append(order)
