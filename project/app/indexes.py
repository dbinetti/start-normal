# Third-Party
import algoliasearch_django as algoliasearch
from algoliasearch_django import AlgoliaIndex

# Local
from .models import District
from .models import School


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
        'get_doc_display',
        'nces_district_id',
    ]
    geo_field = 'location'
    settings = {
        'searchableAttributes': [
            'name',
            'slug',
            'county',
            'city',
            'state',
            'nces_district_id',
        ],
        'attributesForFaceting': [
            'city',
            'state',
            'county',
        ],
    }
    should_index = 'is_active'


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
        'get_soc_display',
        'nces_school_id',
        'eil',
        'grades',
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
            'nces_school_id',
        ],
        'attributesForFaceting': [
            'city',
            'state',
            'county',
        ],
    }
    should_index = 'is_active'
