from rest_framework import serializers
from .models import Person, Uzytkownik, Kuchnia, Skladnik, NarzedzieKuchenne, PreferencjeDietetyczne, Przepis, Recenzja, UlubionePrzepisy, MONTHS
from datetime import date


class PersonSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True)
    month_added = serializers.ChoiceField(choices=MONTHS.choices, default=MONTHS.choices[0][0])

    def validate_name(self, value):
        if not value.istitle():
            raise serializers.ValidationError(
                "Nazwa osoby powinna rozpoczynać się wielką literą!"
            )
        return value

    def create(self, validated_data):
        return Person.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.month_added = validated_data.get('month_added', instance.month_added)
        instance.save()
        return instance


class UzytkownikSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uzytkownik
        fields = ['id', 'imie', 'nazwisko', 'pseudonim', 'email', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class KuchniaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kuchnia
        fields = ['id', 'nazwa', 'opis']
        read_only_fields = ['id']


class SkladnikSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skladnik
        fields = ['id', 'nazwa', 'opis', 'weganin', 'bezglutenowe']
        read_only_fields = ['id']


class NarzedzieKuchenneSerializer(serializers.ModelSerializer):
    odpowiednie_dla = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Kuchnia.objects.all()
    )

    class Meta:
        model = NarzedzieKuchenne
        fields = ['id', 'nazwa', 'opis', 'odpowiednie_dla']
        read_only_fields = ['id']


class PreferencjeDietetyczneSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreferencjeDietetyczne
        fields = ['id', 'uzytkownik', 'weganin', 'wegetarianin', 'bezglutenowe', 'alergie']
        read_only_fields = ['id']


class PrzepisSerializer(serializers.ModelSerializer):
    skladniki = serializers.PrimaryKeyRelatedField(many=True, queryset=Skladnik.objects.all())
    kuchnia = serializers.PrimaryKeyRelatedField(queryset=Kuchnia.objects.all())

    class Meta:
        model = Przepis
        fields = [
            'id', 'tytul', 'opis', 'difficulty_levels', 'kuchnia', 'skladniki',
            'instrukcje', 'czas_przygotowania', 'czas_gotowania', 'porcje',
            'autor', 'data_utworzenia', 'data_aktualizacji'
        ]
        read_only_fields = ['id', 'autor', 'data_utworzenia', 'data_aktualizacji']


class RecenzjaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recenzja
        fields = ['id', 'przepis', 'uzytkownik', 'ocena', 'komentarz', 'data_utworzenia']
        read_only_fields = ['id', 'uzytkownik', 'data_utworzenia']


class UlubionePrzepisySerializer(serializers.ModelSerializer):
    class Meta:
        model = UlubionePrzepisy
        fields = ['id', 'uzytkownik', 'przepis', 'data_dodania']
        read_only_fields = ['id', 'data_dodania']
