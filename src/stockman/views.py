from django.shortcuts import render

from .models import *
from .forms import StockCreateForm


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


def add_items(request):
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {
        "form": form,
        "title": "Add Item",
    }
    return render(request, "add_items.html", context)
