from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from datetime import timedelta, datetime
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
    model = Osoba
    template_name ='osoba/list_detail.html'


    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         osoba = self.get_object()
         lekce = osoba.rezervace_set.all()
         context['lekce'] = lekce
         return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        osoba = self.get_object()
        rezervace = osoba.rezervace_set.all()
        context['rezervace'] = rezervace
        return context



def calendar_view(request):
    return render(request, 'calendar.html')

from django.urls import reverse

def get_events(request):
    date_str = request.GET.get('date')

    if date_str:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        start = date.replace(hour=0, minute=0, second=0)
        end = start + timedelta(days=1)

        lekce = Lekce.objects.filter(start__gte=start, konec__lt=end)
        events = []

        for lek in lekce:
            rezervace_count = Rezervace.objects.filter(lekce=lek).count()
            event_url = reverse('detail_lekce', args=[lek.id])
            room_name = lek.mistnost.jmeno
            trainer_name = lek.cvicitel.jmeno
            trainer_surname = lek.cvicitel.prijmeni
            events.append({
                'title': lek.nazev,
                'start_time': lek.start.strftime('%H:%M'),
                'end_time': lek.konec.strftime('%H:%M'),
                'count': rezervace_count,
                'url': event_url,
                'room': room_name,
                'trainer': trainer_name,
                'trainer_sur': trainer_surname
            })

        return JsonResponse(events, safe=False)
    else:
        return JsonResponse({'error': 'Missing date parameter'}, status=400)


