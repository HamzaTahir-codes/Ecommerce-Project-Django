from django.shortcuts import render, redirect
from core.models import CartOrder, Product, Category
from django.db.models import Sum
from userauths.models import User
from .forms import AddProductForm
import datetime
# Create your views here.

def dashboard(request):
    revenue = CartOrder.objects.aggregate(price=Sum("price"))
    total_orders_count = CartOrder.objects.all()
    all_products = Product.objects.all()
    all_categories = Category.objects.all()
    new_customers = User.objects.all().order_by("-id")
    latest_orders = CartOrder.objects.all().order_by("-id")

    this_month = datetime.datetime.now().month

    monthly_revenue = CartOrder.objects.filter(order_date__month=this_month).aggregate(price=Sum("price"))

    context = {
        'revenue': revenue,
        'total_orders_count': total_orders_count,
        'all_products': all_products,
        'all_categories': all_categories,
        'new_customers': new_customers,
        'latest_orders': latest_orders,
        'monthly_revenue': monthly_revenue,
    }

    return render(request, "useradmin/dashboard.html", context)


def products(request):
    all_products = Product.objects.all().order_by("-id")
    all_categories = Category.objects.all()

    context = {
        'all_products': all_products,
        'all_categories': all_categories,
    }

    return render(request, "useradmin/products.html", context)

def add_product(request):
    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                new_form = form.save(commit=False)
                new_form.user = request.user
                new_form.save()
                return redirect("useradmin:products")
            except ValueError as e:
                print("Form save error:", e)
                print("Form errors:", form.errors)
                # Optionally, add a message to the context to display to the user
        else:
            print("Form is not valid:", form.errors)
    else:
        form = AddProductForm()

    context = {
        'form': form
    }

    return render(request, "useradmin/add-product.html", context)

def edit_product(request, pid):
    product = Product.objects.get(pid=pid)
    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            return redirect("useradmin:edit-product", product.pid)
    else:
        form = AddProductForm(instance=product)

    context = {
        'form': form,
        'product' : product,
    }

    return render(request, "useradmin/edit-product.html", context)

def delete_product(request,pid):
    product = Product.objects.get(pid=pid)
    product.delete()
    return redirect("useradmin:products")