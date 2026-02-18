

# Create your views here.
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from .forms import *
from django.contrib import messages


from django.db.models import Sum, F, DecimalField
from django.db.models.functions import Coalesce
def add_purchase(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            purchase = form.save(commit=False)

            feed = purchase.feed

            # 🔹 UPDATE STOCK
            feed.quantity += purchase.quantity

            # 🔹 UPDATE PURCHASE PRICE (IMPORTANT)
            feed.purchase_price = purchase.rate

            feed.save()
            purchase.save()

            return redirect('dashboard')
    else:
        form = PurchaseForm()

    return render(request, 'inventory/purchase.html', {'form': form})


from django.utils.timezone import now
from datetime import timedelta


def dashboard(request):
    feeds = Feed.objects.all()

    total_feeds = feeds.count()
    total_stock = sum(feed.quantity for feed in feeds)

    # Low stock (less than 10)
    low_stock_feeds = feeds.filter(quantity__lt=10)
    total_due = Customer.objects.filter(balance__gt=0).count()

    # Expiring in next 15 days
    today = now().date()
    expiry_limit = today + timedelta(days=15)
    expiring_feeds = feeds.filter(expiry_date__lte=expiry_limit, expiry_date__gte=today)

    context = {
        'feeds': feeds,
        'total_feeds': total_feeds,
        'total_stock': total_stock,
        'low_stock_feeds': low_stock_feeds,
        'expiring_feeds': expiring_feeds,
    }

    return render(request, 'inventory/dashboard.html', context)
from .forms import SaleForm
def add_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)

            feed = sale.feed

            # stock reduce
            feed.quantity -= sale.quantity
            feed.save()

            # customer balance
            balance = sale.total_amount - sale.paid_amount
            sale.customer.balance += balance
            sale.customer.save()

            sale.save()
            return redirect('dashboard')
    else:
        form = SaleForm()

    return render(request, 'inventory/sales.html', {'form': form})

from decimal import Decimal

def add_payment(request):
    if request.method == 'POST':
        customer_id = request.POST['customer']
        amount = Decimal(request.POST['amount'])

        customer = Customer.objects.get(id=customer_id)
        customer.balance -= amount
        customer.save()
from django.http import JsonResponse
from .models import Feed

def get_feed_rate(request):
    feed_id = request.GET.get('feed_id')

    if not feed_id:
        return JsonResponse({'price': 0})

    feed = Feed.objects.get(id=feed_id)

    return JsonResponse({
        'price': str(feed.selling_price)   # ✅ CORRECT FIELD
    })
def balance_sheet(request):

    total_purchase = Purchase.objects.aggregate(
        total=Coalesce(
            Sum('total_amount'),
            0,
            output_field=DecimalField(max_digits=10, decimal_places=2)
        )
    )['total']

    total_sales = Sale.objects.aggregate(
        total=Coalesce(
            Sum('total_amount'),
            0,
            output_field=DecimalField(max_digits=10, decimal_places=2)
        )
    )['total']

    profit = total_sales - total_purchase

    total_due = Customer.objects.aggregate(
        total=Coalesce(
            Sum('balance'),
            0,
            output_field=DecimalField(max_digits=10, decimal_places=2)
        )
    )['total']

    context = {
        'total_purchase': total_purchase,
        'total_sales': total_sales,
        'profit': profit,
        'total_due': total_due,
    }

    return render(request, 'inventory/balance_sheet.html', context)

def sales_report(request):
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')

    sales = Sale.objects.all()

    if start_date and end_date:
        sales = sales.filter(date__range=[start_date, end_date])

    total_amount = sales.aggregate(total=Sum('total_amount'))['total'] or 0

    return render(request, 'inventory/sales_report.html', {
        'sales': sales,
        'total_amount': total_amount
    })


def purchase_report(request):
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')

    purchases = Purchase.objects.all()

    if start_date and end_date:
        purchases = purchases.filter(date__range=[start_date, end_date])

    total_amount = purchases.aggregate(total=Sum('total_amount'))['total'] or 0

    return render(request, 'inventory/purchase_report.html', {
        'purchases': purchases,
        'total_amount': total_amount
    })
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

@login_required
def customer_report(request):

    customers = Customer.objects.all()

    selected_customer = None
    sales = None
    total_sales = 0
    total_paid = 0
    balance = 0

    customer_id = request.GET.get('customer')
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')

    if customer_id:
        selected_customer = Customer.objects.get(id=customer_id)

        sales = Sale.objects.filter(customer=selected_customer)

        if start_date and end_date:
            sales = sales.filter(date__range=[start_date, end_date])

        total_sales = sales.aggregate(
            total=Sum('total_amount')
        )['total'] or 0

        total_paid = sales.aggregate(
            paid=Sum('paid_amount')
        )['paid'] or 0

        balance = total_sales - total_paid

    context = {
        'customers': customers,
        'selected_customer': selected_customer,
        'sales': sales,
        'total_sales': total_sales,
        'total_paid': total_paid,
        'balance': balance
    }

    return render(request, 'inventory/customer_report.html', context)
@login_required
def add_feed(request):
    if request.method == "POST":
        form = FeedForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_feed')
    else:
        form = FeedForm()

    return render(request, 'inventory/add_feed.html', {'form': form})

@login_required
def feed_list(request):
    feeds = Feed.objects.all().order_by('-id')
    return render(request, 'feed_list.html', {'feeds': feeds})

@login_required
def update_feed(request, pk):
    feed = get_object_or_404(Feed, pk=pk)

    if request.method == 'POST':
        form = FeedForm(request.POST, instance=feed)
        if form.is_valid():
            form.save()
            return redirect('feed_list')
    else:
        form = FeedForm(instance=feed)

    return render(request, 'inventory/add_feed.html', {'form': form})
@login_required
def delete_feed(request, pk):
    feed = get_object_or_404(Feed, pk=pk)

    if request.method == 'POST':
        feed.delete()
        return redirect('feed_list')

    return render(request, 'inventory/delete_feed.html', {'feed': feed})

@login_required
def admin_dashboard(request):
    return render(request, 'inventory/admin_dashboard.html')

@login_required
def add_customer(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()

    return render(request, 'add_customer.html', {'form': form})
@login_required
def customer_list(request):
    customers = Customer.objects.all().order_by('-id')
    return render(request, 'inventory/customer_list.html', {'customers': customers})

@login_required
def update_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'inventory/add_customer.html', {'form': form})
@login_required
def delete_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == "POST":
        customer.delete()
        return redirect('customer_list')

    return render(request, 'inventory/delete_customer.html', {'customer': customer})
