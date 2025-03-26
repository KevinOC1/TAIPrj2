class Comic:
    def __init__(self, id, title, image_url, price, stock):
        self.id = id
        self.title = title
        self.image_url = image_url
        self.price = price
        self.stock = stock

class Order:
    def __init__(self, id, customer_name, products, date, total, status):
        self.id = id
        self.customer_name = customer_name
        self.products = products
        self.date = date
        self.total = total
        self.status = status

# Datos de ejemplo para los cómics
comics_db = [
    Comic(1, "Dragon Ball Super Vol. 1", "/static/images/comic.png", 50.8, 52),
    Comic(2, "Dragon Ball Super Vol. 2", "/static/images/comic.png", 50.8, 52),
    Comic(3, "Dragon Ball Super Vol. 3", "/static/images/comic.png", 50.8, 52),
    Comic(4, "Dragon Ball Super Vol. 4", "/static/images/comic.png", 50.8, 52),
    Comic(5, "Dragon Ball Super Vol. 5", "/static/images/comic.png", 50.8, 52),
    Comic(6, "Dragon Ball Super Vol. 6", "/static/images/comic.png", 50.8, 52),
    Comic(7, "Dragon Ball Super Vol. 7", "/static/images/comic.png", 50.8, 52),
    Comic(8, "Dragon Ball Super Vol. 8", "/static/images/comic.png", 50.8, 52),
]

# Funciones para manipular datos
def get_all_comics():
    return comics_db

def get_comic_by_id(comic_id):
    for comic in comics_db:
        if comic.id == comic_id:
            return comic
    return None

def update_comic(comic_id, price=None, stock=None):
    comic = get_comic_by_id(comic_id)
    if comic:
        if price is not None:
            comic.price = price
        if stock is not None:
            comic.stock = stock
        return True
    return False

# Datos de ejemplo para los pedidos
orders_db = [
    Order(1, "Juan Pérez", ["Dragon Ball Super Vol. 1", "Dragon Ball Super Vol. 2"], "2023-05-15", 101.6, "Entregado"),
    Order(2, "María González", ["Dragon Ball Super Vol. 3"], "2023-05-18", 50.8, "En proceso"),
    Order(3, "Carlos Rodríguez", ["Dragon Ball Super Vol. 4", "Dragon Ball Super Vol. 5", "Dragon Ball Super Vol. 6"], "2023-05-20", 152.4, "Pendiente"),
    Order(4, "Ana López", ["Dragon Ball Super Vol. 7"], "2023-05-22", 50.8, "Cancelado"),
    Order(5, "Roberto Martínez", ["Dragon Ball Super Vol. 8", "Dragon Ball Super Vol. 1"], "2023-05-25", 101.6, "Entregado"),
]

def get_all_orders():
    return orders_db

def get_order_by_id(order_id):
    for order in orders_db:
        if order.id == order_id:
            return order
    return None