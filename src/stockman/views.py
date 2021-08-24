from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *

import csv


# Create your views here.
def home(request):
    title = "Welcome to the home page"
    form = "Welcome to the home page"
    context = {
        "title": title,
        "test": form,
    }
    return render(request, "home.html", context)


@login_required
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


@login_required
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


@login_required
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


@login_required
def delete_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, 'Successfully Deleted')
        return redirect('/list_items')
    return render(request, 'delete_items.html')


@login_required
def stock_detail(request, pk):
    queryset = Stock.objects.get(id=pk)
    context = {
        "title": queryset.item_name,
        "queryset": queryset,
    }
    return render(request, "stock_detail.html", context)


@login_required
def issue_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = IssueItemForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.receive_quantity = 0
        instance.quantity -= instance.issued_quantity
        instance.issued_by = str(request.user)
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


@login_required
def receive_item(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReceiveItemForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.issued_quantity = 0
        instance.quantity += instance.receive_quantity
        instance.receive_by = str(request.user)
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


@login_required
def reorder_level(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReorderLevelForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Reorder level for " + str(instance.item_name) + " is updated to " + str(
            instance.reorder_level))
        return redirect('/list_items')

    context = {
        "instance": queryset,
        'form': form
    }
    return render(request, 'add_items.html', context)


@login_required
def list_history(request):
    header = 'HISTORY'
    queryset = StockHistory.objects.all()
    form = StockSearchForm(request.POST or None)
    context = {
        "header": header,
        "queryset": queryset,
        "form": form,
    }
    if request.method == 'POST':
        category = form['category'].value()
        queryset = StockHistory.objects.filter(
            item_name__icontains=form['item_name'].value()
        )
        if category != '':
            queryset = queryset.filter(category_id=category)
        context = {
            'form': form,
            'header': header,
            'queryset': queryset,
        }
        if form['export_to_CSV'].value():
            response = HttpResponse(content_type='text/csv')
            response['content-Disposition'] = 'attachment; filename="Stock History.csv"'
            writer = csv.writer(response)
            writer.writerow(
                ['CATEGORY',
                 'ITEM NAME',
                 'QUANTITY',
                 'ISSUED QUANTITY',
                 'RECEIVE QUANTITY',
                 'RECEIVE BY',
                 'ISSUE BY',
                 'LAST UPDATED'])
            instance = queryset
            for stock in instance:
                writer.writerow(
                    [stock.category,
                     stock.item_name,
                     stock.quantity,
                     stock.issued_quantity,
                     stock.receive_quantity,
                     stock.receive_by,
                     stock.issued_by,
                     stock.last_updated])
            return response
    return render(request, "list_history.html", context)
