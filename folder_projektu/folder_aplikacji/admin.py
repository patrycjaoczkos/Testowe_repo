# Admin.py:

from django.contrib import admin
from .models import Person, Uzytkownik, Kuchnia, Skladnik, NarzedzieKuchenne, PreferencjeDietetyczne, Przepis, Recenzja, UlubionePrzepisy, PrzepisSkladnik

# Rejestracja modelu Person z dekoratorem i konfiguracją list_display oraz filtrami
@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['name', 'month_added']
    list_filter = ['month_added']
    search_fields = ['name']

# Rejestracja modelu Uzytkownik
@admin.register(Uzytkownik)
class UzytkownikAdmin(admin.ModelAdmin):
    list_display = ['imie', 'nazwisko', 'pseudonim', 'email', 'date_joined']
    list_filter = ['date_joined']
    search_fields = ['imie', 'nazwisko', 'email', 'pseudonim']

# Rejestracja modelu Kuchnia
@admin.register(Kuchnia)
class KuchniaAdmin(admin.ModelAdmin):
    list_display = ['nazwa', 'opis']
    list_filter = ['nazwa']
    search_fields = ['nazwa']

# Rejestracja modelu Skladnik
@admin.register(Skladnik)
class SkladnikAdmin(admin.ModelAdmin):
    list_display = ['nazwa', 'weganin', 'bezglutenowe', 'opis']
    list_filter = ['weganin', 'bezglutenowe']
    search_fields = ['nazwa']

# Rejestracja modelu NarzedzieKuchenne
@admin.register(NarzedzieKuchenne)
class NarzedzieKuchenneAdmin(admin.ModelAdmin):
    list_display = ['nazwa', 'opis']
    list_filter = ['odpowiednie_dla']
    search_fields = ['nazwa']

# Rejestracja modelu PreferencjeDietetyczne
@admin.register(PreferencjeDietetyczne)
class PreferencjeDietetyczneAdmin(admin.ModelAdmin):
    list_display = ['uzytkownik', 'weganin', 'wegetarianin', 'bezglutenowe', 'alergie_info']
    list_filter = ['weganin', 'wegetarianin', 'bezglutenowe']
    search_fields = ['uzytkownik__username']

    @admin.display(description="Alergie (tekst)")
    def alergie_info(self, obj):
        return obj.alergie if obj.alergie else "Brak alergii"

# Rejestracja modelu Przepis
@admin.register(Przepis)
class PrzepisAdmin(admin.ModelAdmin):
    list_display = ['tytul', 'difficulty_levels', 'kuchnia', 'czas_przygotowania', 'czas_gotowania', 'porcje', 'autor', 'data_utworzenia']
    list_filter = ['difficulty_levels', 'kuchnia', 'autor']
    search_fields = ['tytul', 'kuchnia__nazwa', 'autor__username']

# Rejestracja modelu Recenzja
@admin.register(Recenzja)
class RecenzjaAdmin(admin.ModelAdmin):
    list_display = ['przepis', 'uzytkownik', 'ocena', 'data_utworzenia']
    list_filter = ['ocena']
    search_fields = ['przepis__tytul', 'uzytkownik__username']

# Rejestracja modelu UlubionePrzepisy
@admin.register(UlubionePrzepisy)
class UlubionePrzepisyAdmin(admin.ModelAdmin):
    list_display = ['uzytkownik', 'przepis', 'data_dodania']
    list_filter = ['data_dodania']
    search_fields = ['uzytkownik__username', 'przepis__tytul']

# Rejestracja modelu PrzepisSkladnik
@admin.register(PrzepisSkladnik)
class PrzepisSkladnikAdmin(admin.ModelAdmin):
    list_display = ['przepis', 'skladnik', 'ilosc']
    search_fields = ['przepis__tytul', 'skladnik__nazwa']
