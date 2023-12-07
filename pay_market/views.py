from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
import stripe
from django.http import JsonResponse
from .models import Discount, Item, Order, Tax
from django.views.generic import TemplateView, DetailView, View, ListView


class ItemDetailView(DetailView):

    """ Detail view for individual items """

    model = Item
    template_name = 'item_detail.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        context['stripe_public_key'] = settings.STRIPE_PUBLIC_KEY
        return context


class ItemsListView(ListView):

    """ List view for all items """

    model = Item
    template_name = 'items_list.html'
    context_object_name = 'items'


class BuyItemView(View):

    """ Handles purchasing of items """

    def post(self, request, pk):
        item_obj = get_object_or_404(Item, id=pk)
        price_in_cents = int(item_obj.price * 100)
        success_url = '/success'
        cancel_url = '/cancel'
        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': item_obj.name,
                        },
                        'unit_amount': price_in_cents,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri(success_url),
                cancel_url=request.build_absolute_uri(cancel_url),
            )

            return JsonResponse({'session_id': session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)})
            

class CreateOrder(View):

    """ Handles creation of orders """

    def get(self, request):
        # Displays the shopping cart

        items_in_cart = Item.objects.filter(id__in=request.session.get('cart', []))
        
        return render(request, 'view_cart.html', {
                'items': items_in_cart, 
                'items_price': sum([item.price for item in items_in_cart]),
                'public_key': settings.STRIPE_PUBLIC_KEY,
                'checkout': False,
            }
        )

    def post(self, request, pk=None):
        # Adds items to the cart or creates an order

        items_in_cart = Item.objects.filter(id__in=request.session.get('cart', []))
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        if pk:
            item = get_object_or_404(Item, id=pk)
                
            if 'cart' not in request.session:
                request.session['cart'] = []
            
            if item.id not in request.session['cart']:  
                request.session['cart'].append(item.id)
            request.session.save()
            return JsonResponse({'message': f'Item {item.name} added to cart'})
        
        else:
            order = Order.objects.create()
            order.items.add(*Item.objects.filter(id__in=items_in_cart))
            order.discounts.add(*Discount.objects.all())
            order.taxes.add(*Tax.objects.all())
            order.save()
            request.session['current_order'] = order.id
            request.session['total_price'] = str(order.total_price)
            request.session.save()

            return render(request, 'view_cart.html', {
                'items': items_in_cart, 
                'items_price': order.items_price,
                'total_price': order.total_price,
                'public_key': settings.STRIPE_PUBLIC_KEY,
                'checkout': True,
            }
        )


class CheckoutOrder(View):

    """ Handles checkout of orders """

    def post(self, request):
        # Initiates a Stripe checkout session for payment

        order_id = request.session.get('current_order')
        total_price = request.session.get('total_price')
        stripe.api_key = settings.STRIPE_SECRET_KEY
        success_url = '/success'
        cancel_url = '/cancel'
        
        if float(total_price) < 0:
            # Raises an error if the total price is negative
            raise ValueError('Total price cannot be negative') 

        try:
            # Create a Stripe checkout session for payment
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f'Order #{order_id}', 
                        },
                        'unit_amount': int(float(total_price) * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri(success_url),
                cancel_url=request.build_absolute_uri(cancel_url),
            )

            # Return session ID for client-side redirection
            return JsonResponse(
                {
                    'session_id': session.id, 
                    'public_key': settings.STRIPE_PUBLIC_KEY
                }
            )
        
        except Exception as e:
            return JsonResponse({'error': str(e)})
    

class SuccessView(TemplateView):

    """ Handles successful operations """
    
    template_name = 'successful_operation.html'


class CancelView(TemplateView):

    """ Handles cancellation of operations """

    template_name = 'cancel_operation.html'

    
class ClearCartView(View):

    """ Handles clearing of the shopping cart """

    def post(self, request):
        request.session['cart'] = []
        request.session.save()
        return redirect(reverse('create-order'))