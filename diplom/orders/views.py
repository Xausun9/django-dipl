from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order
from .forms import OrderForm, UpdateOrderForm


@login_required
def index(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "orders/index.html", {"orders": orders})


@login_required
def create_order(request):
    orders = Order.objects.filter(user=request.user)
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            return redirect("orders:index")
    else:
        form = OrderForm()
    return render(request, "orders/student.html", {"form": form, "orders": orders})


@login_required
def secretary_view(request):
    if not request.user.is_staff:
        return redirect("orders:index")

    orders = Order.objects.filter(status="В ожидании")

    if request.method == "POST":
        order_id = request.POST.get("order_id")
        order = get_object_or_404(Order, id=order_id)
        form = UpdateOrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect("orders:secretary")
    else:
        form = UpdateOrderForm()

    return render(request, "orders/secretary.html", {"orders": orders, "form": form})
