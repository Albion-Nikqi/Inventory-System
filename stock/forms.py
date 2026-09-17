from django import forms
from .models import Category, Product, StockMovement

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'price', 'stock_quantity', 'minimum_stock']

class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['movement_type', 'quantity', 'note']

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity is not None and quantity <= 0:
            raise forms.ValidationError("Sasia e lëvizjes duhet të jetë më e madhe se zero.")
        return quantity