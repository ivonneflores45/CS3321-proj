import django_filters
from django import forms
from .models import Listing

'''
Shop Filters: a robust filtering system that
allows users to select multiple filters
Author: Maryam Khan
Date created: 4/10/2026
'''

class ListingFilter(django_filters.FilterSet):
    #partial text search on title
    title = django_filters.CharFilter(lookup_expr='icontains', label='Search')

    #price range filters
    min_price = django_filters.NumberFilter(field_name='base_price', lookup_expr='gte', label='Min Price')
    max_price = django_filters.NumberFilter(field_name='base_price', lookup_expr='lte', label='Max Price')
    
    #dropdown filters using listing model choice sets
    category = django_filters.ChoiceFilter(
        choices=[('', 'All Categories')] + list(Listing.CATEGORY_CHOICES),
\
    )

    condition = django_filters.ChoiceFilter(
        choices=[('', 'All Conditions')] + list(Listing.CONDITION_CHOICES),

     
    )
    rarity = django_filters.ChoiceFilter(
        choices=[('', 'All Rarities')] + list(Listing.RARITY_CHOICES),

     
    )
    element = django_filters.ChoiceFilter(
        choices=[('', 'All Elements')] + list(Listing.ELEMENT_CHOICES),

    )
    types = django_filters.ChoiceFilter(
        choices=[('', 'All Types')] + list(Listing.TYPE_CHOICES),

     
    )
    #set name search
    set_name = django_filters.CharFilter(lookup_expr='icontains', label='Set Name')

    #sort options
    sort = django_filters.OrderingFilter(
        fields = (
            ('base_price', 'price_asc'),
            ('title', 'name_asc'),
        ),
        field_labels = {
            'base_price' : 'Prie: Low to High',
            '-base_price': 'Price: High to Low',
            'title' : 'Name: A to Z'
        },
        choices = [
            ('base_price', 'Price: Low to High'),
            ('-base_price', 'Price: High to Low'),
            ('title', 'Name: A to Z'),
        ]
    )

    class Meta: 
        model = Listing
        fields = {'title', 'set_name', 'category', 'condition', 'rarity', 'element', 'type'}


