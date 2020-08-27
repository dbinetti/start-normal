# Third-Party
# First-Party
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
        'grades',
        'grades_display',
        'get_level_display',
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
            'get_level_display',
            'get_kind_display',
        ],
    }
    should_index = 'should_index'

class HomeroomIndex(AlgoliaIndex):
    fields = [
        'id',
        'get_status_display',
        'get_safety_display',
        'get_schedule_display',
        'get_frequency_display',
        'size',
        'notes',
        'schools',
        'grades',
        'parent_name',
        'student_names',
    ]
    geo_field = 'location'
    settings = {
        'searchableAttributes': [
            'schools',
            'grades',
            'parent_name',
            'student_names',
        ],
        'attributesForFaceting': [
            'get_status_display',
            'get_safety_display',
            'get_schedule_display',
            'get_frequency_display',
            'size',
        ],
    }
    should_index = 'should_index'
