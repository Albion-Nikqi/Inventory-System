from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Product, StockMovement
from .forms import CategoryForm, ProductForm, StockMovementForm
from django.db.models import Q, ProtectedError
from django.core.paginator import Paginator
from django.contrib import messages
from django.db import transaction
from django.db.models import F


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'home.html', {'categories':categories})

def category_create(request):
    form = CategoryForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('home')

    return render(request, 'create_category.html', {'form':form})

def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = category.product_set.all()

    return render(request, 'category_detail.html', {'category':category, 'products':products})

def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)

    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect('home')

    return render(request, 'create_category.html', {'category':category, 'form':form})

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        category.delete()
        return redirect('home')

    return render(request, 'delete_category.html', {'category':category})    

def product_list(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')

    products = Product.objects.all()

    if query: 
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    if category_id:
        products = products.filter(category_id=category_id)    

    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(request, 'product_list.html', {'query':query, 'category_id':category_id, 'products':products, 'paginator':paginator,
                    'page_number':page_number, 'page_obj':page_obj, 'categories':categories})

def product_create(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    form = ProductForm(request.POST or None)

    if form.is_valid():
        product = form.save(commit=False)
        product.category = category
        product.save()
        return redirect('category_detail', pk=category_id)

    return render(request, 'create_product.html', {'form':form, 'category':category})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product_movements = product.stock_movements.all().order_by('-created_at')

    return render(request, 'product_detail.html', {'product':product, 'product_movements':product_movements})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk) 
    category_id = product.category.id

    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('category_detail', pk=category_id)

    return render(request, 'create_product.html', {'product':product, 'form':form, 'category':product.category})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    category_id = product.category.id


    if request.method == 'POST':
        try:
            product.delete()
            messages.success(request, 'Produkti u fshi me sukses!')
            return redirect('category_detail', pk=category_id)
        
        except ProtectedError:
            messages.error(request, "Nuk mund ta fshini këtë produkt sepse ka lëvizje stoku të regjistruara!")

    return render(request, 'delete_product.html', {'product':product, 'category_id':category_id}) 

def add_stock_movement(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = StockMovementForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        movement = form.save(commit=False)
        movement.product = product

        if movement.movement_type == 'OUT' and product.stock_quantity < movement.quantity:
            messages.error(request, f"Nuk ka stok të mjaftueshëm! Stoku aktual është {product.stock_quantity}.")
            return render(request, 'add_stock_movement.html', {'form':form, 'product':product})

        with transaction.atomic():
            if movement.movement_type == 'IN':
                product.stock_quantity += movement.quantity
            elif movement.movement_type == 'OUT':
                product.stock_quantity -= movement.quantity

            product.save()
            movement.save()
        messages.success(request, "Lëvizja e stokut u regjistrua me sukses!")
        return redirect('product_detail', pk=product.id)

    return render(request, 'add_stock_movement.html', {'product':product, 'form':form})

def dashboard(request):
    total_products = Product.objects.count()
    total_categories = Category.objects.count()

    out_of_stock = Product.objects.filter(stock_quantity=0)

    low_stock = Product.objects.filter(
        stock_quantity__lte=F('minimum_stock'),
        stock_quantity__gt=0
    )

    return render(request, 'dashboard.html', {'total_products':total_products, 'total_categories':total_categories, 'out_of_stock':out_of_stock,
                    'low_stock':low_stock})
