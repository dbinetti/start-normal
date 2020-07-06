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
    ]
    geo_field = 'location'
    settings = {
        'searchableAttributes': [
            'name',
            'slug',
            'county',
            'city',
            'state',
            # 'attributesForFaceting': [
            #     'city',
            #     'state',
            #     'county',
            # ],
        ],
    }
    should_index = 'is_active'


# class SchoolIndex(AlgoliaIndex):
#     fields = [
#         'name',
#         'slug',
#     ]
#     geo_field = 'location'
#     settings = {
#         'searchableAttributes': [
#             'name',
#             'slug',
#             'county',
#             'city',
#             'state',
#         ],
#     }
#     should_index = 'is_active'
