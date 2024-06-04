from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from datetime import timedelta
from .models import Lekce, Osoba, Rezervace


def index(request):
    return render(request, 'base.html')

class LekceListView(ListView):
    model = Lekce
    template_name ='lekce/lekce_list.html'
    context_object_name ='lekce_list'
    queryset = Lekce.objects.order_by('start')


class LekceDetailView(DetailView):
    model = Lekce
    template_name ='lekce/lekce_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rezervace_list'] = Rezervace.objects.filter(lekce=self.get_object())
        return context


class OsobaListView(ListView):
    model = Osoba
    template_name ='osoba/list.html'
    context_object_name ='osoba_list'
    queryset = Osoba.objects.order_by('status')

class OsobaDetailView(DetailView):
    model = Lekce
    template_name ='osoba/list_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rezervace_list'] = Rezervace.objects.filter(lekce=self.get_object())
        return context


def calendar_view(request):
    return render(request, 'index.html')


def get_events(request):
    start = request.GET.get('start', '')
    end = request.GET.get('end', '')

    lekce = Lekce.objects.filter(start__gte=start, konec__lte=end)
    events = []

    for lek in lekce:
        rezervace_count = Rezervace.objects.filter(lekce=lek).count()
        events.append({
            'title': f'{lek.nazev} ({rezervace_count})',
            'start': lek.start.isoformat(),
            'end': lek.konec.isoformat(),
        })

    return JsonResponse(events, safe=False)
