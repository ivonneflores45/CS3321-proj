import django_filters
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
    category = django_filters.MultipleChoiceFilter(choices=Listing.CATEGORY_CHOICES, label='Category')
    condition = django_filters.MultipleChoiceFilter(choices=Listing.CONDITION_CHOICES, label='Condition')
    rarity = django_filters.MultipleChoiceFilter(choices=Listing.RARITY_CHOICES, label='Rarity')
    element = django_filters.MultipleChoiceFilter(choices=Listing.ELEMENT_CHOICES, label='Element')
    type = django_filters.MultipleChoiceFilter(choices=Listing.TYPE_CHOICES, label='Type')

    #set name search
    set_name = django_filters.CharFilter(lookup_expr='icontains', label='Set Name')

    #sort options
    sort = django_filters.OrderingFilter(
        fields = (
            ('base_price', 'price_asc'),
            ('-base_price', 'price_desc'),
            ('title', 'name_asc'),
        ),
        field_labels = {
            'base_price' : 'Prie: Low to High',
            '-base_price': 'Price: High to Low',
            'title' : 'Name: A to Z'
        }
    )

    class Meta: 
        model = Listing
        fields = {'title', 'set_name', 'category', 'condition', 'rarity', 'element', 'type'}


