
import requests
import time
import csv
import os
from datetime import datetime
import time
from typing import List, Dict, Optional
from django.conf import settings

class NepalShopScraper:
    def __init__(self):
        """Initialize scraper with Google Places API key from Django settings"""
        self.api_key = settings.GOOGLE_MAPS_API_KEY
        self.base_url = "https://maps.googleapis.com/maps/api/place"
        
        # Nepal major cities with coordinates
        self.nepal_cities = {
            'kathmandu': {'lat': 27.7172, 'lng': 85.3240},
            'pokhara': {'lat': 28.2096, 'lng': 83.9856},
            'lalitpur': {'lat': 27.6588, 'lng': 85.3247},
            'patan': {'lat': 27.6588, 'lng': 85.3247},
            'bhaktapur': {'lat': 27.6710, 'lng': 85.4298},
            'biratnagar': {'lat': 26.4525, 'lng': 87.2718},
            'birgunj': {'lat': 27.0106, 'lng': 84.8721},
            'dharan': {'lat': 26.8147, 'lng': 87.2789},
            'butwal': {'lat': 27.7000, 'lng': 83.4486},
            'hetauda': {'lat': 27.4286, 'lng': 85.0326},
            'janakpur': {'lat': 26.7288, 'lng': 85.9266},
            'nepalgunj': {'lat': 28.0500, 'lng': 81.6167},
            'dhangadhi': {'lat': 28.6833, 'lng': 80.6000},
            'chitwan': {'lat': 27.5291, 'lng': 84.3542},
            'itahari': {'lat': 26.6650, 'lng': 87.2722},
            'bharatpur': {'lat': 27.6761, 'lng': 84.4361},
        }
        
        # Category-specific search queries and types
        self.category_config = {
            'mobile_shop': {
                'queries': ['mobile shop', 'phone store', 'electronics store', 'smartphone shop'],
                'types': ['electronics_store'],
                'keywords': ['mobile', 'phone', 'smartphone', 'electronics', 'gadget']
            },
            'grocery_store': {
                'queries': ['grocery store', 'supermarket', 'general store', 'convenience store'],
                'types': ['grocery_or_supermarket', 'store'],
                'keywords': ['grocery', 'supermarket', 'store', 'mart']
            },
            'clothing_store': {
                'queries': ['clothing store', 'fashion store', 'garment shop', 'boutique'],
                'types': ['clothing_store'],
                'keywords': ['clothing', 'fashion', 'garment', 'boutique', 'dress']
            },
            'pharmacy': {
                'queries': ['pharmacy', 'medical store', 'drug store', 'chemist'],
                'types': ['pharmacy'],
                'keywords': ['pharmacy', 'medical', 'drug', 'medicine', 'chemist']
            },
            'restaurant': {
                'queries': ['restaurant', 'cafe', 'food', 'dining'],
                'types': ['restaurant', 'food'],
                'keywords': ['restaurant', 'cafe', 'food', 'dining', 'kitchen']
            },
            'vehicle_showroom': {
                'queries': ['car showroom', 'vehicle dealer', 'auto dealer', 'motorcycle dealer'],
                'types': ['car_dealer'],
                'keywords': ['car', 'vehicle', 'auto', 'motorcycle', 'showroom', 'dealer']
            },
            'stationery': {
                'queries': ['stationery shop', 'book store', 'office supplies'],
                'types': ['book_store'],
                'keywords': ['stationery', 'book', 'office', 'supplies', 'pen', 'paper']
            },
            'gift_shop': {
                'queries': ['gift shop', 'souvenir shop', 'novelty store'],
                'types': ['store'],
                'keywords': ['gift', 'souvenir', 'novelty', 'present']
            },
            'book_store': {
                'queries': ['book store', 'bookshop', 'library'],
                'types': ['book_store'],
                'keywords': ['book', 'library', 'publication', 'reading']
            },
            'hardware_store': {
                'queries': ['hardware store', 'tools shop', 'construction materials'],
                'types': ['hardware_store'],
                'keywords': ['hardware', 'tools', 'construction', 'materials']
            },
            'beauty_salon': {
                'queries': ['beauty salon', 'hair salon', 'spa', 'beauty parlor'],
                'types': ['beauty_salon', 'spa'],
                'keywords': ['beauty', 'salon', 'hair', 'spa', 'parlor']
            },
            'gym': {
                'queries': ['gym', 'fitness center', 'health club'],
                'types': ['gym'],
                'keywords': ['gym', 'fitness', 'health', 'exercise', 'workout']
            },
            'bank': {
                'queries': ['bank', 'ATM', 'financial institution'],
                'types': ['bank', 'atm'],
                'keywords': ['bank', 'atm', 'financial', 'money']
            },
            'hospital': {
                'queries': ['hospital', 'clinic', 'medical center'],
                'types': ['hospital', 'doctor'],
                'keywords': ['hospital', 'clinic', 'medical', 'health', 'doctor']
            },
            'school': {
                'queries': ['school', 'college', 'university', 'education'],
                'types': ['school', 'university'],
                'keywords': ['school', 'college', 'university', 'education', 'academy']
            },
            'hotel': {
                'queries': ['hotel', 'lodge', 'guest house', 'accommodation'],
                'types': ['lodging'],
                'keywords': ['hotel', 'lodge', 'guest', 'accommodation', 'stay']
            },
            'gas_station': {
                'queries': ['gas station', 'petrol pump', 'fuel station'],
                'types': ['gas_station'],
                'keywords': ['gas', 'petrol', 'fuel', 'station', 'pump']
            },
            'bakery': {
                'queries': ['bakery', 'cake shop', 'pastry shop'],
                'types': ['bakery'],
                'keywords': ['bakery', 'cake', 'pastry', 'bread', 'bakehouse']
            },
            'jewelry_store': {
                'queries': ['jewelry store', 'gold shop', 'jeweler'],
                'types': ['jewelry_store'],
                'keywords': ['jewelry', 'gold', 'silver', 'jeweler', 'ornament']
            },
            'flower_shop': {
                'queries': ['flower shop', 'florist', 'plant nursery'],
                'types': ['florist'],
                'keywords': ['flower', 'florist', 'plant', 'nursery', 'garden']
            }
        }
    
    def search_shops(self, location: str, category: str, radius: int = 10000) -> List[Dict]:
        """Search for shops using Google Places API"""
        print(f"Searching for {category} in {location}...")
        
        coordinates = self._get_location_coordinates(location)
        if not coordinates:
            return []
        
        config = self.category_config.get(category, self.category_config['mobile_shop'])
        all_shops = []
        
        for query in config['queries']:
            shops = self._search_places_nearby(coordinates, query, radius, config['types'][0])
            
            # Add unique shops only
            for shop in shops:
                if not any(existing['place_id'] == shop['place_id'] for existing in all_shops):
                    if self._is_relevant_shop(shop, config['keywords']):
                        all_shops.append(shop)
            
            time.sleep(1)  # Rate limiting
        
        # Get detailed information
        detailed_shops = []
        for shop in all_shops[:50]:  # Limit to 50 shops to avoid quota issues
            details = self._get_place_details(shop['place_id'])
            if details:
                shop.update(details)
                detailed_shops.append(shop)
            time.sleep(0.5)  # Rate limiting
        
        return detailed_shops
    
    def _get_location_coordinates(self, location: str) -> Optional[Dict]:
        """Get coordinates for a location"""
        location_lower = location.lower()
        
        if location_lower in self.nepal_cities:
            return self.nepal_cities[location_lower]
        
        # Use Geocoding API for unknown locations
        geocode_url = f"{self.base_url}/findplacefromtext/json"
        params = {
            'input': f"{location}, Nepal",
            'inputtype': 'textquery',
            'fields': 'geometry',
            'key': self.api_key
        }
        
        try:
            response = requests.get(geocode_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == 'OK' and data['candidates']:
                location_data = data['candidates'][0]['geometry']['location']
                return {'lat': location_data['lat'], 'lng': location_data['lng']}
        
        except requests.RequestException:
            pass
        
        return None
    
    def _search_places_nearby(self, coordinates: Dict, query: str, radius: int, place_type: str) -> List[Dict]:
        """Search for places using Google Places Nearby Search"""
        nearby_url = f"{self.base_url}/nearbysearch/json"
        params = {
            'location': f"{coordinates['lat']},{coordinates['lng']}",
            'radius': radius,
            'keyword': query,
            'type': place_type,
            'key': self.api_key
        }
        
        shops = []
        
        try:
            response = requests.get(nearby_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == 'OK':
                for place in data.get('results', []):
                    shop_info = {
                        'place_id': place['place_id'],
                        'name': place.get('name', 'N/A'),
                        'rating': place.get('rating', None),
                        'user_ratings_total': place.get('user_ratings_total', 0),
                        'vicinity': place.get('vicinity', 'N/A'),
                        'latitude': place['geometry']['location']['lat'],
                        'longitude': place['geometry']['location']['lng'],
                        'types': place.get('types', []),
                        'business_status': place.get('business_status', 'N/A'),
                        'price_level': place.get('price_level', None)
                    }
                    shops.append(shop_info)
        
        except requests.RequestException as e:
            print(f"Error searching places: {e}")
        
        return shops
    
    def _is_relevant_shop(self, place: Dict, keywords: List[str]) -> bool:
        """Check if a place is relevant to the search category"""
        name = place.get('name', '').lower()
        types = ' '.join(place.get('types', [])).lower()
        combined_text = f"{name} {types}"
        
        return any(keyword in combined_text for keyword in keywords)
    
    def _get_place_details(self, place_id: str) -> Optional[Dict]:
        """Get detailed information for a place"""
        details_url = f"{self.base_url}/details/json"
        params = {
            'place_id': place_id,
            'fields': 'name,formatted_phone_number,international_phone_number,formatted_address,website,opening_hours,reviews,url',
            'key': self.api_key
        }
        
        try:
            response = requests.get(details_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == 'OK':
                result = data['result']
                
                opening_hours = 'N/A'
                if 'opening_hours' in result:
                    weekday_text = result['opening_hours'].get('weekday_text', [])
                    opening_hours = '; '.join(weekday_text) if weekday_text else 'N/A'
                
                reviews_summary = 'N/A'
                if 'reviews' in result and result['reviews']:
                    reviews_summary = f"{len(result['reviews'])} reviews available"
                
                return {
                    'phone': result.get('formatted_phone_number', result.get('international_phone_number', 'N/A')),
                    'address': result.get('formatted_address', 'N/A'),
                    'website': result.get('website', 'N/A'),
                    'google_url': result.get('url', 'N/A'),
                    'opening_hours': opening_hours,
                    'reviews_summary': reviews_summary
                }
        
        except requests.RequestException as e:
            print(f"Error getting place details: {e}")
        
        return None



class MobileShopScraper:
    def __init__(self):
        """Initialize mobile shop scraper with Google Places API key from Django settings"""
        self.api_key = settings.GOOGLE_MAPS_API_KEY
        self.base_url = "https://maps.googleapis.com/maps/api/place"

        # Nepal major cities with coordinates
        self.nepal_cities = {
            'kathmandu': {'lat': 27.7172, 'lng': 85.3240},
            'pokhara': {'lat': 28.2096, 'lng': 83.9856},
            'lalitpur': {'lat': 27.6588, 'lng': 85.3247},
            'patan': {'lat': 27.6588, 'lng': 85.3247},
            'bhaktapur': {'lat': 27.6710, 'lng': 85.4298},
            'biratnagar': {'lat': 26.4525, 'lng': 87.2718},
            'birgunj': {'lat': 27.0106, 'lng': 84.8721},
            'dharan': {'lat': 26.8147, 'lng': 87.2789},
            'butwal': {'lat': 27.7000, 'lng': 83.4486},
            'hetauda': {'lat': 27.4286, 'lng': 85.0326},
            'janakpur': {'lat': 26.7288, 'lng': 85.9266},
            'nepalgunj': {'lat': 28.0500, 'lng': 81.6167},
            'dhangadhi': {'lat': 28.6833, 'lng': 80.6000},
            'chitwan': {'lat': 27.5291, 'lng': 84.3542},
            'itahari': {'lat': 26.6650, 'lng': 87.2722},
            'bharatpur': {'lat': 27.6761, 'lng': 84.4361},
        }

        # Mobile shop specific search configuration
        self.mobile_shop_config = {
            'queries': [
                'mobile shop', 'phone store', 'smartphone shop',
                'cell phone store', 'mobile phone dealer',
                'electronics store mobile', 'gadget store',
                'mobile accessories shop'
            ],
            'types': ['electronics_store', 'store'],
            'keywords': [
                'mobile', 'phone', 'smartphone', 'cell phone',
                'electronics', 'gadget', 'samsung', 'apple',
                'iphone', 'android', 'accessories', 'sim card',
                'mobile repair', 'phone repair'
            ]
        }

    def search_mobile_shops(self, location: str, radius: int = 10000, max_results: int = 50) -> List[Dict]:
        print(f"Searching for mobile shops in {location}...")
        coordinates = self._get_location_coordinates(location)
        if not coordinates:
            print(f"Could not find coordinates for {location}")
            return []

        all_mobile_shops = []

        for query in self.mobile_shop_config['queries']:
            print(f"Searching with query: {query}")
            shops = self._search_places_nearby(coordinates, query, radius)
            for shop in shops:
                if not any(existing['place_id'] == shop['place_id'] for existing in all_mobile_shops):
                    if self._is_mobile_shop(shop):
                        all_mobile_shops.append(shop)
            time.sleep(1)

        print(f"Found {len(all_mobile_shops)} unique mobile shops")

        detailed_shops = []
        for i, shop in enumerate(all_mobile_shops[:max_results]):
            print(f"Getting details for shop {i + 1}/{min(len(all_mobile_shops), max_results)}: {shop['name']}")
            details = self._get_place_details(shop['place_id'])
            if details:
                shop.update(details)
                detailed_shops.append(shop)
            time.sleep(0.5)

        # Sort by rating and user ratings
        detailed_shops.sort(key=lambda x: (x.get('rating', 0) or 0, x.get('user_ratings_total', 0)), reverse=True)

        # Save to CSV
        self._save_to_csv(detailed_shops, location)

        print(f"✅ Successfully saved details of {len(detailed_shops)} shops.")
        return detailed_shops

    def _get_location_coordinates(self, location: str) -> Optional[Dict]:
        location_lower = location.lower().strip()
        if location_lower in self.nepal_cities:
            return self.nepal_cities[location_lower]

        geocode_url = f"{self.base_url}/findplacefromtext/json"
        params = {
            'input': f"{location}, Nepal",
            'inputtype': 'textquery',
            'fields': 'geometry',
            'key': self.api_key
        }

        try:
            response = requests.get(geocode_url, params=params)
            response.raise_for_status()
            data = response.json()

            if data['status'] == 'OK' and data['candidates']:
                location_data = data['candidates'][0]['geometry']['location']
                return {'lat': location_data['lat'], 'lng': location_data['lng']}
        except requests.RequestException as e:
            print(f"Error geocoding location: {e}")
        return None

    def _search_places_nearby(self, coordinates: Dict, query: str, radius: int) -> List[Dict]:
        nearby_url = f"{self.base_url}/nearbysearch/json"
        params = {
            'location': f"{coordinates['lat']},{coordinates['lng']}",
            'radius': radius,
            'keyword': query,
            'type': 'electronics_store',
            'key': self.api_key,
            'language': 'en',
            'region': 'np'
        }

        shops = []
        try:
            response = requests.get(nearby_url, params=params)
            response.raise_for_status()
            data = response.json()

            if data['status'] == 'OK':
                for place in data.get('results', []):
                    shop_info = {
                        'place_id': place['place_id'],
                        'name': place.get('name', 'N/A'),
                        'rating': place.get('rating', None),
                        'user_ratings_total': place.get('user_ratings_total', 0),
                        'vicinity': place.get('vicinity', 'N/A'),
                        'latitude': place['geometry']['location']['lat'],
                        'longitude': place['geometry']['location']['lng'],
                        'types': place.get('types', []),
                        'business_status': place.get('business_status', 'N/A'),
                        'price_level': place.get('price_level', None),
                        'permanently_closed': place.get('permanently_closed', False)
                    }
                    shops.append(shop_info)
        except requests.RequestException as e:
            print(f"Error searching places: {e}")
        return shops

    def _is_mobile_shop(self, place: Dict) -> bool:
        name = place.get('name', '').lower()
        types = ' '.join(place.get('types', [])).lower()
        vicinity = place.get('vicinity', '').lower()
        combined_text = f"{name} {types} {vicinity}"

        mobile_keywords = self.mobile_shop_config['keywords']
        has_mobile_keyword = any(keyword in combined_text for keyword in mobile_keywords)

        exclude_keywords = [
            'hospital', 'school', 'restaurant', 'hotel', 'bank',
            'pharmacy', 'gas station', 'grocery', 'clothing',
            'beauty salon', 'gym', 'church', 'temple'
        ]
        has_exclude_keyword = any(keyword in combined_text for keyword in exclude_keywords)

        return has_mobile_keyword and not has_exclude_keyword

    def _get_place_details(self, place_id: str) -> Optional[Dict]:
        details_url = f"{self.base_url}/details/json"
        params = {
            'place_id': place_id,
            'fields': 'name,formatted_phone_number,international_phone_number,formatted_address,website,opening_hours,reviews,url,business_status,price_level',
            'key': self.api_key
        }

        try:
            response = requests.get(details_url, params=params)
            response.raise_for_status()
            data = response.json()

            if data['status'] == 'OK':
                result = data['result']

                opening_hours = 'N/A'
                is_open_now = None
                if 'opening_hours' in result:
                    weekday_text = result['opening_hours'].get('weekday_text', [])
                    opening_hours = '; '.join(weekday_text) if weekday_text else 'N/A'
                    is_open_now = result['opening_hours'].get('open_now', None)

                reviews_summary = 'N/A'
                latest_reviews = []
                if 'reviews' in result and result['reviews']:
                    reviews_count = len(result['reviews'])
                    reviews_summary = f"{reviews_count} reviews available"
                    latest_reviews = [
                        {
                            'author': review.get('author_name', 'Anonymous'),
                            'rating': review.get('rating', ''),
                            'text': review.get('text', ''),
                            'relative_time': review.get('relative_time_description', '')
                        }
                        for review in result['reviews'][:3]
                    ]

                details = {
                    'phone': result.get('international_phone_number', result.get('formatted_phone_number', 'N/A')),
                    'address': result.get('formatted_address', 'N/A'),
                    'website': result.get('website', 'N/A'),
                    'opening_hours': opening_hours,
                    'is_open_now': is_open_now,
                    'reviews_summary': reviews_summary,
                    'latest_reviews': latest_reviews,
                    'google_url': result.get('url', ''),
                    'business_status': result.get('business_status', 'N/A'),
                    'price_level': result.get('price_level', None)
                }
                return details
        except requests.RequestException as e:
            print(f"Error getting place details: {e}")
        return None

    def _save_to_csv(self, shops: List[Dict], location: str):
        timestamp = datetime.now().strftime("%Y-%m-%d")
        safe_location = location.lower().replace(" ", "_")
        filename = f"{safe_location}_mobile_shops_{timestamp}.csv"

        output_dir = os.path.join(settings.BASE_DIR, 'scraped_data')
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)

        fieldnames = [
            'name', 'address', 'phone', 'website', 'google_url',
            'latitude', 'longitude', 'rating', 'user_ratings_total',
            'opening_hours', 'reviews_summary', 'business_status',
            'price_level'
        ]

        with open(filepath, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for shop in shops:
                writer.writerow({
                    'name': shop.get('name', ''),
                    'address': shop.get('address', ''),
                    'phone': shop.get('phone', ''),
                    'website': shop.get('website', ''),
                    'google_url': shop.get('google_url', ''),
                    'latitude': shop.get('latitude', ''),
                    'longitude': shop.get('longitude', ''),
                    'rating': shop.get('rating', ''),
                    'user_ratings_total': shop.get('user_ratings_total', ''),
                    'opening_hours': shop.get('opening_hours', ''),
                    'reviews_summary': shop.get('reviews_summary', ''),
                    'business_status': shop.get('business_status', ''),
                    'price_level': shop.get('price_level', ''),
                })

        print(f"\n📁 CSV file saved: {filepath}")
        return filename
