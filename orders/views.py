from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import MenuItem, Order, OfficerProfile
from .forms import OfficerSignUpForm, OfficeUpdateForm


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('officer_dashboard')
    if request.method == 'POST':
        form = OfficerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('officer_dashboard')
    else:
        form = OfficerSignUpForm()
    return render(request, 'orders/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_dashboard')
        return redirect('officer_dashboard')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')
            return redirect('officer_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'orders/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')



@login_required
def officer_dashboard(request):
    try:
        officer_profile = request.user.officerprofile
    except OfficerProfile.DoesNotExist:
        return redirect('admin_dashboard')

    menu_items = MenuItem.objects.filter(is_available=True)
    my_orders = Order.objects.filter(officer=officer_profile).order_by('-created_at')
    
    if request.method == 'POST':
        if 'update_office' in request.POST:
            office_form = OfficeUpdateForm(request.POST, instance=officer_profile)
            if office_form.is_valid():
                office_form.save()
                return redirect('officer_dashboard')
        
        elif 'place_order' in request.POST:
            selected_item_ids = request.POST.getlist('items')
            if selected_item_ids:
                order = Order.objects.create(officer=officer_profile)
                order.items.set(selected_item_ids)
                order.save()
                return redirect('officer_dashboard')
    else:
        office_form = OfficeUpdateForm(instance=officer_profile)

    context = {
        'profile': officer_profile,
        'menu_breakfast': menu_items.filter(category='BREAKFAST'),
        'menu_lunch': menu_items.filter(category='LUNCH'),
        'menu_dinner': menu_items.filter(category='DINNER'),
        'menu_drinks': menu_items.filter(category='DRINK'),
        'my_orders': my_orders,
        'office_form': office_form,
        'mess_contact': '0716342355'
    }
    return render(request, 'orders/officer_dashboard.html', context)

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, officer=request.user.officerprofile)
    if order.status == 'PENDING':
        order.status = 'CANCELLED'
        order.save()
    return redirect('officer_dashboard')



@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    pending_orders = Order.objects.filter(status='PENDING').order_by('-created_at')
    all_orders = Order.objects.all().order_by('-created_at')
    menu_items = MenuItem.objects.all().order_by('category', 'name')
    
    if request.method == 'POST':
        if 'add_item' in request.POST:
            name = request.POST.get('name')
            category = request.POST.get('category')
            price = request.POST.get('price') # <-- Catching the new price field value input
            if name and category and price:
                MenuItem.objects.create(name=name, category=category, price=price)
            return redirect('admin_dashboard')
            
    return render(request, 'orders/admin_dashboard.html', {
        'pending_orders': pending_orders,
        'all_orders': all_orders,
        'menu_items': menu_items
    })

@user_passes_test(lambda u: u.is_superuser)
def accept_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 'ACCEPTED'
    order.save()
    return redirect('admin_dashboard')

@user_passes_test(lambda u: u.is_superuser)
def toggle_menu_item(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    item.is_available = not item.is_available
    item.save()
    return redirect('admin_dashboard')