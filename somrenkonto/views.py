from django.shortcuts import render
from django.views import View

from schedule.models import Calendar


class CalendarView(View):

    def get(self, request):
        try:
            ing_calendar = Calendar.objects.get_calendar_for_object(request.user)
        except Calendar.DoesNotExist:
            ing_calendar = 'failed'

        context = {
            'calendar': ing_calendar
        }
        return render(request, 'calendar.html', context)
