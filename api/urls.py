from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import KayakReservationViewSet, KayakRouteViewSet, kayak_availability, get_prices, kayak_reservation_create, check_cabin_availability, create_cabin_reservation, get_cabins, get_cabin_price, get_camping_prices, create_camping_reservation, get_kayak_route_detail, blog_list, blog_detail

router = DefaultRouter()
router.register(r'kayak_reservations', KayakReservationViewSet)
router.register(r'kayak_routes', KayakRouteViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('kayak_availability/', kayak_availability, name='kayak_availability'),
    path('prices/', get_prices, name='get_prices'),
    path('kayak_reservations/', kayak_reservation_create, name='kayak_reservations'),
    path('check_cabin_availability/', check_cabin_availability, name='check_cabin_availability'),
    path('create_cabin_reservation/', create_cabin_reservation, name='create_cabin_reservation'),
    path('cabins/', get_cabins, name='cabins'),
    path('cabin_price/<int:cabin_id>/', get_cabin_price),
    path('camping_prices/', get_camping_prices),
    path('create_camping_reservation/', create_camping_reservation),
    path('kayak_route/<int:pk>/', get_kayak_route_detail),
    path('blog/', blog_list, name='blog-list'),
    path('blog/<slug:slug>/', blog_detail, name='blog-detail'),
]
