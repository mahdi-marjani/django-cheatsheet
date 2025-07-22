from .cart import Cart

def cart_func(request):
    return {'cart': Cart(request)}