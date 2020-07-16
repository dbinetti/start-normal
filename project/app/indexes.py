# Third-Party
import algoliasearch_django as algoliasearch
from algoliasearch_django import AlgoliaIndex


class SchoolIndex(AlgoliaIndex):
    fields = [
        'name',
        'slug',
        'county',
        'address',
        'city',
        'state',
        'zipcode',
        'phone',
        'website',
        'nces_id',
        'get_kind_display',
        'district',
    ]
    geo_field = 'location'
    settings = {
        'searchableAttributes': [
            'name',
            'slug',
            'county',
            'city',
            'state',
            'nces_id',
        ],
        'attributesForFaceting': [
            'city',
            'state',
            'county',
            'get_kind_display',
        ],
    }
    should_index = 'is_active'

class DistrictIndex(AlgoliaIndex):
    fields = [
        'name',
        'slug',
        'county',
        'address',
        'city',
        'state',
        'zipcode',
        'phone',
        'website',
        'nces_id',
        'get_kind_display',
    ]
    geo_field = 'location'
    settings = {
        'searchableAttributes': [
            'name',
            'slug',
            'county',
            'city',
            'state',
            'nces_id',
        ],
        'attributesForFaceting': [
            'city',
            'state',
            'county',
            'get_kind_display',
        ],
    }
    should_index = 'is_active'
