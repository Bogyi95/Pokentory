from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Product, Order, Category
from .forms import ProductForm, OrderForm
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.

@login_required
def index(request):
    orders = Order.objects.all()
    products = Product.objects.all()
    orders_count = orders.count()
    product_count = products.count()
    workers_count = User.objects.all().count()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.staff = request.user
            instance.save()
            return redirect('dashboard-index')
    else:
        form = OrderForm()
    context = {
        'orders': orders,
        'form': form,
        'products': products,
        'workers_count': workers_count,
        'product_count': product_count,
        'orders_count': orders_count,
    }
    return render(request, 'dashboard/index.html', context)


@login_required
def staff(request):
    workers = User.objects.all()
    workers_count = workers.count()
    orders_count = Order.objects.all().count()
    product_count = Product.objects.all().count()
    context = {
        'workers': workers,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'product_count': product_count,
    }
    return render(request, 'dashboard/staff.html', context)


@login_required
def staff_detail(request, pk):
    workers = User.objects.get(id=pk)
    context = {
        'workers': workers,
    }
    return render(request, 'dashboard/staff_detail.html', context)


@login_required
def product(request):
    items = Product.objects.all()  # Using ORM
    product_count = items.count()
    # items = Product.objects.raw('SELECT * FROM dashboard_product')
    workers_count = User.objects.all().count()
    orders_count = Order.objects.all().count()

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            product_name = form.cleaned_data.get('name')
            messages.success(request, f'{product_name} has been added')
            return redirect('dashboard-product')
    else:
        form = ProductForm()

    context = {
        'items': items,
        'form': form,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'product_count': product_count,
    }
    return render(request, 'dashboard/product.html', context)

@login_required
def product_user(request):
    items = Product.objects.all()
    categories = Category.objects.all()

    selected_category = request.GET.get('category')
    if selected_category:
        items = items.filter(category__name=selected_category)

    context = {
        'items': items,
        'categories' : categories,
        'selected_category': selected_category,
    }
    return render(request, 'dashboard/product_user.html', context)


@login_required
def product_delete(request, pk):
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('dashboard-product')
    return render(request, 'dashboard/product_delete.html')


@login_required
def product_update(request, pk):
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('dashboard-product')
    else:
        form = ProductForm(instance=item)
    context = {
        'form': form,
    }
    return render(request, 'dashboard/product_update.html', context)


@login_required
def order(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        order_quantity = request.POST.get('order_quantity')
        product = Product.objects.get(pk=product_id)
        order = Order.objects.create(
            product=product,
            order_quantity=order_quantity,
            staff=request.user,
        )
        order_category_names = product.category.all().values_list('name', flat=True)
        order.category.set(Category.objects.filter(name__in=order_category_names))
        product.quantity -= int(order_quantity)
        product.save()
        return redirect('dashboard-index')

    return render(request, 'order/.html', {'orders': Order.objects.all()})

def buy_request(request, pk):
    item = Product.objects.get(id=pk)
    items = Product.objects.all()
    categories = Category.objects.all()
    print("You want to buy : ", item)
    selected_category = request.GET.get('category')
    if selected_category:
        items = items.filter(category__name=selected_category)
    
    context= {
        'item':item,
        'items':items,
        'categories':categories,
    }
    return render(request, "user/buy_request.html", context)
