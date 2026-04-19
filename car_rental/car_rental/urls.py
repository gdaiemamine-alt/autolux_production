from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from cars import views as car_views

def contact_view(request):
    sent = False
    if request.method == 'POST':
        sent = True
    return render(request, 'contact.html', {'sent': sent})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', car_views.home, name='home'),
    path('cars/', include('cars.urls')),
    path('bookings/', include('bookings.urls')),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('contact/', contact_view, name='contact'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = lambda req, exc: render(req, '404.html', status=404)
