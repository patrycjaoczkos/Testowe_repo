from django.db import models
from django.contrib.auth.models import User

MONTHS = models.IntegerChoices('Miesiace', 'Styczeń Luty Marzec Kwiecień Maj Czerwiec Lipiec Sierpień Wrzesień Październik Listopad Grudzień')

class Person(models.Model):
    name = models.CharField(max_length=60)
    month_added = models.IntegerField(choices=MONTHS.choices, default=MONTHS.choices[0][0])

    def __str__(self):
        return self.name

class Uzytkownik(models.Model):
    imie = models.CharField(max_length=100, blank=False, null=False)
    nazwisko = models.CharField(max_length=500, blank=False, null=False)
    pseudonim = models.CharField(max_length=100, blank=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.imie} {self.nazwisko}'

class Kuchnia(models.Model):
    nazwa = models.CharField(max_length=100, unique=True)
    opis = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nazwa

class Skladnik(models.Model):
    nazwa = models.CharField(max_length=100, unique=True)
    opis = models.TextField(blank=True, null=True)
    weganin = models.BooleanField(default=True)
    bezglutenowe = models.BooleanField(default=True)

class Przepis(models.Model):
    DIFFICULTY_LEVELS = (
        ('P', 'PROSTY'),
        ('S', 'ŚREDNI'),
        ('T', 'TRUDNY'),
    )

    tytul = models.CharField(max_length=100, blank=False, null=False)
    opis = models.TextField(blank=False, null=False)
    difficulty_levels = models.CharField(max_length=1, choices=DIFFICULTY_LEVELS, default=DIFFICULTY_LEVELS[0][0])
    kuchnia = models.ForeignKey('Kuchnia', on_delete=models.SET_NULL, null=True, blank=True, related_name="przepisy")
    skladniki = models.ManyToManyField('Skladnik', through='PrzepisSkladnik', related_name="przepisy", blank=True)
    instrukcje = models.TextField(blank=False, null=False)
    czas_przygotowania = models.PositiveIntegerField(help_text="Czas przygotowania w minutach", null=True, blank=True)
    czas_gotowania = models.PositiveIntegerField(help_text="Czas gotowania w minutach", null=True, blank=True)
    porcje = models.PositiveIntegerField(null=True, blank=True)
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="przepisy")
    data_utworzenia = models.DateTimeField(auto_now_add=True)
    data_aktualizacji = models.DateTimeField(auto_now=True)
    kategoria = models.CharField(max_length=100, blank=True, null=True)
    obrazek = models.ImageField(upload_to='images/', blank=True, null=True)

    def calkowity_czas(self):
        return self.czas_przygotowania + self.czas_gotowania

    def __str__(self):
        return self.tytul

class UlubionePrzepisy(models.Model):
    uzytkownik = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ulubione_przepisy")
    przepis = models.ForeignKey(Przepis, on_delete=models.CASCADE, related_name="ulubione_przez")
    data_dodania = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.uzytkownik.username} dodał do ulubionych {self.przepis.tytul}"

class PrzepisSkladnik(models.Model):
    przepis = models.ForeignKey(Przepis, on_delete=models.CASCADE)
    skladnik = models.ForeignKey(Skladnik, on_delete=models.CASCADE)
    ilosc = models.CharField(max_length=100, help_text="Ilość składnika (np. 2 łyżki)")

    def __str__(self):
        return f"{self.skladnik.nazwa} w {self.przepis.tytul}"
