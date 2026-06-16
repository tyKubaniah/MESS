from decimal import Decimal, InvalidOperation
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout  # Make sure logout is imported here!
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import user_passes_test
from .models import Order, MenuItem

# --- ADD THIS LOGOUT VIEW FUNCTION ---
def logout_view(request):
    """Logs out the user or superuser and safely flushes their active session."""
    logout(request)
    return redirect('login')  # Redirects straight to your login page URL route


# --- YOUR EXISTING WORKING VIEWS (Keep these exactly as they are) ---
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('admin_dashboard' if user.is_superuser else 'officer_dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('admin_dashboard' if user.is_superuser else 'officer_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    pending_orders = Order.objects.filter(status='PENDING').order_by('-created_at')
    all_orders = Order.objects.all().order_by('-created_at')
    menu_items = MenuItem.objects.all().order_by('category', 'name')
    
    if request.method == 'POST':
        if 'add_item' in request.POST:
            name = request.POST.get('name')
            category = request.POST.get('category')
            price = request.POST.get('price')
            if name and category and price:
                MenuItem.objects.create(name=name, category=category, price=price)
            return redirect('admin_dashboard')
        
        elif 'update_item' in request.POST:
            item_id = request.POST.get('item_id')
            item = get_object_or_404(MenuItem, id=item_id)
            
            edit_name = request.POST.get(f'edit_name_{item_id}')
            edit_price = request.POST.get(f'edit_price_{item_id}')
            edit_category = request.POST.get(f'edit_category_{item_id}')
            
            if edit_name: item.name = edit_name
            if edit_category: item.category = edit_category
            if edit_price:
                try:
                    clean_price = str(edit_price).replace('KSh', '').strip()
                    item.price = Decimal(clean_price)
                except (InvalidOperation, ValueError):
                    pass
            item.save()
            return redirect('admin_dashboard')

    context = {
        'pending_orders': pending_orders,
        'all_orders': all_orders,
        'menu_items': menu_items,
    }
    return render(request, 'admin_dashboard.html', context)


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