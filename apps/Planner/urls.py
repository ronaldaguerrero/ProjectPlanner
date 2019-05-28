from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^success$', views.success),
    url(r'^register$', views.register),
    url(r'^entry$', views.entry),
    url(r'^form_entry', views.entry_form),
    url(r'^login$', views.login),
    url(r'^calendar', views.CalendarView.as_view(), name='calendar'),
]