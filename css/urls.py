"""css URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from . import views, scheduling


urlpatterns = [
    # BASE_URL/Home* addresses
    url(r'^$', views.IndexView, name='index'),
    url(r'^home/$', views.HomeView, name='home'),
    url(r'^resources/', include([
        url(r'^faculty/$', views.FacultyView, name='faculty'),
        url(r'^rooms/$', views.RoomsView, name='rooms'),
        url(r'^courses/$', views.CoursesView, name='courses'),
    ])),
    url(r'^scheduling/', include([
        url(r'^$', views.SchedulingView, name='scheduling'),
        url(r'^options$', scheduling.Options, name='options'), 
        url(r'^schedules$', scheduling.Schedules, name='schedules'),
        url(r'^sections$', scheduling.Sections, name='sections'),
        url(r'^newSection$', scheduling.NewSection, name='newSection')
    ])),
    url(r'^department/', include([
        url(r'^schedulers/$', views.SchedulersView, name='schedulers'),
        url(r'^settings/$', views.SettingsView, name='settings'), 
    ])),
    url(r'^register/$', views.RegistrationView, name='register'),
    url(r'^faq/$', views.FAQView, name='faq'),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.LoginView, name='login'),
    url(r'^loginhelp/$', views.LoginView, name='loginhelp'),
    url(r'^landing/$', views.LandingView, name='landing'),
    url(r'^logout/$', views.LogoutView, name='logout'),
    url(r'^availability/$', views.AvailabilityView, name='availability')

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

