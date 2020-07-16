# First-Party
import algoliasearch_django as algoliasearch
from algoliasearch_django import AlgoliaIndex


class OrganizationIndex(AlgoliaIndex):
    fields = [
        'name',
        'slug',
        'get_status_display',
        'get_kind_display',
        'nces_id',
        'address',
        'city',
        'state',
        'zipcode',
        'county',
        'phone',
        'website',
    ]
    geo_field = 'location'
    settings = {
        'searchableAttributes': [
            'name',
            'nces_id',
            'city',
            'state',
            'county',
        ],
        'attributesForFaceting': [
            'get_status_display',
            'get_kind_display',
        ],
    }
    should_index = 'should_index'


class SchoolIndex(AlgoliaIndex):
    fields = [
        'name',
        'slug',
        'description',
        'county',
        'address',
        'city',
        'state',
        'zipcode',
        'phone',
        'website',
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


class DistrictIndex(AlgoliaIndex):
    fields = [
        'name',
        'slug',
        'description',
        'county',
        'address',
        'city',
        'state',
        'zipcode',
        'phone',
        'website',
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
