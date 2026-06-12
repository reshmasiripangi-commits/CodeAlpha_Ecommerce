from django.shortcuts import render, get_object_or_404, redirect
from .models import Product,Cart,Order


def home(request):
    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    return render(request,'home.html',
                  {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)

    return render(request, 'product_details.html',
                  {'product': product})
def add_to_cart(request, pk):
    product = Product.objects.get(id=pk)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('/')
def remove_from_cart(request, pk):
    item = Cart.objects.get(id=pk)
    item.delete()
    return redirect('cart')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)

    total = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    return render(
        request,
        'cart.html',
        {
            'cart_items': cart_items,
            'total': total
        }
    )
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = 0
    for item in cart_items:
        total += item.product.price * item.quantity

    order = Order.objects.create(user=request.user, total_price=total)
    order.products.set([item.product for item in cart_items])
    order.save()

    cart_items.delete()
def order_history(request):
    orders = Order.objects.filter(
        user=request.user
    )

    return render(
        request,
        'orders.html',
        {'orders': orders}
    )

    return render(request,'success.html')