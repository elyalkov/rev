#КОРЗИНА ЧЕРЕЗ СЕССИИ (ЧЕРЕЗ COCKIE)
from django.conf import settings
from reverence.main.models import ClothingItem


class Cart: #класс управляет добавлением, удалением и хранением товаров в корзине пользователя
    def __init__(self, request): #gолучает объект request, чтобы обратиться к сессии
        self.session = request.session #инициализирует сессию
        cart = self.session.get(settings.CART_SESSION_ID) #смотрит, есть ли в сессии корзина с ключом settings.CART_SESSION_ID
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {} #если нет, создаёт пустую корзину
        self.cart = cart #сохраняет

    def add(self, product, quantity=1, override_quantity=False): #добавляет товар в корзину
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):  #позволяет перебирать товары в корзине, как в списке
        product_ids = self.cart.keys()
        products = ClothingItem.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = float(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(float(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()