from rest_framework.permissions import BasePermission

class IsAuthorOrReadOnly(BasePermission):
    """
    Pozwala na pełny dostęp tylko autorowi obiektu.
    Pozostali użytkownicy mają tylko dostęp do odczytu.
    """
    def has_object_permission(self, request, view, obj):
        # Zezwolenie na odczyt dla wszystkich użytkowników
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        
        # Pełny dostęp tylko dla autora
        return obj.autor == request.user


class IsAuthenticatedOrPostOnly(BasePermission):
    """
    Zezwala na wykonanie żądania POST bez uwierzytelnienia.
    Wymaga uwierzytelnienia dla innych metod HTTP.
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return request.user and request.user.is_authenticated


class IsAdminOrReadOnly(BasePermission):
    """
    Zezwala administratorom na pełny dostęp, a innym użytkownikom tylko na odczyt.
    """
    def has_permission(self, request, view):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return request.user and request.user.is_staff


class IsUserOrReadOnly(BasePermission):
    """
    Pozwala użytkownikom na dostęp tylko do własnych obiektów.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return obj.uzytkownik == request.user
