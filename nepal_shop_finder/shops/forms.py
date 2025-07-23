from django import forms

class ShopSearchForm(forms.Form):
    CATEGORY_CHOICES = [
        ('mobile_shop', '📱 Mobile & Electronics'),
        ('grocery_store', '🛒 Grocery Stores'),
        ('clothing_store', '👕 Clothing Stores'),
        ('pharmacy', '💊 Pharmacies'),
        ('restaurant', '🍽️ Restaurants'),
        ('vehicle_showroom', '🚗 Vehicle Showrooms'),
        ('stationery', '📚 Stationery Shops'),
        ('gift_shop', '🎁 Gift Shops'),
        ('book_store', '📖 Book Stores'),
        ('hardware_store', '🔧 Hardware Stores'),
        ('beauty_salon', '💄 Beauty Salons'),
        ('gym', '💪 Gyms & Fitness'),
        ('bank', '🏦 Banks & ATMs'),
        ('hospital', '🏥 Hospitals & Clinics'),
        ('school', '🎓 Schools & Colleges'),
        ('hotel', '🏨 Hotels & Lodging'),
        ('gas_station', '⛽ Gas Stations'),
        ('bakery', '🥖 Bakeries'),
        ('jewelry_store', '💎 Jewelry Stores'),
        ('flower_shop', '🌸 Flower Shops'),
    ]
    
    NEPAL_CITIES = [
        ('kathmandu', 'Kathmandu'),
        ('pokhara', 'Pokhara'),
        ('lalitpur', 'Lalitpur (Patan)'),
        ('bhaktapur', 'Bhaktapur'),
        ('biratnagar', 'Biratnagar'),
        ('birgunj', 'Birgunj'),
        ('dharan', 'Dharan'),
        ('butwal', 'Butwal'),
        ('hetauda', 'Hetauda'),
        ('janakpur', 'Janakpur'),
        ('nepalgunj', 'Nepalgunj'),
        ('dhangadhi', 'Dhangadhi'),
        ('chitwan', 'Chitwan'),
        ('itahari', 'Itahari'),
        ('bharatpur', 'Bharatpur'),
    ]
    
    RADIUS_CHOICES = [
        (5000, '5 km'),
        (10000, '10 km'),
        (15000, '15 km'),
        (20000, '20 km'),
        (25000, '25 km'),
    ]
    
    location = forms.ChoiceField(
        choices=NEPAL_CITIES,
        widget=forms.Select(attrs={'class': 'form-control form-control-lg'}),
        initial='kathmandu'
    )
    
    custom_location = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Or enter custom location...'
        }),
        help_text='Leave empty to use selected city above'
    )
    
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control form-control-lg'}),
        initial='mobile_shop'
    )
    
    radius = forms.ChoiceField(
        choices=RADIUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control form-control-lg'}),
        initial=10000
    )
    
    def clean(self):
        cleaned_data = super().clean()
        location = cleaned_data.get('location')
        custom_location = cleaned_data.get('custom_location')
        
        # Use custom location if provided, otherwise use selected location
        if custom_location:
            cleaned_data['final_location'] = custom_location
        else:
            # Convert location code to display name
            location_dict = dict(self.NEPAL_CITIES)
            cleaned_data['final_location'] = location_dict.get(location, location)
        
        return cleaned_data
    

from django import forms

class MobileShopSearchForm(forms.Form):
    NEPAL_CITIES = [
        ('kathmandu', 'Kathmandu'),
        ('pokhara', 'Pokhara'),
        ('lalitpur', 'Lalitpur (Patan)'),
        ('bhaktapur', 'Bhaktapur'),
        ('biratnagar', 'Biratnagar'),
        ('birgunj', 'Birgunj'),
        ('dharan', 'Dharan'),
        ('butwal', 'Butwal'),
        ('hetauda', 'Hetauda'),
        ('janakpur', 'Janakpur'),
        ('nepalgunj', 'Nepalgunj'),
        ('dhangadhi', 'Dhangadhi'),
        ('chitwan', 'Chitwan'),
        ('itahari', 'Itahari'),
        ('bharatpur', 'Bharatpur'),
    ]
    
    RADIUS_CHOICES = [
        (2000, '2 km'),
        (5000, '5 km'),
        (10000, '10 km'),
        (15000, '15 km'),
        (20000, '20 km'),
        (25000, '25 km'),
    ]
    
    MAX_RESULTS_CHOICES = [
        (10, '10 shops'),
        (20, '20 shops'),
        (30, '30 shops'),
        (50, '50 shops'),
        (75, '75 shops'),
        (100, '100 shops'),
    ]
    CATEGORY_CHOICES = [
        ('mobile_shop', 'Mobile Shops'),
        ('phone_repair', 'Phone Repair'),
        ('accessories', 'Mobile Accessories'),
    ]
    
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control form-control-lg',
            'id': 'category-select'
        }),
        initial='mobile_shop',
        label='📱 Shop Category',
        help_text='Type of mobile-related shops to search for'
    )
    
    custom_location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter specific location (optional)',
            'id': 'custom-location'
        }),
        label='🔍 Specific Location',
        help_text='Add a more specific location within the city (optional)'
    )
    
    SORT_BY_CHOICES = [
        ('rating', 'Rating (High to Low)'),
        ('reviews', 'Number of Reviews'),
        ('distance', 'Distance (Nearest First)'),
        ('name', 'Name (A to Z)'),
    ]
    
    location = forms.ChoiceField(
        choices=NEPAL_CITIES,
        widget=forms.Select(attrs={
            'class': 'form-control form-control-lg',
            'id': 'location-select'
        }),
        initial='kathmandu',
        label='📍 Select City',
        help_text='Choose the city where you want to find mobile shops'
    )
    
    
    radius = forms.ChoiceField(
        choices=RADIUS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control form-control-lg',
            'id': 'radius-select'
        }),
        initial=10000,
        label='📏 Search Radius',
        help_text='How far to search from the location'
    )
    
    max_results = forms.ChoiceField(
        choices=MAX_RESULTS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control form-control-lg',
            'id': 'max-results-select'
        }),
        initial=30,
        label='📊 Maximum Results',
        help_text='How many mobile shops to find'
    )
    
    sort_by = forms.ChoiceField(
        choices=SORT_BY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control form-control-lg',
            'id': 'sort-select'
        }),
        initial='rating',
        label='🔄 Sort By',
        help_text='How to sort the search results'
    )
    
    include_reviews = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'include-reviews'
        }),
        label='📝 Include Customer Reviews',
        help_text='Get detailed customer reviews for each shop'
    )
    
    only_open_now = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'only-open'
        }),
        label='🕐 Only Currently Open Shops',
        help_text='Show only shops that are open right now'
    )
    
    min_rating = forms.FloatField(
        min_value=0.0,
        max_value=5.0,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'min': '0',
            'max': '5',
            'placeholder': '0.0',
            'id': 'min-rating'
        }),
        label='⭐ Minimum Rating',
        help_text='Only show shops with rating above this value (0-5)'
    )
    
    def clean(self):
        cleaned_data = super().clean()
        location = cleaned_data.get('location')

        location_dict = dict(self.NEPAL_CITIES)
        cleaned_data['final_location'] = location_dict.get(location, location)

        cleaned_data['radius'] = int(cleaned_data.get('radius', 10000))
        cleaned_data['max_results'] = int(cleaned_data.get('max_results', 30))
        
        return cleaned_data
    
    def get_search_parameters(self):
        """Return cleaned parameters ready for the MobileShopScraper"""
        if not self.is_valid():
            return None
            
        return {
            'location': self.cleaned_data['final_location'],
            'radius': self.cleaned_data['radius'],
            'max_results': self.cleaned_data['max_results'],
            'sort_by': self.cleaned_data['sort_by'],
            'include_reviews': self.cleaned_data['include_reviews'],
            'only_open_now': self.cleaned_data['only_open_now'],
            'min_rating': self.cleaned_data.get('min_rating', 0.0),
        }