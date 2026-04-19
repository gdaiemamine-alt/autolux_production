from django.shortcuts import render, get_object_or_404
from .models import Car, Category

def home(request):
    featured_cars = Car.objects.filter(is_available=True)[:6]
    categories = Category.objects.all()
    total_cars = Car.objects.count()
    available_cars = Car.objects.filter(is_available=True).count()
    context = {
        'featured_cars': featured_cars,
        'categories': categories,
        'total_cars': total_cars,
        'available_cars': available_cars,
    }
    return render(request, 'home.html', context)

def car_list(request):
    cars = Car.objects.all()
    categories = Category.objects.all()

    category_id = request.GET.get('category')
    transmission = request.GET.get('transmission')
    fuel_type = request.GET.get('fuel_type')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    search = request.GET.get('search')
    available_only = request.GET.get('available_only')

    if category_id:
        cars = cars.filter(category_id=category_id)
    if transmission:
        cars = cars.filter(transmission=transmission)
    if fuel_type:
        cars = cars.filter(fuel_type=fuel_type)
    if min_price:
        cars = cars.filter(price_per_day__gte=min_price)
    if max_price:
        cars = cars.filter(price_per_day__lte=max_price)
    if search:
        cars = cars.filter(brand__icontains=search) | cars.filter(model__icontains=search)
    if available_only:
        cars = cars.filter(is_available=True)

    context = {
        'cars': cars,
        'categories': categories,
    }
    return render(request, 'cars/car_list.html', context)

def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    similar_cars = Car.objects.filter(category=car.category, is_available=True).exclude(pk=pk)[:3]
    context = {
        'car': car,
        'similar_cars': similar_cars,
    }
    return render(request, 'cars/car_detail.html', context)
