from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib import messages
from django.http import HttpResponse
import bcrypt
from .myCalendar import *
from datetime import datetime as dt
from .myCalendar import *
from .models import *
from django.views import generic
from django.utils.safestring import mark_safe


def index(request):
    return render(request, 'Planner/index.html')


def register(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        month_start = request.POST['month_start']
        year_start = request.POST['year_start']
        errors = User.objects.new_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            hash_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            print(hash_pw.decode())
            new_user = User.objects.create(
                fname=fname,
                lname=lname,
                email=email,
                start_month=month_start,
                start_year=year_start,
                password=hash_pw.decode()
            )
            request.session['email'] = email
            request.session['logged'] = True
            return redirect('/success')


def login(request):
    if request.method == 'POST':
        email = request.POST['lemail']
        password = request.POST['lpassword']
        errors = User.objects.log_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            request.session['email'] = email
            request.session['logged'] = True
            return redirect('/success')


def success(request):
    return render(request, "Planner/blank.html")

def entry_form(request):
    return render(request, "Planner/entry.html")

class CalendarView(generic.ListView):
    model = Event
    template_name = 'Planner/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = dt.today()

        # Instantiate our calendar class with today's year and date
        cal = MyCalendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        return context


def entry(request):
    if request.session['logged']:
        email=request.session['email']
        user_enter = User.objects.get(email=email)
        title = request.POST['title']
        start = request.POST['start']
        end = request.POST['end']
        start_dt = dt.strptime(start, '%Y-%m-%dT%H:%M')
        start_time = start_dt.time()
        end_dt = dt.strptime(end, '%Y-%m-%dT%H:%M')
        end_time= end_dt.time()
        notes = request.POST['notes']
        new_enrty = Event.objects.create(
            title=title,
            end=end_dt,
            start=start_dt,
            notes=notes,
            user_created = user_enter
        )
        return redirect('/success')
