from django.db import models
from django.utils import timezone

class SearchHistory(models.Model):
    location = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    radius = models.IntegerField()
    results_count = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Search Histories"
    
    def __str__(self):
        return f"{self.category} in {self.location} - {self.results_count} results"

class Shop(models.Model):
    search_history = models.ForeignKey(SearchHistory, on_delete=models.CASCADE, related_name='shops')
    place_id = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    google_url = models.URLField(blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    rating = models.FloatField(blank=True, null=True)
    user_ratings_total = models.IntegerField(default=0)
    business_status = models.CharField(max_length=50, blank=True, null=True)
    price_level = models.IntegerField(blank=True, null=True)
    opening_hours = models.TextField(blank=True, null=True)
    reviews_summary = models.CharField(max_length=200, blank=True, null=True)
    types = models.TextField(blank=True, null=True)  # Store as comma-separated values
    vicinity = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-rating', '-user_ratings_total']
    
    def __str__(self):
        return self.name
    
    @property
    def types_list(self):
        """Return types as a list"""
        if self.types:
            return [t.strip() for t in self.types.split(',')]
        return []
    
    @property
    def rating_stars(self):
        """Return rating as stars for display"""
        if self.rating:
            return '★' * int(self.rating) + '☆' * (5 - int(self.rating))
        return 'No rating'