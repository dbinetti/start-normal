# Generated by Django 3.0.8 on 2020-07-06 13:37

import autoslug.fields
from django.db import migrations, models
import hashid_field.field


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_auto_20200706_0630'),
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique=True)),
                ('status', models.TextField(blank=True)),
                ('schedule', models.IntegerField(choices=[(0, '(Unknown)'), (10, 'In-Person'), (20, 'Blended'), (30, 'Distance'), (40, 'Undecided')], default=0, null=True)),
                ('masks', models.IntegerField(choices=[(0, '(Unknown)'), (10, 'Required'), (20, 'Optional'), (30, 'Disallowed')], default=0, null=True)),
                ('is_masks', models.BooleanField(default=True)),
                ('meeting_date', models.DateField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('cd_status', models.IntegerField(blank=True, choices=[(10, 'Active'), (20, 'Closed'), (30, 'Merged')], null=True)),
                ('cd_id', models.IntegerField(blank=True, null=True, unique=True)),
                ('nces_school_id', models.IntegerField(blank=True, null=True, unique=True)),
                ('district_name', models.CharField(blank=True, default='', max_length=255)),
                ('county_name', models.CharField(blank=True, default='', max_length=255)),
                ('address', models.CharField(blank=True, default='', max_length=255)),
                ('city', models.CharField(blank=True, default='', max_length=255)),
                ('state', models.CharField(blank=True, default='', max_length=255)),
                ('zipcode', models.CharField(blank=True, default='', max_length=255)),
                ('phone', models.CharField(blank=True, default='', max_length=255)),
                ('website', models.URLField(blank=True, default='')),
                ('soc', models.IntegerField(blank=True, choices=[(8, 'preschoolPreschool'), (9, 'specialeduSpecial Education Schools (Public)'), (10, 'countyCounty Community'), (11, 'yafYouth Authority Facilities (CEA)'), (13, 'opportunityOpportunity Schools'), (14, 'juvenileJuvenile Court Schools'), (15, 'otherOther County or District Programs'), (31, 'specialschoolState Special Schools'), (60, 'elementaryElementary School (Public)'), (61, 'elementary1Elementary School in 1 School District (Public)'), (62, 'intermediateIntermediate/Middle Schools (Public)'), (63, 'alternativeAlternative Schools of Choice'), (64, 'juniorJunior High Schools (Public)'), (65, 'k12K-12 Schools (Public)'), (66, 'highHigh Schools (Public)'), (67, 'high1High Schools in 1 School District (Public)'), (68, 'continuuationContinuation High Schools'), (69, 'communitydayDistrict Community Day Schools'), (70, 'adultAdult Education Centers'), (98, 'rocRegional Occupational Center/Program (ROC/P)')], null=True)),
                ('is_charter', models.BooleanField(default=False)),
                ('charter_number', models.IntegerField(blank=True, null=True)),
                ('funding_type', models.IntegerField(blank=True, choices=[(0, '(Unknown)'), (10, 'Direct Funding'), (20, 'Indirect Funding'), (30, 'Disallowed')], null=True)),
                ('edops_type', models.IntegerField(blank=True, choices=[(10, 'Alternative School of Choice'), (20, 'County Community School'), (30, 'Community Day School'), (40, 'Continuation School'), (50, 'Juvenile Court School'), (60, 'Opportunity School'), (70, 'Youth Authority School'), (80, 'State Special School'), (90, 'Special Education School'), (100, 'Traditional'), (110, 'Regional Occupational Program'), (120, 'Home and Hospital'), (130, 'District Consortia Special Education School')], null=True)),
                ('eil', models.IntegerField(blank=True, choices=[(10, 'Preschool'), (20, 'Elementary'), (30, 'Intermediate/Middle/Junior High'), (40, 'High School'), (50, 'Elementary-High Combination'), (60, 'Adult'), (70, 'Ungraded')], null=True)),
                ('grade_span', models.CharField(blank=True, max_length=255)),
                ('virutal_type', models.IntegerField(blank=True, choices=[(10, 'Exclusively Virutal'), (20, 'Primarily Virtual'), (30, 'Primarily Classroom'), (40, 'Not Virtual'), (50, 'Partial Virtual')], null=True)),
                ('is_magnet', models.BooleanField(default=False)),
                ('fed_nces_school_id', models.IntegerField(blank=True, null=True, unique=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=10, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=10, null=True)),
                ('admin_first_name', models.CharField(blank=True, default='', max_length=255)),
                ('admin_last_name', models.CharField(blank=True, default='', max_length=255)),
                ('admin_email', models.EmailField(blank=True, default='', max_length=255)),
            ],
        ),
    ]
