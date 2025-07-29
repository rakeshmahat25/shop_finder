from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf.urls.static import static
from django.conf import settings

def redirect_to_search(request):
    return redirect('shops:search')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_to_search),
    path('shops/', include('shops.urls')), 
    path('accounts/', include('allauth.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.SCRAPED_DATA_URL, document_root=settings.SCRAPED_DATA_ROOT)