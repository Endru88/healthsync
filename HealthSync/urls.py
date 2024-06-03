from . import views
from django.urls import path


urlpatterns =[
    path('', views.index, name='index'),
    path('seznam/', views.LekceListView.as_view(), name='seznam_lekci'),
    path('lekce/<int:pk>', views.LekceDetailView.as_view(), name='detail_lekce'),
    path('lide/', views.OsobaListView.as_view(), name='seznam_osob'),
]


