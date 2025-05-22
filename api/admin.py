from django.contrib import admin
from .models import KayakReservation, KayakRoute, KayakRentalSettings, Cabin, CabinReservation, CampingPricing, CampingReservation, BlogPost

admin.site.register(KayakReservation)
admin.site.register(KayakRoute)
admin.site.register(KayakRentalSettings)

@admin.register(Cabin)
class CabinAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_per_night')  # Wyświetlanie nazwy i ceny za dobę
    search_fields = ('name',)  # Możliwość wyszukiwania po nazwie

@admin.register(CabinReservation)
class CabinReservationAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'cabin', 'start_date', 'end_date', 'total_price')  # Wyświetlane pola
    list_filter = ('start_date', 'end_date', 'cabin')  # Filtrowanie po dacie i domku
    search_fields = ('user_name', 'email', 'phone_number')  # Wyszukiwanie po użytkowniku
    ordering = ('start_date',)  # Sortowanie po dacie rozpoczęcia

@admin.register(CampingPricing)
class CampingPricingAdmin(admin.ModelAdmin):
    list_display = ('price_per_adult', 'price_per_child')

@admin.register(CampingReservation)
class CampingReservationAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'start_date', 'end_date', 'adults', 'children', 'total_price')
    search_fields = ('user_name', 'email', 'phone_number')
    ordering = ('start_date',)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    