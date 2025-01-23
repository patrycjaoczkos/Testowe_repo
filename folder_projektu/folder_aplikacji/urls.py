# urls.py:
from django.urls import include, path
from . import views

urlpatterns = [
    # API endpoints for Przepis
    path('api/przepisy/', views.przepis_list_api, name='przepis-list-api'),
    path('api/przepisy/<int:pk>/', views.przepis_detail, name='przepis-detail'),

    # API endpoints for Kuchnia
    path('api/kuchnie/', views.kuchnia_list, name='kuchnia-list'),
    path('api/kuchnie/<int:pk>/', views.kuchnia_detail, name='kuchnia-detail'),

    # API endpoints for Skladnik
    path('api/skladniki/', views.skladnik_list, name='skladnik-list'),
    path('api/skladniki/<int:pk>/', views.skladnik_detail, name='skladnik-detail'),

    # API endpoint for Recenzja
    path('api/recenzje/', views.recenzja_create, name='recenzja-create'),

    # HTML views
    path('przepisy/', views.przepis_list_html, name='przepis-list-html'),
    path('przepisy/<int:pk>/', views.przepis_detail_html, name='przepis-detail-html'),
    
    # Jeśli masz dodatkowe URL dla innych aplikacji, usuń ten wpis, jeśli nie jest potrzebny
    # path('api/', include('folder_aplikacji.urls')), # Usuń jeśli nie masz tej aplikacji
]
