from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Person, Uzytkownik, Przepis, Kuchnia, Skladnik, Recenzja, UlubionePrzepisy, NarzedzieKuchenne
from .serializers import (
    PrzepisSerializer,
    KuchniaSerializer,
    SkladnikSerializer,
    RecenzjaSerializer,
    UlubionePrzepisySerializer,
    NarzedzieKuchenneSerializer,
)


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
    """Usuwa konkretną osobę."""
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
def przepis_list(request):
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
def przepis_detail(request, pk):
    przepis = get_object_or_404(Przepis, pk=pk)

    if request.method == 'GET':
        serializer = PrzepisSerializer(przepis)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PrzepisSerializer(przepis, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
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

# Widoki API dla modelu Recenzja
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def recenzja_create(request):
    serializer = RecenzjaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(uzytkownik=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Widoki HTML

def przepis_list_html(request):
    przepisy = Przepis.objects.all()
    return render(request, 'przepisy/przepis_list.html', {'przepisy': przepisy})

def przepis_detail_html(request, pk):
    przepis = get_object_or_404(Przepis, pk=pk)
    return render(request, 'przepisy/przepis_detail.html', {'przepis': przepis})
