"""
   Model an Order, ShoppingCart
   Define method for creating an order.
"""
from datetime import datetime


class Order:
    """
        Define Order params
    """

    def __init__(self,
                 item_name, item_price, item_id=0
                ):
        """
            Initialize an order object
        """
        self.item_id = item_id
        self.item_name = item_name
        self.item_price = item_price
        self.item_quantity = 1
        self.item_ordered_on = ''

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

    def __repr__(self):
        """
            Define a means or representing ShoppingCart in Terminal
        """
        cart_list = [{item.item_name: item.item_price} for item in self.cart]
        return '{}'.format(cart_list)

    def place_order(self, order_params):
        """
            Render order_params as Order object and
            add Order to cart
        """
        # Check whether item already in cart
        # Add new if not,
        # Increase quantity if yes

        items_in_cart = [item.item_name for item in self.cart]

        if order_params['item_name'] in items_in_cart:
            # If ordered item is already in cart,
            # Increase quantity
            for item in self.cart:
                if item.item_name == order_params['item_name']:
                    order = item
                    order.item_quantity += 1
                    break
        else:
            # Create new order
            order = Order(order_params['item_name'],
                          order_params['item_price']
                          )

            # Assign an item_id to newly created order
            # by making reference to the number of items in cart
            order.item_id = len(self.cart) + 1
            # Append timestamp to order
            order.item_ordered_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Add to shopping cart
            self.cart.append(order)
        return order

    def get_orders(self, order_id=None):
        """
            Retrieve list of all orders so far placed,
            Or single order by id
        """
        result = None

        # Respond to request when no order_id is provided
        # Return all existing orders
        if not order_id:
            result = self.cart

        # Search for single item if order_id is provided
        else:
            for item in self.cart:
                if item.item_id == order_id:
                    result = item
                    break
        return result

    def update_order_status(self, order_id, status):
        """
            Retrieve list of all orders so far placed,
            Or single order by id
        """
        # Search for single item if order_id is provided
        order = self.get_orders(order_id)
        if order:
            order.order_status = status
            order.status_updated_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return order
