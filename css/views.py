from django.template import Context, Template
from django.shortcuts import render
from django.views.generic import TemplateView

# ---- Template classes ----
# Template class for the home view
#class HomeView(TemplateView):
#    template_name = "home.html"

# ---- Other views ----
def HomeView(request):
    return render(request, 'home.html');

def IndexView(request):
    return render(request, 'index.html');

def InviteForm(request):
    return render(request, 'invite.html');

