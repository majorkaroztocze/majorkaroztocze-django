from django.db import models
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets
from django.db.models import Sum, Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from cloudinary.uploader import upload as cloudinary_upload
import mimetypes
from .models import KayakReservation, KayakRoute, KayakRentalSettings, CabinReservation, Cabin, CampingReservation, CampingPricing, BlogPost
from .serializers import KayakReservationSerializer, KayakRouteSerializer, CabinReservationSerializer, CabinSerializer, CampingReservationSerializer, BlogPostSerializer

class KayakReservationViewSet(viewsets.ModelViewSet):
    queryset = KayakReservation.objects.all()
    serializer_class = KayakReservationSerializer

class KayakRouteViewSet(viewsets.ModelViewSet):
    queryset = KayakRoute.objects.all()
    serializer_class = KayakRouteSerializer

@api_view(['GET'])
def kayak_availability(request):
    start_date = request.GET.get('start_date')
    settings = KayakRentalSettings.objects.first()

    booked_kayaks_double = KayakReservation.objects.filter(start_date=start_date).aggregate(models.Sum('kayak_double_quantity'))['kayak_double_quantity__sum'] or 0
    booked_kayaks_single = KayakReservation.objects.filter(start_date=start_date).aggregate(models.Sum('kayak_single_quantity'))['kayak_single_quantity__sum'] or 0
    booked_bags = KayakReservation.objects.filter(start_date=start_date).aggregate(models.Sum('waterproof_bag_quantity'))['waterproof_bag_quantity__sum'] or 0

    available_kayaks_double = settings.total_kayaks_double - booked_kayaks_double
    available_kayaks_single = settings.total_kayaks_single - booked_kayaks_single
    available_bags = settings.total_waterproof_bags - booked_bags

    return Response({
        "available_kayaks_double": available_kayaks_double,
        "available_kayaks_single": available_kayaks_single,
        "available_bags": available_bags
    })



@api_view(['GET'])
def get_prices(request):
    settings = KayakRentalSettings.objects.first()
    if not settings:
        return Response({"error": "Brak ustawień cenowych"}, status=500)

    routes = KayakRoute.objects.all()
    routes_data = KayakRouteSerializer(routes, many=True).data

    return Response({
        "extra_child": settings.price_extra_child,
        "waterproof_bag": settings.price_waterproof_bag,
        "routes": routes_data
    })

@api_view(['POST'])
def kayak_reservation_create(request):
    serializer = KayakReservationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Rezerwacja zapisana!"}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def check_cabin_availability(request):
    """Sprawdza dostępność domku w wybranym terminie."""
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    cabin_id = request.GET.get('cabin_id')

    overlapping_reservations = CabinReservation.objects.filter(
        Q(start_date__lt=end_date, end_date__gt=start_date),
        cabin_id=cabin_id,
    )

    return Response({"is_available": not overlapping_reservations.exists()})

@api_view(['POST'])
def create_cabin_reservation(request):
    data = request.data.copy()
    data.pop('total_price', None)
    serializer = CabinReservationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Rezerwacja zapisana!"}, status=201)

    return Response(serializer.errors, status=400)

@api_view(['GET'])
def get_cabins(request):
    """Zwraca listę wszystkich domków"""
    cabins = Cabin.objects.all()
    serializer = CabinSerializer(cabins, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_cabin_price(request, cabin_id):
    """Zwraca cenę danego domku"""
    try:
        cabin = Cabin.objects.get(id=cabin_id)
        return Response({"cabin_id": cabin.id, "name": cabin.name, "price_per_night": cabin.price_per_night})
    except Cabin.DoesNotExist:
        return Response({"error": "Domek nie istnieje"}, status=404)

@api_view(['GET'])
def get_camping_prices(request):
    """Zwraca aktualne ceny pola namiotowego"""
    pricing = CampingPricing.objects.first()
    if pricing:
        return Response({"price_per_adult": pricing.price_per_adult, "price_per_child": pricing.price_per_child})
    return Response({"error": "Brak cennika"}, status=404)

@api_view(['POST'])
def create_camping_reservation(request):
    """Tworzy nową rezerwację pola namiotowego"""
    serializer = CampingReservationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Rezerwacja zapisana!"}, status=201)

    return Response(serializer.errors, status=400)

@api_view(['GET'])
def get_kayak_route_detail(request, pk):
    try:
        route = KayakRoute.objects.get(pk=pk)
        serializer = KayakRouteSerializer(route)
        return Response(serializer.data)
    except KayakRoute.DoesNotExist:
        return Response({"error": "Trasa nie istnieje"}, status=404)
    
@api_view(['GET'])
def blog_list(request):
    posts = BlogPost.objects.all().order_by('-id')
    serializer = BlogPostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def blog_detail(request, slug):
    try:
        post = BlogPost.objects.get(slug=slug)
        serializer = BlogPostSerializer(post)
        return Response(serializer.data)
    except BlogPost.DoesNotExist:
        return Response({"error": "Post nie istnieje"}, status=status.HTTP_404_NOT_FOUND)

# api/views/ckeditor_upload.py

@csrf_exempt
def ckeditor_image_upload(request):
    if request.method == "POST" and request.FILES.get("upload"):
        file = request.FILES["upload"]

        # Napraw brakujący typ MIME i nazwę
        if not file.content_type:
            file.content_type = mimetypes.guess_type(file.name)[0] or "image/jpeg"
        if not file.name:
            file.name = "uploaded.jpg"

        try:
            result = cloudinary_upload(
                file,
                resource_type="image",
                folder="ckeditor_uploads"
            )
            return JsonResponse({
                "url": result["secure_url"],
                "uploaded": True,
            })
        except Exception as e:
            return JsonResponse({"error": {"message": str(e)}}, status=400)

    return JsonResponse({"error": {"message": "Brak pliku lub nieprawidłowe żądanie"}}, status=400)
