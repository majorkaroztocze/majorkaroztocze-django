from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import timedelta
from cloudinary.models import CloudinaryField
from cloudinary_storage.storage import MediaCloudinaryStorage
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field

class KayakRentalSettings(models.Model):
    total_kayaks_double = models.PositiveIntegerField(default=10)
    total_kayaks_single = models.PositiveIntegerField(default=0)
    total_waterproof_bags = models.PositiveIntegerField(default=10)

    # Ceny stałe
    price_extra_child = models.DecimalField(max_digits=6, decimal_places=2, default=10.00)   # Cena dostawki
    price_waterproof_bag = models.DecimalField(max_digits=6, decimal_places=2, default=5.00) # Cena worka

    def __str__(self):
        return f"Dostawka: {self.price_extra_child} PLN, Worek: {self.price_waterproof_bag} PLN"



class KayakRoute(models.Model):
    name = models.CharField(max_length=100)
    duration = models.PositiveIntegerField(help_text="Czas trwania w godzinach")

    # Ceny różne w zależności od trasy
    price_kayak_double = models.DecimalField(max_digits=6, decimal_places=2, default=50.00)  # 2-osobowy
    price_kayak_single = models.DecimalField(max_digits=6, decimal_places=2, default=40.00)  # 1-osobowy

    def __str__(self):
        return f"{self.name} ({self.duration}h) - 2-os: {self.price_kayak_double} PLN, 1-os: {self.price_kayak_single} PLN"


class KayakReservation(models.Model):
    user_name = models.CharField(max_length=255, default="Guest")
    phone_number = models.CharField(max_length=15, default="000-000-000")
    email = models.CharField(max_length=255, null=True, blank=True) 
    kayak_route = models.ForeignKey(KayakRoute, on_delete=models.SET_NULL, null=True)
    kayak_double_quantity = models.PositiveIntegerField(default=0)  # 2-osobowe
    kayak_extra_child_quantity = models.PositiveIntegerField(default=0)  # Dostawki
    kayak_single_quantity = models.PositiveIntegerField(default=0)  # 1-osobowe
    waterproof_bag_quantity = models.PositiveIntegerField(default=0)  # Worki wodoszczelne

    start_date = models.DateField()
    start_time = models.TimeField()

    def clean(self):
        """Sprawdzamy dostępność kajaków i worków"""
        settings = KayakRentalSettings.objects.first()
        if not settings:
            raise ValidationError("Brak ustawień wypożyczalni kajaków!")

        if self.kayak_extra_child_quantity > self.kayak_double_quantity:
            raise ValidationError("Liczba dostawek nie może być większa niż liczba kajaków 2-osobowych.")

        # Sprawdzamy dostępność kajaków i worków
        booked_kayaks_double = KayakReservation.objects.filter(start_date=self.start_date).aggregate(models.Sum('kayak_double_quantity'))['kayak_double_quantity__sum'] or 0
        booked_kayaks_single = KayakReservation.objects.filter(start_date=self.start_date).aggregate(models.Sum('kayak_single_quantity'))['kayak_single_quantity__sum'] or 0
        booked_bags = KayakReservation.objects.filter(start_date=self.start_date).aggregate(models.Sum('waterproof_bag_quantity'))['waterproof_bag_quantity__sum'] or 0

        if booked_kayaks_double + self.kayak_double_quantity > settings.total_kayaks_double:
            raise ValidationError("Brak dostępnych kajaków 2-osobowych na ten dzień.")
        
        if booked_kayaks_single + self.kayak_single_quantity > settings.total_kayaks_single:
            raise ValidationError("Brak dostępnych kajaków 1-osobowych na ten dzień.")

        if booked_bags + self.waterproof_bag_quantity > settings.total_waterproof_bags:
            raise ValidationError("Brak dostępnych worków wodoszczelnych.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

'''domek całoroczny'''

class Cabin(models.Model):
    name = models.CharField(max_length=100)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class CabinReservation(models.Model):
    user_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    start_date = models.DateField()
    end_date = models.DateField()
    cabin = models.ForeignKey('Cabin', on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError("Data zakończenia nie może być wcześniejsza niż data rozpoczęcia.")

    def save(self, *args, **kwargs):
        self.clean()  # zapewnij, że walidacja się wykona
        nights = (self.end_date - self.start_date).days
        self.total_price = nights * self.cabin.price_per_night
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Rezerwacja {self.user_name} - {self.start_date} do {self.end_date}"


class CampingPricing(models.Model):
    price_per_adult = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_child = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Ceny pola namiotowego: Dorosły {self.price_per_adult} PLN, Dziecko {self.price_per_child} PLN"

class CampingReservation(models.Model):
    user_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    start_date = models.DateField()
    end_date = models.DateField()
    adults = models.PositiveIntegerField(default=1)
    children = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError("Data zakończenia nie może być wcześniejsza niż data rozpoczęcia.")

    def save(self, *args, **kwargs):
        self.clean()  # upewnij się, że walidacja zadziała
        nights = (self.end_date - self.start_date).days
        pricing = CampingPricing.objects.first()  # Zakładamy, że tylko jeden zestaw cen
        self.total_price = (
            (self.adults * pricing.price_per_adult + self.children * pricing.price_per_child) * nights
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Rezerwacja {self.user_name} - {self.start_date} do {self.end_date}"


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = CKEditor5Field('Treść', config_name='default')   # html + obrazy
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # SEO
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title