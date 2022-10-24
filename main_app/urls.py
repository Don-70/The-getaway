from django.urls import path 
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('vacas/', views.vacas_index, name='vacas_index'),
    path('vacas/<int:vaca_id>/', views.vacas_detail, name='vacas_detail'),
    path('vacas/create/', views.VacasCreate.as_view(), name='vacas_create'),
    path('vacas/<int:pk>/update/', views.VacasUpdate.as_view(), name='vacas_update'),
    path('vacas/<int:pk>/delete/', views.VacasDelete.as_view(), name='vacas_delete'),
    path('vacas/<int:vaca_id>/add_traveling/', views.add_traveling, name='add_traveling'),
    path('stuff/create/', views.StuffsCreate.as_view(), name='stuffs_create'),
    path('stuffs/', views.StuffsIndex.as_view(), name='stuffs_index'),
    path('stuffs/<int:pk>/', views.StuffsDetail.as_view(), name='stuffs_detail'),
    path('stuffs/<int:pk>/update/', views.StuffsUpdate.as_view(), name='stuffs_update'),
    path('stuffs/<int:pk>/delete/', views.StuffsDelete.as_view(), name='stuffs_delete'),
    path('vacas/<int:vaca_id>/assoc_stuff/<int:stuff_id>/', views.assoc_stuff, name='assoc_stuff'),
    path('vacas/<int:vaca_id>/add_photo', views.add_photo, name='add_photo'),
    path('accounts/signup/', views.signup, name='signup'),
]