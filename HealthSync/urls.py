from . import views
from django.urls import path


urlpatterns =[
    path('', views.index, name='index'),
    path('seznam', views.LekceListView.as_view(), name='seznam_rezervaci'),
    path('detail/<int:pk>', views.LekceDetailView.as_view(), name='detail_rezervace'),
]


