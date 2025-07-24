from django.urls import path
from django.contrib.auth import views as auth_views 
from . import views

app_name = 'shops'

urlpatterns = [
    path('', views.search_view, name='search'),
    path('search/', views.search_results_view, name='search_results'),
    path('results/<int:search_id>/', views.results_view, name='results'),
    path('visualize/<int:search_id>/', views.visualize_view, name='visualize'),
    path('history/', views.search_history_view, name='history'),
    path('delete/<int:search_id>/', views.delete_search_view, name='delete_search'),
    path('shop/<int:shop_id>/', views.shop_detail_view, name='shop_detail'),
   # --- Authentication URLs ---
    # Use Django's built-in LoginView. We just tell it which template to use.
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    
    # Use Django's built-in LogoutView. It handles everything.
    path('logout/', auth_views.LogoutView.as_view(next_page='shops:search'), name='logout'),
    # Use your custom view for signing up.
    path('signup/', views.signup_view, name='signup'),
]