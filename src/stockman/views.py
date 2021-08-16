from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

from .models import *
from .forms import (StockCreateForm, StockSearchForm, StockUpdateForm, ReceiveItemForm, IssueItemForm)

import csv


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
    header = "List of items"
    queryset = Stock.objects.all()
    form = StockSearchForm(request.POST or None)

    context = {
        "header": header,
        "queryset": queryset,
        "form": form
    }

    if request.method == 'POST':
        queryset = Stock.objects.filter(  # category__icontains=form['category'].value(),
            item_name__icontains=form['item_name'].value())
        if form['export_to_CSV'].value():
            response = HttpResponse(content_type='text/csv')
            response['content-Disposition'] = 'attachment; filename="List of stock.csv"'
            writer = csv.writer(response)
            writer.writerow(['CATEGORY', 'ITEM NAME', 'QUANTITY'])
            instance = queryset
            for stock in instance:
                writer.writerow([stock.category, stock.item_name, stock.quantity])
            return response

        context = {
            "form": form,
            "header": header,
            "queryset": queryset,
        }

    return render(request, "list-item.html", context)


def add_items(request):
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully Saved')
        return redirect('/list_items')
    context = {
        "form": form,
        "title": "Add Item",
    }
    return render(request, "add_items.html", context)


def update_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = StockUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully Updated')
            return redirect('/list_items')

    context = {
        'form': form
    }
    return render(request, 'add_items.html', context)


def delete_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, 'Successfully Deleted')
        return redirect('/list_items')
    return render(request, 'delete_items.html')


def stock_detail(request, pk):
    queryset = Stock.objects.get(id=pk)
    context = {
        "title": queryset.item_name,
        "queryset": queryset,
    }
    return render(request, "stock_detail.html", context)


def issue_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = IssueItemForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.quantity -= instance.issue_quantity
        # instance.issue_by = str(request.user)
        messages.success(request, "Issued SUCCESSFULLY. " + str(instance.quantity) + " " + str(
            instance.item_name) + "s now left in Store")
        instance.save()

        return redirect('/item_detail/' + str(instance.id))
    context = {
        "title": "Issued " + str(queryset.item_name),
        "queryset": queryset,
        "form": form,
        "username": "Issued By: " + str(request.user),
    }
    return render(request, "add_items.html", context)


def receive_item(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReceiveItemForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.quantity += instance.receive_quantity
        instance.save()
        messages.success(request, "Received SUCCESSFULLY. " + str(instance.quantity) + " " + str(
            instance.item_name) + "s now in Store")
        return redirect('/item_detail/' + str(instance.id))
    context = {
        "title": "Received " + str(queryset.item_name),
        "instance": queryset,
        "form": form,
        "username": "Received By: " + str(request.user)
    }
    return render(request, "add_items.html", context)
