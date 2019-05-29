from calendar import HTMLCalendar
from datetime import datetime, timedelta
from .models import *


class MyCalendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(MyCalendar, self).__init__()

    # formats a day as a td
    # filter events by day
    def formatday(self, day, events, user):
        events_per_day = events.filter(start__day=day, user_created=user)
        d = ''
        for event in events_per_day:
            d += f'<li> <a href="view/{event.id}">{event.title} <br> {event.start.time().strftime("%H:%M")} </a></li>'

        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    # formats a week as a tr
    def formatweek(self, theweek, events, user):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events, user)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self,user, withyear=True):
        events = Event.objects.filter(
            start__year=self.year, start__month=self.month, user_created=user )
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events, user)}\n'
        return cal
