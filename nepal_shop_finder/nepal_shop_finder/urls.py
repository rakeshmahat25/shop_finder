from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def redirect_to_search(request):
    return redirect('shops:search')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_to_search),
    path('shops/', include('shops.urls')),   
]