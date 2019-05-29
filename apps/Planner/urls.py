from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^success$', views.success),
    url(r'^register$', views.register),
    url(r'^entry$', views.entry),
    url(r'^form_entry', views.entry_form),
    url(r'^login$', views.login),
    url(r'^calendarall', views.CalendarView.as_view(), name='calendar'),
    url(r'^view/(?P<id>\d+)$', views.view),
    url(r'^edit/(?P<id>\d+)$', views.edit),
    url(r'edit_event/(?P<id>\d+)', views.edit_event),
    url(r'delete/(?P<id>\d+)', views.delete),
    url(r'edit_profile/(?P<id>\d+)$', views.edit_profile),
    url(r'^editp/(?P<id>\d+)$', views.editp),
    url(r'^logout$', views.logout),
    url(r'^user_post$', views.write_post),
    url(r'user_comment/(?P<id>\d+)$', views.write_comment),
    url(r'delete_comment/(?P<id>\d+)$', views.delete_comment),
    url(r'delete_post/(?P<id>\d+)$', views.delete_post),
    url(r'view_profile/(?P<id>\d+)$', views.view_profile)
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)