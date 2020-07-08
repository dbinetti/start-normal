# Third-Party
# First-Party
import algoliasearch_django as algoliasearch
from algoliasearch_django import AlgoliaIndex

# Local
from .models import Petition


class PetitionIndex(AlgoliaIndex):
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


# class SchoolIndex(AlgoliaIndex):
#     fields = [
#         'name',
#         'slug',
#         'county',
#         'address',
#         'city',
#         'state',
#         'zipcode',
#         'phone',
#         'website',
#         'get_soc_display',
#         'nces_school_id',
#         'get_eil_display',
#         'grades',
#         'district',
#     ]
#     geo_field = 'location'
#     settings = {
#         'searchableAttributes': [
#             'name',
#             'slug',
#             'county',
#             'city',
#             'state',
#             'nces_school_id',
#         ],
#         'attributesForFaceting': [
#             'city',
#             'state',
#             'county',
#             'get_soc_display',
#             'get_eil_display',
#         ],
#     }
#     should_index = 'is_active'
