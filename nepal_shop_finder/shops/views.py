from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Avg
from django.contrib.auth.decorators import login_required
from .forms import ShopSearchForm, MobileShopSearchForm
from .models import SearchHistory, Shop
from .utils import NepalShopScraper, MobileShopScraper
import json

def index(request):
    """Main landing page"""
    return render(request, 'shops/index.html')

def search_view(request):
    """Main search page. Shows recent searches only to logged-in users."""
    form = MobileShopSearchForm()
    recent_searches = [] 

    # Check if the user making the request is logged in
    if request.user.is_authenticated:

        recent_searches = SearchHistory.objects.filter(user=request.user).order_by('-created_at')[:5]

    context = {
        'form': form,
        'recent_searches': recent_searches,
    }
    return render(request, 'shops/search.html', context)

@login_required
def search_results_view(request):
    """Handle search form submission and display results"""
    if request.method == 'POST':
        
        form = MobileShopSearchForm(request.POST)
        if not form.is_valid():
            # Print form errors to console for debugging
            print("Form errors:", form.errors.as_json())
            messages.error(request, f'Please correct the errors: {form.errors}')
            return redirect('shops:search')
        
        if form.is_valid():
            # Get all parameters from the form's get_search_parameters method
            search_params = form.get_search_parameters()
            if not search_params:
                messages.error(request, 'Invalid search parameters')
                return redirect('shops:search')
            
            try:
                # Initialize scraper and search
                scraper = MobileShopScraper()

                shops_data = scraper.search_mobile_shops(
                    location=search_params['location'],
                    radius=search_params['radius'],
                    max_results=search_params['max_results']
                )
                filename = scraper._save_to_csv(shops_data, search_params['location'])
                
                # Save search history
                search_history = SearchHistory.objects.create(
                    user=request.user,
                    location=search_params['location'],
                    category=form.cleaned_data['category'],
                    radius=search_params['radius'],
                    results_count=len(shops_data),
                    csv_filename=filename  # save the file name here
                )
                print('debug: Search history created:', search_history)
                # Save shops data
                for shop_data in shops_data:
                    Shop.objects.create(
                        search_history=search_history,
                        place_id=shop_data.get('place_id', ''),
                        name=shop_data.get('name', 'N/A'),
                        phone=shop_data.get('phone', ''),
                        address=shop_data.get('address', ''),
                        website=shop_data.get('website', ''),
                        google_url=shop_data.get('google_url', ''),
                        latitude=shop_data.get('latitude', 0),
                        longitude=shop_data.get('longitude', 0),
                        rating=shop_data.get('rating'),
                        user_ratings_total=shop_data.get('user_ratings_total', 0),
                        business_status=shop_data.get('business_status', ''),
                        price_level=shop_data.get('price_level'),
                        opening_hours=shop_data.get('opening_hours', ''),
                        reviews_summary=shop_data.get('reviews_summary', ''),
                        types=', '.join(shop_data.get('types', [])),
                        vicinity=shop_data.get('vicinity', '')
                    )
                
                if shops_data:
                    messages.success(request, f'Found {len(shops_data)} {form.cleaned_data["category"].replace("_", " ")} in {form.cleaned_data["location"]}!')
                    return redirect('shops:results', search_id=search_history.id)
                else:
                    messages.warning(request, f'No {form.cleaned_data["category"].replace("_", " ")} found in {form.cleaned_data["location"]}. Try increasing the search radius.')
            
            except Exception as e:
                messages.error(request, f'An error occurred during search: {str(e)}')
        
        else:
            messages.error(request, 'Please correct the errors in the form.')
    
    return redirect('shops:search')

@login_required
def results_view(request, search_id):
    """Display search results"""
    search_history = get_object_or_404(SearchHistory, id=search_id)
    shops = Shop.objects.filter(search_history=search_history)
    
    # Apply filters
    search_query = request.GET.get('search', '')
    min_rating = request.GET.get('min_rating', '')
    sort_by = request.GET.get('sort', 'rating')
    
    if search_query:
        shops = shops.filter(
            Q(name__icontains=search_query) | 
            Q(address__icontains=search_query) |
            Q(vicinity__icontains=search_query)
        )
    
    if min_rating:
        try:
            min_rating_value = float(min_rating)
            shops = shops.filter(rating__gte=min_rating_value)
        except ValueError:
            pass
    
    # Sort results
    if sort_by == 'rating':
        shops = shops.order_by('-rating', '-user_ratings_total')
    elif sort_by == 'name':
        shops = shops.order_by('name')
    elif sort_by == 'reviews':
        shops = shops.order_by('-user_ratings_total')
    
    # Pagination
    paginator = Paginator(shops, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistics
    stats = {
        'total_shops': shops.count(),
        'with_phone': shops.exclude(Q(phone='') | Q(phone='N/A')).count(),
        'with_website': shops.exclude(Q(website='') | Q(website='N/A')).count(),
        'with_rating': shops.filter(rating__isnull=False).count(),
        'avg_rating': shops.filter(rating__isnull=False).aggregate(
            avg_rating=Avg('rating')
        )['avg_rating'] or 0
    }
    
    context = {
        'search_history': search_history,
        'page_obj': page_obj,
        'shops': page_obj,
        'stats': stats,
        'search_query': search_query,
        'min_rating': min_rating,
        'sort_by': sort_by,
    }
    
    return render(request, 'shops/results.html', context)

@login_required
def visualize_view(request, search_id):
    """Display data visualizations"""
    search_history = get_object_or_404(SearchHistory, id=search_id)
    shops = Shop.objects.filter(search_history=search_history)
    
    # --- REFINED DATA PREPARATION FOR CHARTS ---

    # 1. Rating Distribution Data
    rating_labels = ['1-2', '2-3', '3-4', '4-5', '5']
    rating_values = [
        shops.filter(rating__gte=1, rating__lt=2).count(),
        shops.filter(rating__gte=2, rating__lt=3).count(),
        shops.filter(rating__gte=3, rating__lt=4).count(),
        shops.filter(rating__gte=4, rating__lt=5).count(),
        shops.filter(rating=5).count(),
    ]
    rating_distribution = {
        'labels': rating_labels,
        'data': rating_values,
    }

    # 2. Open vs. Closed Status Data
    open_now_count = shops.filter(business_status='OPERATIONAL').count()
    closed_count = shops.count() - open_now_count
    status_distribution = {
        'labels': ['Open', 'Closed'],
        'data': [open_now_count, closed_count],
    }
    
    context = {
        'search_history': search_history,
        # Pass the structured data, converted to JSON string for JS
        'rating_distribution': json.dumps(rating_distribution),
        'status_distribution': json.dumps(status_distribution),
    }
    
    return render(request, 'shops/visualize.html', context)

@login_required
def search_history_view(request):
    """Display search history"""
    searches = SearchHistory.objects.all()
    
    # Pagination
    paginator = Paginator(searches, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'searches': page_obj
    }
    
    return render(request, 'shops/history.html', context)

@login_required
def delete_search_view(request, search_id):
    """Delete a search history record"""
    if request.method == 'POST':
        search_history = get_object_or_404(SearchHistory, id=search_id)
        search_history.delete()
        messages.success(request, 'Search history deleted successfully.')
    
    return redirect('shops:history')

@login_required
def shop_detail_view(request, shop_id):
    """Display detailed shop information"""
    shop = get_object_or_404(Shop, id=shop_id)
    
    context = {
        'shop': shop,
        'search_history': shop.search_history
    }
    
    return render(request, 'shops/shop_detail.html', context)

@login_required
def clear_search_history(request):
    if request.method == 'POST':
        # Delete all search history for the current user
        SearchHistory.objects.filter(user=request.user).delete()
        return redirect('shops:search_history')  # adjust to your URL name
    return redirect('shops:search_history')

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('shops:search') # Redirect logged-in users away

    if request.method == 'POST':
        # UserCreationForm handles validation and password hashing automatically
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Create the user
            login(request, user)  # Log them in immediately
            messages.success(request, "Account created successfully! You are now logged in.")
            return redirect('shops:search') # Redirect to the main search page
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/signup.html', {'form': form})

import os
from django.conf import settings
from django.http import FileResponse, Http404

def favicon_view(request):
    # CHANGE THE PATH to look inside the 'favicon_io' folder
    favicon_path = os.path.join(settings.BASE_DIR, 'favicon_io', 'favicon.ico')
    
    if os.path.exists(favicon_path):
        return FileResponse(open(favicon_path, 'rb'))
    else:
        raise Http404("Favicon not found")

