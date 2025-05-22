from rest_framework import serializers
from bs4 import BeautifulSoup
from .models import KayakReservation, KayakRoute, KayakRentalSettings, CabinReservation, Cabin, CampingReservation, BlogPost

class KayakRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = KayakRoute
        fields = '__all__'

class KayakRentalSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = KayakRentalSettings
        fields = '__all__'


class KayakReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = KayakReservation
        fields = '__all__'

        def validate(self, data):
            if data['kayak_extra_child_quantity'] > data['kayak_double_quantity']:
                raise serializers.ValidationError("Liczba dostawek nie może być większa niż liczba kajaków 2-osobowych.")
            return data

    def validate(self, data):
        reservation = KayakReservation(**data)
        reservation.clean()  # Sprawdzenie dostępności kajaków
        return data

class CabinReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CabinReservation
        fields = '__all__'
        read_only_fields = ['total_price']

class CabinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cabin
        fields = '__all__'

class CampingReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampingReservation
        fields = '__all__'
        read_only_fields = ['total_price']  # Cena obliczana automatycznie


class BlogPostSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    excerpt = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = [
            'id',
            'title',
            'slug',
            'content',
            'meta_title',
            'meta_description',
            'image',
            'excerpt'
                # dodajemy dynamiczne pole z obrazkiem
        ]

    def get_image(self, obj):
        """Wydobywa pierwszy obraz z treści HTML."""
        soup = BeautifulSoup(obj.content, 'html.parser')
        first_img = soup.find('img')
        return first_img['src'] if first_img and 'src' in first_img.attrs else None
    
    def get_excerpt(self, obj):
        soup = BeautifulSoup(obj.content or "", 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        print(">>> DEBUG excerpt:", repr(text[:200])) 
        return text[:200] + "..." if len(text) > 200 else text