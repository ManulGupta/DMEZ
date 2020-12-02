from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home),
    path('about/',views.about),
    path('contact/',views.contact),
    path('allproduct/',views.allproduct),
    path('testing/',views.testing),
    path('store/', views.store, name="store"),
    path("products/<int:myid>", views.productView, name="ProductView"),
    path('join/',views.join),
    path('upload/',views.upload),
    path('top/',views.top),
    path('specific/',views.specific),
    path('bestselling/',views.bestselling),
    path('account/',views.account),
    path('consult/',views.consult),

    path('cart/',views.cart, name='cart'),
    path('update_item/',views.updateItem, name='update_item'),
    path('process_order/',views.processOrder, name='process_order'),
    path('checkout/',views.checkout, name='checkout'),
    path('signup/',views.signup, name='signup'),
    path('login/',views.login, name='login'),
    path('logout/',views.logout, name='logout'),
]
