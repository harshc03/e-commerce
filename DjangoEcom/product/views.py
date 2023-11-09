from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from .models import *
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import base64
def product_detail(request, product_id):
    # Retrieve the product data
    product = get_object_or_404(Product, id=product_id)
    
    # Retrieve the related product images
    product_images = ProductImage.objects.filter(product_id_id=product_id)
    desc = Description.objects.filter(product_id=product_id)

    # Create a context dictionary with both product and product_images
    context = {
        'product': product,
        'product_images': product_images,
        'desc': desc,
    }

    return render(request, 'product/product_page.html', context)
    
def product_page(request):
    return render(request,'product/product_page.html')


def product_list(request):

    # Fetch featured products with their first images
    products = Product.objects.all().annotate(first_image=models.Subquery(
        ProductImage.objects.filter(product_id=models.OuterRef('pk')).values('image')[:1]
    ))

    # Add your logic to fetch and display the product list and cart data here
    # ...

    return render(request, 'product/product_listing.html', {'products': products})
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Check if the user has an active cart, create one if not
    if not request.user.is_anonymous:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        # Handle the case where the user is not authenticated
        # You can implement your own logic here
        pass

    # Check if the product is already in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    # If the product was already in the cart, increment its quantity
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect(reverse('product_page', kwargs={'product_id': product_id}))
def view_cart(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Get or create the user's cart
        user_cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = user_cart.cartitem_set.all()
    else:
        cart_items = []

    context = {
        'cart_items': cart_items,
    }

    return render(request, 'product/cart_detail.html', context)

def remove_from_cart(request):
    item_id = request.GET.get('item_id')

    if item_id:
        try:
            # Attempt to get the CartItem by its ID and delete it
            cart_item = CartItem.objects.get(id=item_id)
            cart_item.delete()
        except CartItem.DoesNotExist:
            pass  # Handle the case where the item does not exist

    return redirect('view_cart')  # Redirect to your shopping cart page
def checkout_view(request):
    return render(request, 'product/checkout.html')
# def checkout(request):
#     if request.method == 'POST':
#         # Assuming you have a function to get the current user, e.g., get_current_user()
#         user = get_current_user(request)

#         # Loop through the cart items and create an order for each item
#         for cart_item in user.cart_items.all():
#             order = Order(
#                 user=user,
#                 product=cart_item.product,
#                 quantity=cart_item.quantity,
#                 total_price=cart_item.total_price
#             )
#             order.save()
        
#         # Clear the user's cart after placing the order
#         user.cart_items.all().delete()

#         # You can also display a success message here
#         return render(request, 'checkout_success.html')

#     return render(request, 'checkout.html')