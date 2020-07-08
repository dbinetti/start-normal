# Generated by Django 3.0.8 on 2020-07-08 14:20

import app.models
import autoslug.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import hashid_field.field
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text="Real name strongly encouraged.  However, if necessary use a descriptor like 'Concerned Parent' or 'Father of Two'. (Required)", max_length=255)),
                ('email', models.EmailField(help_text="Your email is private and not shared.  It's used to manage preferences and send adminstrative updates. (Required)", max_length=254, unique=True)),
                ('location', models.CharField(blank=True, choices=[('ath', 'Atherton'), ('bel', 'Belmont'), ('brb', 'Brisbane'), ('bur', 'Burlingame'), ('col', 'Colma'), ('dc', 'Daly City'), ('epa', 'East Palo Alto'), ('fc', 'Foster City'), ('hmb', 'Half Moon Bay'), ('hil', 'Hillsborough'), ('mp', 'Menlo Park'), ('mil', 'Millbrae'), ('pac', 'Pacifica'), ('pv', 'Portola Valley'), ('rc', 'Redwood City'), ('sb', 'San Bruno'), ('sc', 'San Carlos'), ('sm', 'San Mateo'), ('ssf', 'South San Francisco'), ('ws', 'Woodside'), ('un', 'Unincorporated San Mateo County'), ('out', 'Outside of San Mateo County')], help_text='Your city. (Required)', max_length=255)),
                ('phone', models.CharField(blank=True, help_text='Your mobile phone. (Optional)', max_length=255)),
                ('is_volunteer', models.BooleanField(default=False, help_text="If you're willing to volunteer please check this box.")),
                ('is_teacher', models.BooleanField(default=False, help_text="If you're an educator please check this box.")),
                ('is_doctor', models.BooleanField(default=False, help_text="If you're a physician please check this box.")),
                ('notes', models.TextField(blank=True, default='', help_text='Feel free to include private notes just for us.', max_length=512)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='account', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('text', models.TextField(blank=True)),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=False, max_length=255, populate_from=app.models.get_populate_from, unique=True)),
                ('status', models.IntegerField(choices=[(10, 'Active'), (20, 'Closed'), (30, 'Merged')], default=10)),
                ('kind', models.IntegerField(blank=True, choices=[('District', [(400, 'County Office of Education'), (402, 'State Board of Education'), (403, 'Statewide Benefit Charter'), (431, 'State Special Schools'), (434, 'Non-school Location*'), (442, 'Joint Powers Authority (JPA)'), (452, 'Elementary School District'), (454, 'Unified School District'), (456, 'High School District'), (458, 'Community College District'), (498, 'Regional Occupational Center/Program (ROC/P)'), (499, 'Administration Only')]), ('School', [(510, 'Preschool'), (520, 'Elementary'), (530, 'Intermediate/Middle/Junior High'), (540, 'High School'), (550, 'Elementary-High Combination'), (560, 'Adult'), (570, 'Ungraded')])], null=True)),
                ('nces_id', models.IntegerField(blank=True, null=True, unique=True)),
                ('address', models.CharField(blank=True, default='', max_length=255)),
                ('city', models.CharField(blank=True, default='', max_length=255)),
                ('state', models.CharField(blank=True, default='', max_length=255)),
                ('zipcode', models.CharField(blank=True, default='', max_length=255)),
                ('county', models.CharField(blank=True, max_length=255)),
                ('phone', models.CharField(blank=True, default='', max_length=255)),
                ('website', models.URLField(blank=True, default='')),
                ('lat', models.DecimalField(blank=True, decimal_places=6, max_digits=10, null=True)),
                ('lon', models.DecimalField(blank=True, decimal_places=6, max_digits=10, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='app.Department')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, max_length=255, populate_from=app.models.get_populate_from, unique=True)),
                ('status', models.IntegerField(choices=[(10, 'Active'), (20, 'Closed'), (30, 'Merged')], default=10)),
                ('cd_id', models.IntegerField(unique=True)),
                ('nces_district_id', models.IntegerField(unique=True)),
                ('county', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('zipcode', models.CharField(max_length=255)),
                ('phone', models.CharField(blank=True, default='', max_length=255)),
                ('website', models.URLField(blank=True, default='')),
                ('doc', models.IntegerField(choices=[(0, 'County Office of Education'), (2, 'State Board of Education'), (3, 'Statewide Benefit Charter'), (31, 'State Special Schools'), (34, 'Non-school Location*'), (42, 'Joint Powers Authority (JPA)'), (52, 'Elementary School District'), (54, 'Unified School District'), (56, 'High School District'), (58, 'Community College District'), (98, 'Regional Occupational Center/Program (ROC/P)'), (99, 'Administration Only')])),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=10, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=10, null=True)),
                ('admin_first_name', models.CharField(blank=True, default='', max_length=255)),
                ('admin_last_name', models.CharField(blank=True, default='', max_length=255)),
                ('admin_email', models.EmailField(blank=True, default='', max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('num', models.IntegerField(default=50)),
                ('question', models.CharField(max_length=255)),
                ('answer', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Signature',
            fields=[
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('status', models.IntegerField(choices=[(0, 'New'), (10, 'Signed'), (20, 'Removed')], default=0)),
                ('name', models.CharField(help_text="Real name strongly encouraged.  However, if necessary use a descriptor like 'Concerned Parent' or 'Father of Two'. (Required)", max_length=255)),
                ('is_approved', models.BooleanField(default=False)),
                ('is_public', models.BooleanField(default=False, help_text='List My Name on the Website.')),
                ('message', models.TextField(blank=True, default='', help_text='Feel free to include a public message attached to your signature.', max_length=512)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='signatures', to='app.Account')),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='signatures', to='app.Department')),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, max_length=255, populate_from=app.models.get_populate_from, unique=True)),
                ('status', models.IntegerField(choices=[(10, 'Active'), (20, 'Closed'), (30, 'Merged')], default=10)),
                ('cd_id', models.IntegerField(unique=True)),
                ('nces_school_id', models.IntegerField(unique=True)),
                ('county', models.CharField(default='', max_length=255)),
                ('address', models.CharField(default='', max_length=255)),
                ('city', models.CharField(default='', max_length=255)),
                ('state', models.CharField(default='', max_length=255)),
                ('zipcode', models.CharField(default='', max_length=255)),
                ('phone', models.CharField(blank=True, default='', max_length=255)),
                ('website', models.URLField(blank=True, default='')),
                ('soc', models.IntegerField(choices=[(8, 'Preschool'), (9, 'Special Education Schools (Public)'), (10, 'County Community'), (11, 'Youth Authority Facilities (CEA)'), (13, 'Opportunity Schools'), (14, 'Juvenile Court Schools'), (15, 'Other County or District Programs'), (31, 'State Special Schools'), (60, 'Elementary School (Public)'), (61, 'Elementary School in 1 School District (Public)'), (62, 'Intermediate/Middle Schools (Public)'), (63, 'Alternative Schools of Choice'), (64, 'Junior High Schools (Public)'), (65, 'K-12 Schools (Public)'), (66, 'High Schools (Public)'), (67, 'High Schools in 1 School District (Public)'), (68, 'Continuation High Schools'), (69, 'District Community Day Schools'), (70, 'Adult Education Centers'), (98, 'Regional Occupational Center/Program (ROC/P)')])),
                ('is_charter', models.BooleanField(default=False)),
                ('charter_number', models.IntegerField(blank=True, null=True)),
                ('funding', models.IntegerField(blank=True, choices=[(0, '(Unknown)'), (10, 'Direct Funding'), (20, 'Indirect Funding'), (30, 'Disallowed')], null=True)),
                ('edops', models.IntegerField(blank=True, choices=[(10, 'Alternative School of Choice'), (20, 'County Community School'), (30, 'Community Day School'), (40, 'Continuation School'), (50, 'Juvenile Court School'), (60, 'Opportunity School'), (70, 'Youth Authority School'), (80, 'State Special School'), (90, 'Special Education School'), (100, 'Traditional'), (110, 'Regional Occupational Program'), (120, 'Home and Hospital'), (130, 'District Consortia Special Education School')], null=True)),
                ('eil', models.IntegerField(blank=True, choices=[(10, 'Preschool'), (20, 'Elementary'), (30, 'Intermediate/Middle/Junior High'), (40, 'High School'), (50, 'Elementary-High Combination'), (60, 'Adult'), (70, 'Ungraded')], null=True)),
                ('grades', models.CharField(blank=True, default='', max_length=255)),
                ('virtual', models.IntegerField(blank=True, choices=[(10, 'Exclusively Virutal'), (20, 'Primarily Virtual'), (30, 'Primarily Classroom'), (40, 'Not Virtual'), (50, 'Partial Virtual')], null=True)),
                ('is_magnet', models.BooleanField(default=False)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=10, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=10, null=True)),
                ('admin_first_name', models.CharField(blank=True, default='', max_length=255)),
                ('admin_last_name', models.CharField(blank=True, default='', max_length=255)),
                ('admin_email', models.EmailField(blank=True, default='', max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schools', to='app.District')),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=255)),
                ('role', models.IntegerField(blank=True, choices=[(410, 'Superintendent'), (420, 'Board President'), (430, 'Board Vice-President'), (440, 'Board Clerk'), (450, 'Board Trustee'), (510, 'Principal')], null=True)),
                ('email', models.CharField(blank=True, default='', max_length=255)),
                ('phone', models.CharField(blank=True, default='', max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contacts', to='app.Department')),
            ],
        ),
    ]
