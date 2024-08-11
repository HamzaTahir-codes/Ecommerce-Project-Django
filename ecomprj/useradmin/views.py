from django.shortcuts import render, redirect
from core.models import CartOrder, Product, Category, CartOrderItems, ProductReview
from userauths.models import Profile
from django.db.models import Sum
from userauths.models import User
from .forms import AddProductForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login, authenticate, logout
from .decorators import admin_required
import datetime
# Create your views here.

@admin_required
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

@admin_required
def products(request):
    all_products = Product.objects.all().order_by("-id")
    all_categories = Category.objects.all()

    context = {
        'all_products': all_products,
        'all_categories': all_categories,
    }

    return render(request, "useradmin/products.html", context)

@admin_required
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

@admin_required
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

@admin_required
def delete_product(request,pid):
    product = Product.objects.get(pid=pid)
    product.delete()
    return redirect("useradmin:products")

@admin_required
def orders_list(request):
    orders = CartOrder.objects.all()
    context = {
        "orders" : orders
    }
    return render(request, "useradmin/orders-list.html", context)

@admin_required
def orders_detail(request, oid):
    order = CartOrder.objects.get(oid=oid)
    order_items = CartOrderItems.objects.filter(order = order)

    context = {
        "order" : order,
        "order_items" : order_items
    }
    return render(request, "useradmin/order_detail.html", context)

@admin_required
@csrf_exempt
def change_product_status(request, oid):
    order = CartOrder.objects.get(oid=oid)
    if request.method == "POST":
        status = request.POST.get("status")
        print("Status  ========= >> ", status)
        order.product_status = status
        order.save()
        messages.success(request, f"Status changed to {status}")
    
    return redirect("useradmin:order-detail", order.oid)

@admin_required
def shop_page(request):
    products = Product.objects.all()
    revenue = CartOrder.objects.aggregate(price=Sum("price"))
    total_sales = CartOrderItems.objects.filter(order__paid_status = True).aggregate(qty=Sum("qty"))

    context = {
        "products" : products,
        "revenue" : revenue,
        "total_sales" : total_sales
    }

    return render(request, "useradmin/shop-page.html", context)

@admin_required
def reviews(request):
    reviews = ProductReview.objects.all()
    context = {
        "reviews" : reviews,
    }
    return render(request, "useradmin/reviews.html", context)

@admin_required
def settings(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        image = request.FILES.get("image")
        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        bio = request.POST.get("bio")
        address = request.POST.get("address")
        country = request.POST.get("country")

        if image != None:
            profile.image = image

        profile.full_name = full_name
        profile.phone = phone
        profile.bio = bio
        profile.address = address
        profile.country = country

        profile.save()
        messages.success(request, "Profile Successfully Updated!")
        return redirect("useradmin:settings")
    
    context = {
        "profile" : profile
    }

    return render(request, "useradmin/settings.html", context)


@admin_required
def change_password(request):
    user = request.user

    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "Password Miss-Matched!!")
            return redirect("useradmin:change-password")
        
        if check_password(old_password, user.password):
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password Changed Successfully")
            return redirect("useradmin:login")
        else:
            messages.error(request, "Old Password is not correct")
            return redirect("useradmin:change-password")
    return render(request, "useradmin/change-password.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("useradmin:vendor-dashboard")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email = email)
            
            user = authenticate(request, email = email, password = password)

            if user is not None:
                login(request, user)
                messages.success(request, "You are successfully logged In!")
                return redirect("useradmin:vendor-dashboard")
            else:
                messages.error(request, "User doesn't exist, Please Sign-Up")

        except:
            messages.error(request, f"User with {email} doesn't exist")

    return render(request, "useradmin/login.html")

def logout_view(request):
    logout(request)
    messages.success(request,"Logged Out Successfully!")
    return redirect("useradmin:login")