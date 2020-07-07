from django.shortcuts import render
from django.views import View


class CalendarView(View):

    def get(self, request):
        context = {
            'hola': "hola"
        }
        return render(request, 'calendar.html', context)
