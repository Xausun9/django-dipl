from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order
from .forms import OrderForm, UpdateOrderForm


@login_required
def create_order(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.full_name = request.user.full_name
            order.group = request.user.group
            order.save()
            return redirect("orders:create_order")
    else:
        form = OrderForm()
    return render(request, "orders/student.html", {"form": form, "orders": orders})


@login_required
def secretary_view(request):
    if not request.user.is_authenticated or request.user.role not in ["secretary", "admin"]:
        return redirect("redirect_by_role")

    orders = Order.objects.filter(status="in_anticipation")

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
