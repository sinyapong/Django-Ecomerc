from .cart import Cart

def cart(request):
    #Return The default data from our Cart
    return {'cart':Cart(request)}