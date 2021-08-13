from django.shortcuts import render

from .models import *


# Create your views here.
def home(request):
    title = "Welcome to the home page"
    form = "Welcome to the home page"
    context = {
        "title": title,
        "test": form
    }
    return render(request, "home.html", context)


def list_items(request):
    title = "List of items"
    queryset = Stock.objects.all()
    context = {
        "title": title,
        "queryset": queryset,
    }
    return render(request, "list-item.html", context)
