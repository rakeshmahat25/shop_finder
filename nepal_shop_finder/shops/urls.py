from django.urls import path
from django.contrib.auth import views as auth_views 
from . import views

app_name = 'shops'

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search_view, name='search'),
    path('search_results/', views.search_results_view, name='search_results'),
    path('results/<int:search_id>/', views.results_view, name='results'),
    path('visualize/<int:search_id>/', views.visualize_view, name='visualize'),
    path('history/', views.search_history_view, name='history'),
    path('delete_search/<int:search_id>/', views.delete_search_view, name='delete_search'),
    path('shop/<int:shop_id>/', views.shop_detail_view, name='shop_detail'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='shops:search'), name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('clear-search-history/', views.clear_search_history, name='clear_search_history'),
]
