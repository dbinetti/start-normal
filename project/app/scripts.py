# Standard Library
import csv

# Third-Party
from algoliasearch_django.decorators import disable_auto_indexing

# Django
from django.db import IntegrityError

# Local
from .forms import DistrictForm
from .forms import SchoolForm


def districts_list():
    with open('ca.csv') as f:
        reader = csv.reader(
            f,
            skipinitialspace=True,
        )
        rows = [row for row in reader]
        t = len(rows)
        i = 0
        errors = []
        output = []
        for row in rows:
            i += 1
            print(f"{i}/{t}")
            status_map = {
                'Active': 10,
                'Closed': 20,
                'Merged': 30,
            }
            status_key = str(row[3]) if row[3] != 'No Data' else None
            cd_status = status_map.get(status_key, None)
            district = {
                'schedule': 0,
                'masks': 0,
                'cd_status': cd_status,
                'name': str(row[5]) if row[5] != 'No Data' else '',
                'cd_id': int(row[0][:7]) if row[0] != 'No Data' else None,
                'nces_district_id': int(row[1]) if row[1] != 'No Data' else None,
                'district_name': str(row[5]) if row[5] != 'No Data' else '',
                'county': str(row[4]) if row[4] != 'No Data' else '',
                'address': str(row[8]) if row[8] != 'No Data' else '',
                'city': str(row[9]) if row[9] != 'No Data' else '',
                'state': str(row[11]) if row[11] != 'No Data' else '',
                'zipcode': str(row[10]) if row[10] != 'No Data' else '',
                'phone': str(row[17]) if row[17] != 'No Data' else '',
                'website': str(row[21].replace(" ", "")) if row[21] != 'No Data' else '',
                'doc': int(row[27]) if row[27] != 'No Data' else None,
                'latitude': float(row[41]) if row[41] != 'No Data' else None,
                'longitude': float(row[42]) if row[42] != 'No Data' else None,
                'admin_first_name': str(row[43]) if row[43] != 'No Data' else '',
                'admin_last_name': str(row[44]) if row[44] != 'No Data' else '',
                'admin_email': str(row[45].replace(
                    ' ', ''
                ).replace(
                    'ndenson@compton.k12.ca.u', 'ndenson@compton.k12.ca.us'
                ).replace(
                    'bmcconnell@compton.k12.ca.u', 'bmcconnell@compton.k12.ca.us'
                )) if row[45] not in [
                    'Information Not Available',
                    'No Data',
                ] else '',
            }
            form = DistrictForm(district)
            if not form.is_valid():
                errors.append((row, form))
                break
            output.append(district)
        if not errors:
            return output
        else:
            print('Error!')
            return errors


@disable_auto_indexing
def import_districts(districts):
    t = len(districts)
    i = 0

    for district in districts:
        i+=1
        print(f"{i}/{t}")
        try:
            District.objects.create(**district)
        except IntegrityError:
            continue

def privates_list(filename='privates.csv'):
    with open(filename) as f:
        reader = csv.reader(
            f,
            skipinitialspace=True,
        )
        rows = [row for row in reader]
        t = len(rows)
        i = 0
        errors = []
        output = []
        for row in rows:
            i += 1
            print(f"{i}/{t}")
            status_map = {
                'Active': 10,
                'Closed': 20,
                'Merged': 30,
            }
            status_key = str(row[3]) if row[3] != 'No Data' else None
            cd_status = status_map.get(status_key, None)
            district = {
                'schedule': 0,
                'masks': 0,
                'cd_status': cd_status,
                'name': str(row[5]) if row[5] != 'No Data' else '',
                'cd_id': int(row[0][:7]) if row[0] != 'No Data' else None,
                'nces_district_id': int(row[1]) if row[1] != 'No Data' else None,
                'district_name': str(row[5]) if row[5] != 'No Data' else '',
                'county': str(row[4]) if row[4] != 'No Data' else '',
                'address': str(row[8]) if row[8] != 'No Data' else '',
                'city': str(row[9]) if row[9] != 'No Data' else '',
                'state': str(row[11]) if row[11] != 'No Data' else '',
                'zipcode': str(row[10]) if row[10] != 'No Data' else '',
                'phone': str(row[17]) if row[17] != 'No Data' else '',
                'website': str(row[21].replace(" ", "")) if row[21] != 'No Data' else '',
                'doc': int(row[27]) if row[27] != 'No Data' else None,
                'latitude': float(row[41]) if row[41] != 'No Data' else None,
                'longitude': float(row[42]) if row[42] != 'No Data' else None,
                'admin_first_name': str(row[43]) if row[43] != 'No Data' else '',
                'admin_last_name': str(row[44]) if row[44] != 'No Data' else '',
                'admin_email': str(row[45].replace(
                    ' ', ''
                ).replace(
                    'ndenson@compton.k12.ca.u', 'ndenson@compton.k12.ca.us'
                ).replace(
                    'bmcconnell@compton.k12.ca.u', 'bmcconnell@compton.k12.ca.us'
                )) if row[45] not in [
                    'Information Not Available',
                    'No Data',
                ] else '',
            }
            form = DistrictForm(district)
            if not form.is_valid():
                errors.append((row, form))
                break
            output.append(district)
        if not errors:
            return output
        else:
            print('Error!')
            return errors


@disable_auto_indexing
def import_privates(privates):
    t = len(privates)
    i = 0

    for private in privates:
        i+=1
        print(f"{i}/{t}")
        Petition.objects.create(**privates)


def schools_list(filename):
    with open(filename) as f:
        reader = csv.reader(
            f,
            skipinitialspace=True,
        )
        rows = [row for row in reader]
        t = len(rows)
        i = 0
        errors = []
        output = []
        for row in rows:
            i += 1
            print(f"{i}/{t}")
            status_map = {
                'Active': 10,
                'Closed': 20,
                'Merged': 30,
            }
            funding_map = {
                'Directly funded': 10,
                'Locally funded': 20,
                'Disallowed': 30,
            }
            status_key = str(row[3]) if row[3] != 'No Data' else None
            cd_status = status_map.get(status_key, None)
            if cd_status != 10:
                continue
            name = str(row[6]) if row[6] != 'No Data' else ''
            if not name:
                continue
            try:
                charter_number = int(row[25]) if row[25] != 'No Data' else None
            except ValueError:
                charter_number = None
            school = {
                'schedule': 0,
                'masks': 0,
                'name': name,
                'cd_status': cd_status,
                'cd_id': int(row[0][-7:]) if row[0] != 'No Data' else None,
                'nces_district_id': int(row[1]) if row[1] != 'No Data' else None,
                'nces_school_id': int(row[2]) if row[2] != 'No Data' else None,
                'district_name': str(row[5]) if row[5] != 'No Data' else '',
                'county': str(row[4]) if row[4] != 'No Data' else '',
                'address': str(row[8]) if row[8] != 'No Data' else '',
                'city': str(row[9]) if row[9] != 'No Data' else '',
                'state': str(row[11]) if row[11] != 'No Data' else '',
                'zipcode': str(row[10]) if row[10] != 'No Data' else '',
                'phone': str(row[17]) if row[17] != 'No Data' else '',
                'website': str(row[21].replace(" ", "")) if row[21] != 'No Data' else '',
                'soc': int(row[29]) if row[29] != 'No Data' else None,

                'is_charter': True if row[24]=='Y' else False,
                'charter_number': charter_number,
                'funding_type': funding_map[str(row[26])] if row[26] != 'No Data' else None,
                'edops_type': getattr(School.EDOPS, str(row[31].strip().lower()), None),
                'eil': getattr(School.EIL, str(row[33].strip().lower()), None),
                'grade_span': str(row[35]) if row[35] != 'No Data' else '',
                'virtual_type': getattr(School.VIRTUAL, str(row[37].strip().lower()), None),
                'is_magnet': True if row[38]=='Y' else False,
                'fed_nces_school_id': int(row[40]) if row[40] != 'No Data' else None,

                'latitude': float(row[41]) if row[41] != 'No Data' else None,
                'longitude': float(row[42]) if row[42] != 'No Data' else None,
                'admin_first_name': str(row[43]) if row[43] != 'No Data' else '',
                'admin_last_name': str(row[44]) if row[44] != 'No Data' else '',
                'admin_email': str(row[45].replace(
                    ' ', ''
                ).replace(
                    'ndenson@compton.k12.ca.u', 'ndenson@compton.k12.ca.us'
                ).replace(
                    'bmcconnell@compton.k12.ca.u', 'bmcconnell@compton.k12.ca.us'
                )) if row[45] not in [
                    'Information Not Available',
                    'No Data',
                ] else '',
            }
            form = SchoolForm(school)
            if not form.is_valid():
                errors.append((row, form))
                break
            output.append(school)
        if not errors:
            return output
        else:
            print('Error!')
            return errors

@disable_auto_indexing
def import_schools(schools):
    t = len(schools)
    i = 0

    for school in schools:
        i+=1
        print(f"{i}/{t}")
        School.objects.create(**school)
