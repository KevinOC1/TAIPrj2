class Comic:
    def __init__(self, id, title, image_url, price, stock):
        self.id = id
        self.title = title
        self.image_url = image_url
        self.price = price
        self.stock = stock

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