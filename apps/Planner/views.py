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
    else:
        return render(request, 'Planner/404.html')


def edit_profile(requset, id):
    if requset.session['logged']:
        user_id = int(id)
        user = User.objects.get(id=user_id)
        context = {
            "user": user
        }
        return render(requset, "Planner/edit_profile.html", context)


def editp(request, id):
    if request.session['logged']:
        if request.method == 'POST' and 'profileimage' in request.FILES:
            email = request.session['email']
            user = User.objects.get(email=email)
            bio = request.POST['bio']
            profile_pic = request.FILES['profileimage']
            profile = Profile.objects.create(
                bio=bio, image=profile_pic, user=user)
            return redirect("/success")
    else:
        return render(request, 'Planner/404.html')


def success(request):
    email = request.session['email']
    user = User.objects.get(email=email)
    try:
        profile = Profile.objects.get(user=user)
        posts = Post.objects.all()
        comments = Comment.objects.all()
        daily_events = Event.objects.all()
        context = {
            "user": user,
            'profile': profile,
            'posts': posts,
            'comments': comments,
            'events': daily_events
        }
    except:
        posts = Post.objects.all()
        comments = Comment.objects.all()
        context = {
            "user": user,
            'posts': posts,
            'comments': comments
        }
    return render(request, "Planner/wall.html", context)


def entry_form(request):
    return render(request, "Planner/entry.html")


class CalendarView(generic.ListView):
    model = Event
    template_name = 'Planner/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        email = self.request.session['email']
        user = User.objects.get(email=email)
        # use today's date for the calendar
        d = dt.today()

        # Instantiate our calendar class with today's year and date
        cal = MyCalendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(user, withyear=True)
        context['calendar'] = mark_safe(html_cal)
        return context


def view(request, id):
    if request.session['logged']:
        event_id = int(id)
        get_event = Event.objects.get(id=id)
        context = {
            "event": get_event
        }
        return render(request, "Planner/view.html", context)
    else:
        return render(request, 'Planner/404.html')


def edit_event(request, id):
    if request.session['logged']:
        event_id = int(id)
        get_event = Event.objects.get(id=id)
        title = request.POST['title']
        start = request.POST['start']
        end = request.POST['end']
        notes = request.POST['notes']
        errors = Event.objects.event_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            start_dt = dt.strptime(start, '%Y-%m-%dT%H:%M')
            end_dt = dt.strptime(end, '%Y-%m-%dT%H:%M')
            get_event.title = title
            get_event.start = start_dt
            get_event.end = end_dt
            get_event.notes = notes
            get_event.save()
            context = {
                "event": get_event
            }
            return redirect('/view/'+str(id))
    else:
        return render(request, 'Planner/404.html')


def delete(request, id):
    if request.session['logged']:
        event_id = int(id)
        get_event = Event.objects.get(id=id)
        get_event.delete()
        return redirect("/calendarall")
    else:
        return render(request, 'Planner/404.html')


def edit(request, id):
    if request.session['logged']:
        event_id = int(id)
        get_event = Event.objects.get(id=id)
        context = {
            "event": get_event
        }
        return render(request, "Planner/edit.html", context)
    else:
        return render(request, 'Planner/404.html')


def entry(request):
    if request.session['logged']:
        email = request.session['email']
        user_enter = User.objects.get(email=email)
        title = request.POST['title']
        start = request.POST['start']
        end = request.POST['end']
        start_dt = dt.strptime(start, '%Y-%m-%dT%H:%M')
        start_time = start_dt.time()
        end_dt = dt.strptime(end, '%Y-%m-%dT%H:%M')
        end_time = end_dt.time()
        notes = request.POST['notes']
        new_enrty = Event.objects.create(
            title=title,
            end=end_dt,
            start=start_dt,
            notes=notes,
            user_created=user_enter
        )
        return redirect('/success')
    else:
        return render(request, 'Planner/404.html')


def logout(request):
    if request.session['logged']:
        request.session['email'] = None
        request.session['logged'] = False
        return redirect("/")
    else:
        return render(request, 'Planner/404.html')


def write_post(request):
    if request.session['logged']:
        email = request.session['email']
        user_enter = User.objects.get(email=email)
        text = request.POST['userpost']
        post = Post.objects.create(
            text=text,
            user=user_enter
        )
        return redirect('/success')
    else:
        return render(request, 'Planner/404.html')


def write_comment(request, id):
    if request.session['logged']:
        email = request.session['email']
        user_enter = User.objects.get(email=email)
        text = request.POST['usercomment']
        post_id = int(id)
        post_commented = Post.objects.get(id=id)
        comment = Comment.objects.create(
            text=text, user_comment=user_enter, post_commented=post_commented)
        return redirect('/success')
    else:
        return render(request, 'Planner/404.html')


def delete_comment(request, id):
    if request.session['logged']:
        comment_id = int(id)
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
        return redirect('/success')
    else:
        return render(request, 'Planner/404.html')


def delete_post(request, id):
    if request.session['logged']:
        post_id = int(id)
        post = Post.objects.get(id=post_id)
        post.delete()
        return redirect('/success')
    else:
        return render(request, 'Planner/404.html')


def view_profile(request, id):
    if request.session['logged']:
        user_id = int(id)
        user_view = User.objects.get(id=user_id)
        context = {
            'user': user_view,
        }
        return render(request, 'Planner/view_profile.html', context)
    else:
        return render(request, 'Planner/404.html')
