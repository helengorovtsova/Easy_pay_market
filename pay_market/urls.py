
from .views import (
    SuccessView, 
    CancelView, 
    ItemDetailView, 
    BuyItemView, 
    ItemsListView, 
    CreateOrder,
    ClearCartView,
    CheckoutOrder
)

from django.urls import path


urlpatterns = [
    path('items', ItemsListView.as_view(), name='items_list'),
    path('item/<int:pk>', ItemDetailView.as_view(), name='item_detail'),
    path('buy/<int:pk>', BuyItemView.as_view(), name='buy_item'),
    path('add_to_order/', CreateOrder.as_view(), name='create-order'),
    path('add_to_order/<int:pk>', CreateOrder.as_view(), name='create-order'),
    path('success', SuccessView.as_view(), name='success'), 
    path('cancel', CancelView.as_view(), name='cancel'),
    path('clear_cart', ClearCartView.as_view(), name='clear_cart'),
    path('checkout_order', CheckoutOrder.as_view(), name='checkout_order')
]
