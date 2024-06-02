from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Lekce, Rezervace


def index(request):
    context = {

    }
    return render(request, 'base.html')


class LekceListView(ListView):
    model = Rezervace
    template_name ='lekce/list.html'
    context_object_name ='lekce_list'
    queryset = Rezervace.objects.order_by('cas')


class LekceDetailView(DetailView):
    model = Rezervace
    template_name ='lekce/detail.html'
    context_object_name ='lekce'

