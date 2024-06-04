from . import views
from django.urls import path


urlpatterns =[
    path('', views.calendar_view, name='calendar_view'),
    path('events/', views.get_events, name='get_events'),
    path('seznam/', views.LekceListView.as_view(), name='seznam_lekci'),
    path('lekce/<int:pk>', views.LekceDetailView.as_view(), name='detail_lekce'),
    path('lide/', views.OsobaListView.as_view(), name='seznam_osob'),
    path('lide/<int:pk>', views.OsobaDetailView.as_view(), name='detail_osoba'),
]


