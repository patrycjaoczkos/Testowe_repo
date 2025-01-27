from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import Person, Przepis, Kuchnia, PrzepisSkladnik, Skladnik, UlubionePrzepisy
from .serializers import (PersonSerializer, PrzepisSerializer, KuchniaSerializer,SkladnikSerializer, UserSerializer,  # Dodajemy serializer dla użytkownika
)
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt

@login_required
def toggle_favorite(request, przepis_id):
    """
    Widok obsługujący dodanie lub usunięcie przepisu z ulubionych.
    """
    przepis = get_object_or_404(Przepis, id=przepis_id)
    ulubione, created = UlubionePrzepisy.objects.get_or_create(uzytkownik=request.user, przepis=przepis)

    if not created:
        ulubione.delete()  # Usuń z ulubionych
        return JsonResponse({"status": "removed"})
    else:
        return JsonResponse({"status": "added"})
# Widok rejestracji użytkownika
@api_view(['POST'])
def register_user(request):
    """Rejestracja nowego użytkownika."""
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User registered successfully!",
                "username": user.username,
                "email": user.email,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Widoki API dla modelu Person

@api_view(['GET'])
def person_list(request):
    """Zwraca listę wszystkich osób."""
    people = Person.objects.all()
    serializer = PersonSerializer(people, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def person_detail(request, pk):
    """Zwraca szczegóły konkretnej osoby."""
    try:
        person = Person.objects.get(pk=pk)
    except Person.DoesNotExist:
        return Response({'error': 'Person not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = PersonSerializer(person)
    return Response(serializer.data)


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def person_update(request, pk):
    """Aktualizuje dane konkretnej osoby."""
    try:
        person = Person.objects.get(pk=pk)
    except Person.DoesNotExist:
        return Response({'error': 'Person not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = PersonSerializer(person, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def person_delete(request, pk):
    """Usuwa konkretną osobę (tylko administrator może usunąć)."""
    try:
        person = Person.objects.get(pk=pk)
    except Person.DoesNotExist:
        return Response({'error': 'Person not found'}, status=status.HTTP_404_NOT_FOUND)

    person.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# Widoki API dla modelu Przepis

@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def przepis_list_api(request):
    if request.method == 'GET':
        przepisy = Przepis.objects.all()
        serializer = PrzepisSerializer(przepisy, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PrzepisSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(autor=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def przepis_detail(request, pk):
    przepis = get_object_or_404(Przepis, pk=pk)

    if request.method == 'GET':
        serializer = PrzepisSerializer(przepis)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # Użytkownik może edytować tylko swoje przepisy
        if przepis.autor != request.user and not request.user.is_staff:
            return Response({"error": "You can only edit your own recipes."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = PrzepisSerializer(przepis, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Użytkownik może usuwać tylko swoje przepisy, lub administratorzy mogą usuwać wszystkie
        if przepis.autor != request.user and not request.user.is_staff:
            return Response({"error": "You can only delete your own recipes."}, status=status.HTTP_403_FORBIDDEN)
        
        przepis.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Widoki API dla modelu Kuchnia

@api_view(['GET', 'POST'])
def kuchnia_list(request):
    if request.method == 'GET':
        kuchnie = Kuchnia.objects.all()
        serializer = KuchniaSerializer(kuchnie, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = KuchniaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def kuchnia_detail(request, pk):
    kuchnia = get_object_or_404(Kuchnia, pk=pk)

    if request.method == 'GET':
        serializer = KuchniaSerializer(kuchnia)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = KuchniaSerializer(kuchnia, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        kuchnia.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Widoki API dla modelu Skladnik

@api_view(['GET', 'POST'])
def skladnik_list(request):
    if request.method == 'GET':
        skladniki = Skladnik.objects.all()
        serializer = SkladnikSerializer(skladniki, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SkladnikSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def skladnik_detail(request, pk):
    skladnik = get_object_or_404(Skladnik, pk=pk)

    if request.method == 'GET':
        serializer = SkladnikSerializer(skladnik)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SkladnikSerializer(skladnik, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        skladnik.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Widok API dla Recenzja

def przepis_detail_html(request, pk):
    przepis = Przepis.objects.get(pk=pk)
    przepisy_skladniki = PrzepisSkladnik.objects.filter(przepis=przepis)
    
    return render(request, 'przepis_detail.html', {'przepis': przepis, 'przepisy_skladniki': przepisy_skladniki})

def przepisy_list_html(request):
    search_query = request.GET.get('search', '')  # Pobieramy zapytanie z formularza
    przepisy = Przepis.objects.all()

    if search_query:
        przepisy = przepisy.filter(tytul__icontains=search_query)  # Filtrowanie po tytule przepisu

    return render(request, 'przepisy_list.html', {'przepisy': przepisy})


@login_required
def ulubione_przepisy(request):
    """Wyświetla listę ulubionych przepisów zalogowanego użytkownika."""
    ulubione = UlubionePrzepisy.objects.filter(uzytkownik=request.user)
    przepisy = [ulubiony.przepis for ulubiony in ulubione]
    return render(request, 'ulubione_przepisy.html', {'przepisy': przepisy})

# Widok do dodawania przepisu do ulubionych
@login_required
def add_to_favorites(request, przepis_id):
    """Dodaje przepis do ulubionych użytkownika."""
    przepis = get_object_or_404(Przepis, id=przepis_id)

    # Sprawdzamy, czy przepis już jest w ulubionych
    if UlubionePrzepisy.objects.filter(uzytkownik=request.user, przepis=przepis).exists():
        return JsonResponse({'message': 'Przepis już w ulubionych'}, status=400)

    # Tworzymy nowy obiekt UlubionePrzepisy
    UlubionePrzepisy.objects.create(uzytkownik=request.user, przepis=przepis)
    return JsonResponse({'message': 'Przepis dodany do ulubionych'}, status=200)

# Widok do usuwania przepisu z ulubionych
@login_required
def remove_from_favorites(request, przepis_id):
    """Usuwa przepis z ulubionych użytkownika."""
    przepis = get_object_or_404(Przepis, id=przepis_id)

    # Sprawdzamy, czy przepis jest w ulubionych
    ulubiony = UlubionePrzepisy.objects.filter(uzytkownik=request.user, przepis=przepis)
    if not ulubiony.exists():
        return JsonResponse({'message': 'Przepis nie jest w ulubionych'}, status=400)

    # Usuwamy przepis z ulubionych
    ulubiony.delete()
    return JsonResponse({'message': 'Przepis usunięty z ulubionych'}, status=200)


@api_view(['POST'])
def register_user(request):
    """Rejestracja nowego użytkownika."""
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User registered successfully!",
                "username": user.username,
                "email": user.email,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    """Logowanie użytkownika."""
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({"message": "Zalogowano pomyślnie!"}, status=status.HTTP_200_OK)
    return Response({"error": "Nieprawidłowa nazwa użytkownika lub hasło."}, status=status.HTTP_401_UNAUTHORIZED)

login_required
def user_panel(request):
    """Panel użytkownika."""
    return render(request, 'user_panel.html', {'user': request.user})
@csrf_exempt
@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Użytkownik zarejestrowany pomyślnie!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def logout_user(request):
    """Wylogowanie użytkownika."""
    logout(request)
    return redirect('/')