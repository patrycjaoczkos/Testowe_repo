from django.db import models 
from django.contrib.auth.models import User

# Model Kuchnia reprezentuje różne kuchnie świata, np. włoska, azjatycka.
# Posiada pola: nazwa (unikalna) i opis (opcjonalny).
class Kuchnia(models.Model):
    nazwa = models.CharField(max_length=100, unique=True)
    opis = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nazwa

# Model Skladnik przechowuje informacje o składnikach kulinarnych.
# Zawiera nazwę, opis oraz informacje o tym, czy składnik jest wegański i bezglutenowy.
class Skladnik(models.Model):
    nazwa = models.CharField(max_length=100, unique=True)
    opis = models.TextField(blank=True, null=True)
    czy_weganin = models.BooleanField(default=True)
    czy_bezglutenowe = models.BooleanField(default=True)

    def __str__(self):
        return self.nazwa

# Model Przepis przechowuje przepisy kulinarne.
# Posiada tytuł, opis, przypisaną kuchnię, składniki, instrukcje, czas przygotowania i gotowania,
# liczbę porcji, autora oraz daty utworzenia i aktualizacji.
class Przepis(models.Model):
    tytul = models.CharField(max_length=200)
    opis = models.TextField()
    kuchnia = models.ForeignKey(Kuchnia, on_delete=models.CASCADE, related_name="przepisy")
    skladniki = models.ManyToManyField(Skladnik, through='PrzepisSkladnik', related_name="przepisy")
    instrukcje = models.TextField()
    czas_przygotowania = models.PositiveIntegerField(help_text="Czas przygotowania w minutach")
    czas_gotowania = models.PositiveIntegerField(help_text="Czas gotowania w minutach")
    porcje = models.PositiveIntegerField()
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="przepisy")
    data_utworzenia = models.DateTimeField(auto_now_add=True)
    data_aktualizacji = models.DateTimeField(auto_now=True)

    def calkowity_czas(self):
        return self.czas_przygotowania + self.czas_gotowania

    def __str__(self):
        return self.tytul

# Model PrzepisSkladnik reprezentuje relację składników w przepisach.
# Zawiera informacje o ilości i jednostce danego składnika w przepisie.
class PrzepisSkladnik(models.Model):
    przepis = models.ForeignKey(Przepis, on_delete=models.CASCADE)
    skladnik = models.ForeignKey(Skladnik, on_delete=models.CASCADE)
    ilosc = models.DecimalField(max_digits=6, decimal_places=2)
    jednostka = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.ilosc} {self.jednostka} {self.skladnik.nazwa} w {self.przepis.tytul}"

# Model Recenzja przechowuje recenzje przepisów od użytkowników.
# Zawiera ocenę (1-5), opcjonalny komentarz oraz informacje o dacie utworzenia.
class Recenzja(models.Model):
    przepis = models.ForeignKey(Przepis, on_delete=models.CASCADE, related_name="recenzje")
    uzytkownik = models.ForeignKey(User, on_delete=models.CASCADE)
    ocena = models.PositiveIntegerField(default=1, choices=[(i, str(i)) for i in range(1, 6)])
    komentarz = models.TextField(blank=True, null=True)
    data_utworzenia = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recenzja od {self.uzytkownik.username} - {self.ocena} gwiazdek"

# Model UlubionePrzepisy przechowuje listę ulubionych przepisów użytkownika.
# Zawiera odniesienie do użytkownika i przepisu oraz datę dodania.
class UlubionePrzepisy(models.Model):
    uzytkownik = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ulubione_przepisy")
    przepis = models.ForeignKey(Przepis, on_delete=models.CASCADE, related_name="ulubione_przez")
    data_dodania = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.uzytkownik.username} dodał do ulubionych {self.przepis.tytul}"

# Model PoradaKulinarna przechowuje porady kulinarne od użytkowników.
# Zawiera tytuł, treść, autora oraz datę utworzenia.
class PoradaKulinarna(models.Model):
    tytul = models.CharField(max_length=200)
    tresc = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="porady")
    data_utworzenia = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tytul

# Model NarzedzieKuchenne reprezentuje narzędzia kuchenne (np. mikser, nóż).
# Zawiera nazwę, opis oraz powiązania z kuchniami, w których narzędzie jest używane.
class NarzedzieKuchenne(models.Model):
    nazwa = models.CharField(max_length=100, unique=True)
    opis = models.TextField(blank=True, null=True)
    odpowiednie_dla = models.ManyToManyField(Kuchnia, blank=True, related_name="narzedzia_kuchenne")

    def __str__(self):
        return self.nazwa

# Model PlanPosilkow pozwala użytkownikom tworzyć plany posiłków.
# Zawiera nazwę, opis, przepisy, autora oraz datę utworzenia.
class PlanPosilkow(models.Model):
    nazwa = models.CharField(max_length=100)
    opis = models.TextField(blank=True, null=True)
    przepisy = models.ManyToManyField(Przepis, related_name="plany_posilkow")
    stworzony_przez = models.ForeignKey(User, on_delete=models.CASCADE, related_name="plany_posilkow")
    data_utworzenia = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nazwa

# Model PreferencjeDietetyczne przechowuje preferencje dietetyczne użytkownika.
# Zawiera informacje o weganizmie, wegetarianizmie, bezglutenowości oraz ewentualnych alergiach.
class PreferencjeDietetyczne(models.Model):
    uzytkownik = models.OneToOneField(User, on_delete=models.CASCADE, related_name="preferencje_dietetyczne")
    czy_weganin = models.BooleanField(default=False)
    czy_wegetarianin = models.BooleanField(default=False)
    czy_bezglutenowe = models.BooleanField(default=False)
    alergie = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Preferencje dietetyczne dla {self.uzytkownik.username}"

# Deklaracja statycznej listy wyboru do wykorzystania w klasie modelu.
class Person(models.Model):
    name = models.CharField(max_length=60)
    month_added = models.IntegerField(choices=models.DateField().MONTHS.items(), default=1)

    def __str__(self):
        return self.name

class CustomUser(models.Model):
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Recipe(models.Model):
    DIFFICULTY_LEVELS = (
        ('P', 'Prosty'),
        ('S', 'Średni'),
        ('T', 'Trudny'),
    )

    title = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    difficulty_level = models.CharField(max_length=1, choices=DIFFICULTY_LEVELS, default='P')

    def __str__(self):
        return self.title
