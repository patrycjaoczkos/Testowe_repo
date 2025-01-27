from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Person, Uzytkownik, Kuchnia, Skladnik, Przepis, UlubionePrzepisy, MONTHS
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

class PrzepisSerializer(serializers.ModelSerializer):
    # Zmiana PrimaryKeyRelatedField na serializer, aby pokazać pełne dane
    skladniki = SkladnikSerializer(many=True, read_only=True)  # Pokaż pełne dane składników
    kuchnia = KuchniaSerializer(read_only=True)  # Pokaż pełne dane kuchni

    class Meta:
        model = Przepis
        fields = [
            'id', 'tytul', 'opis', 'difficulty_levels', 'kuchnia', 'skladniki',
            'instrukcje', 'czas_przygotowania', 'czas_gotowania', 'porcje',
            'autor', 'data_utworzenia', 'data_aktualizacji'
        ]
        read_only_fields = ['id', 'autor', 'data_utworzenia', 'data_aktualizacji']

class UlubionePrzepisySerializer(serializers.ModelSerializer):
    class Meta:
        model = UlubionePrzepisy
        fields = ['id', 'uzytkownik', 'przepis', 'data_dodania']
        read_only_fields = ['id', 'data_dodania']


class UserSerializer(serializers.ModelSerializer):
    """Serializer dla modelu User, umożliwiający rejestrację użytkowników"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}  # Hasło jest tylko do zapisu

    def create(self, validated_data):
        """Tworzy nowego użytkownika i zapisuje hasło w postaci zaszyfrowanej"""
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
    class UserSerializer(serializers.ModelSerializer):
        password = serializers.CharField(write_only=True)  # Hasło tylko do zapisu

    class Meta:
        model = User
        fields = ['username', 'email', 'password']  # Pola wymagane do rejestracji

    def create(self, validated_data):
        """Tworzy nowego użytkownika z zaszyfrowanym hasłem"""
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user