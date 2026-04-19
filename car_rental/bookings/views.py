from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking
from .forms import BookingForm
from cars.models import Car

@login_required
def book_car(request, car_pk):
    car = get_object_or_404(Car, pk=car_pk)
    if not car.is_available:
        messages.error(request, "Cette voiture n'est pas disponible.")
        return redirect('car_detail', pk=car_pk)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.car = car
            booking.save()
            car.is_available = False
            car.save()
            messages.success(request, f"Réservation confirmée ! Référence #{booking.pk}")
            return redirect('booking_detail', pk=booking.pk)
    else:
        form = BookingForm()

    context = {'car': car, 'form': form}
    return render(request, 'bookings/book_car.html', context)

@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    return render(request, 'bookings/booking_detail.html', {'booking': booking})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})

@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if booking.status in ['pending', 'confirmed']:
        booking.status = 'cancelled'
        booking.save()
        booking.car.is_available = True
        booking.car.save()
        messages.success(request, "Réservation annulée avec succès.")
    else:
        messages.error(request, "Cette réservation ne peut plus être annulée.")
    return redirect('my_bookings')
