from django import forms
from django.contrib import messages

from .models import *


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

    def clean_category_name(self):
        categories = self.cleaned_data.get('name')
        for instance in categories:
            if instance.name == name:
                raise forms.ValidationError(str(category) + " is already created")
            return name


class StockCreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'quantity', 'date']

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise forms.ValidationError('This Field is required')
        return category

    def clean_item_name(self):
        item_name = self.cleaned_data.get('item_name')
        if not item_name:
            raise forms.ValidationError('This Field is required')
        return item_name


class StockHistorySearchForm(forms.ModelForm):
    export_to_CSV = forms.BooleanField(required=False)
    start_date = forms.DateTimeField(required=False)
    end_date = forms.DateTimeField(required=False)

    class Meta:
        model = StockHistory
        fields = ['category', 'item_name', 'start_date', 'end_date']


class StockSearchForm(forms.ModelForm):
    export_to_CSV = forms.BooleanField(required=False)

    class Meta:
        model = Stock
        fields = ['category', 'item_name']


class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'quantity']


class IssueItemForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['issued_quantity', 'issued_to']


class ReceiveItemForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['receive_quantity'] #, 'receive_by'


class ReorderLevelForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['reorder_level']
