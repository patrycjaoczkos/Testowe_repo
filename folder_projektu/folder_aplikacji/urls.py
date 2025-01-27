# urls.py:
from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/register/', views.register_user, name='register_user'),
    # API endpoints for Przepis
    path('api/przepisy/', views.przepis_list_api, name='przepis-list-api'),
    path('api/przepisy/<int:pk>/', views.przepis_detail, name='przepis-detail'),

    # API endpoints for Kuchnia
    path('api/kuchnie/', views.kuchnia_list, name='kuchnia-list'),
    path('api/kuchnie/<int:pk>/', views.kuchnia_detail, name='kuchnia-detail'),

    # API endpoints for Skladnik
    path('api/skladniki/', views.skladnik_list, name='skladnik-list'),
    path('api/skladniki/<int:pk>/', views.skladnik_detail, name='skladnik-detail'),

    path('przepisy/', views.przepisy_list_html, name='przepis-list-html'),

    path('przepisy/<int:pk>/', views.przepis_detail_html, name='przepis-detail-html'),
    
     # Widok do wyświetlania ulubionych przepisów
    path('ulubione/', views.ulubione_przepisy, name='ulubione_przepisy'),

    # Widok do dodawania przepisu do ulubionych
    path('add_to_favorites/<int:przepis_id>/', views.add_to_favorites, name='add_to_favorites'),

    # Widok do usuwania przepisu z ulubionych
    path('remove_from_favorites/<int:przepis_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    
    path('api/login/', views.login_user, name='login_user'),
    path('api/register/', views.register_user, name='register_user'),
    path('panel/', views.user_panel, name='user_panel'),
    path('api/logout/', views.logout_user, name='logout_user'),
]
    
    # URL do szczegółów przepisu
    
    # Jeśli masz dodatkowe URL dla innych aplikacji, usuń ten wpis, jeśli nie jest potrzebny
    # path('api/', include('folder_aplikacji.urls')), # Usuń jeśli nie masz tej aplikacji

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)