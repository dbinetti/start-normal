# Third-Party
from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

# Local
from .models import District


# @register(District)
class DistrictIndex(AlgoliaIndex):
    fields = [
        'name',
         'date',
    ]
    geo_field = 'location'
    settings = {
        'searchableAttributes': [
            'name',
        ],
    }
    should_index = 'should_index'
