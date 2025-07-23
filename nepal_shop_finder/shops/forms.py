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
        label='📱 Shop Category'
    )
    
    custom_location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter specific location (optional)',
            'id': 'custom-location'
        }),
        label='🔍 Specific Location'
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
        label='📍 Select City'
    )
    
    
    radius = forms.ChoiceField(
        choices=RADIUS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control form-control-lg',
            'id': 'radius-select'
        }),
        initial=10000,
        label='📏 Search Radius'
    )
    
    max_results = forms.ChoiceField(
        choices=MAX_RESULTS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control form-control-lg',
            'id': 'max-results-select'
        }),
        initial=30,
        label='📊 Maximum Results'
    )
    
    sort_by = forms.ChoiceField(
        choices=SORT_BY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control form-control-lg',
            'id': 'sort-select'
        }),
        initial='rating',
        label='🔄 Sort By'
    )
    
    include_reviews = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'include-reviews'
        }),
        label='📝 Include Customer Reviews'
    )
    
    only_open_now = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'only-open'
        }),
        label='🕐 Only Currently Open Shops'
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
        label='⭐ Minimum Rating'
    )
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Ensure required fields are present
        required_fields = ['location', 'radius', 'max_results']
        for field in required_fields:
            if field not in cleaned_data:
                self.add_error(field, 'This field is required')
                return cleaned_data
        
        try:
            location = cleaned_data.get('location')
            location_dict = dict(self.NEPAL_CITIES)
            cleaned_data['final_location'] = location_dict.get(location, location)

            # Convert string values to integers safely
            cleaned_data['radius'] = int(cleaned_data.get('radius', 10000))
            cleaned_data['max_results'] = int(cleaned_data.get('max_results', 30))
            
        except (ValueError, TypeError) as e:
            self.add_error(None, f'Invalid input: {str(e)}')
        
        return cleaned_data
    
    def get_search_parameters(self):
        """Return cleaned parameters ready for the MobileShopScraper"""
        if not self.is_valid():
            print("Form is not valid in get_search_parameters")
            return None
        
        try:
            return {
                'location': self.cleaned_data.get('final_location', ''),
                'radius': self.cleaned_data.get('radius', 10000),
                'max_results': self.cleaned_data.get('max_results', 30),
                'sort_by': self.cleaned_data.get('sort_by', 'rating'),
                'include_reviews': self.cleaned_data.get('include_reviews', True),
                'only_open_now': self.cleaned_data.get('only_open_now', False),
                'min_rating': self.cleaned_data.get('min_rating', 0.0),
                'category': self.cleaned_data.get('category', 'mobile_shop')
            }
        except KeyError as e:
            print(f"Missing key in cleaned_data: {e}")
            return None