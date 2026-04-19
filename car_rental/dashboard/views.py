from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from cars.models import Car, Category
from bookings.models import Booking
from .forms import CarAdminForm

def is_staff(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

staff_required = user_passes_test(is_staff, login_url='/accounts/login/')

@login_required
@staff_required
def dashboard(request):
    from django.db.models import Sum
    context = {
        'total_cars': Car.objects.count(),
        'available_cars': Car.objects.filter(is_available=True).count(),
        'total_bookings': Booking.objects.count(),
        'pending_bookings': Booking.objects.filter(status='pending').count(),
        'total_revenue': Booking.objects.exclude(status='cancelled').aggregate(s=Sum('total_price'))['s'] or 0,
        'total_users': User.objects.count(),
        'recent_bookings': Booking.objects.select_related('user', 'car').order_by('-created_at')[:8],
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
@staff_required
def admin_cars(request):
    cars = Car.objects.select_related('category').all()
    return render(request, 'dashboard/admin_cars.html', {'cars': cars})

@login_required
@staff_required
def admin_car_add(request):
    if request.method == 'POST':
        form = CarAdminForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Véhicule ajouté avec succès.")
            return redirect('admin_cars')
    else:
        form = CarAdminForm()
    return render(request, 'dashboard/admin_car_form.html', {'form': form})

@login_required
@staff_required
def admin_car_edit(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == 'POST':
        form = CarAdminForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            messages.success(request, "Véhicule mis à jour.")
            return redirect('admin_cars')
    else:
        form = CarAdminForm(instance=car)
    return render(request, 'dashboard/admin_car_form.html', {'form': form, 'car': car})

@login_required
@staff_required
def admin_car_delete(request, pk):
    car = get_object_or_404(Car, pk=pk)
    car.delete()
    messages.success(request, "Véhicule supprimé.")
    return redirect('admin_cars')

@login_required
@staff_required
def admin_bookings(request):
    bookings = Booking.objects.select_related('user', 'car').all()
    status_filter = request.GET.get('status')
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    return render(request, 'dashboard/admin_bookings.html', {'bookings': bookings})

@login_required
@staff_required
def admin_booking_update(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Booking.STATUS_CHOICES):
            booking.status = new_status
            booking.save()
            messages.success(request, f"Statut mis à jour : {booking.get_status_display()}")
            return redirect('admin_bookings')
    return render(request, 'dashboard/admin_booking_update.html', {
        'booking': booking,
        'status_choices': Booking.STATUS_CHOICES,
    })
