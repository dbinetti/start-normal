# Third-Party
import algoliasearch_django as algoliasearch
from algoliasearch_django import AlgoliaIndex

# Local
from .models import District


class DistrictIndex(AlgoliaIndex):
    fields = [
        'name',
        'slug',
    ]
    geo_field = 'location'
    settings = {
        'searchableAttributes': [
            'name',
            'slug',
            'county_name',
            'city',
            'state',
        ],
    }
    should_index = 'should_index'
