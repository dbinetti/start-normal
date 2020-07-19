# Django
# Standard Library
import json

from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as log_in
from django.contrib.auth import logout as log_out
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import PasswordResetConfirmView
from django.core.mail import EmailMessage
from django.db.models import Count
from django.db.models import Q
from django.db.models import Sum
from django.dispatch import receiver
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.urls import reverse_lazy

# First-Party
import django_rq
import requests
import shortuuid
from auth0.v3.authentication import Database
from auth0.v3.authentication import Logout
from auth0.v3.exceptions import Auth0Error
from dal import autocomplete
from django_rq import job

# Local
from .forms import AccountForm
from .forms import ContactForm
from .forms import DeleteForm
from .forms import ReportForm
from .forms import SignupForm
from .forms import StudentFormSet
from .forms import SubscribeForm
from .forms import TeacherForm
from .forms import UserCreationForm
from .models import Account
from .models import Contact
from .models import District
from .models import Parent
from .models import Report
from .models import School
from .models import Student
from .models import Teacher
from .models import User
from .tasks import build_email
from .tasks import mailchimp_create_or_update_from_account
from .tasks import mailchimp_subscribe_email
from .tasks import send_email


# Root
def index(request):
    return render(
        request,
        'app/index.html',
        context = {
            'app_id': settings.ALGOLIA['APPLICATION_ID'],
            'search_key': settings.ALGOLIA['SEARCH_KEY'],
            'index_name': "School_{0}".format(settings.ALGOLIA['INDEX_SUFFIX']),
        }
    )

def about(request):
    return render(
        request,
        'app/about.html',
    )

def faq(request):
    return render(
        request,
        'app/faq.html',
    )

def team(request):
    return render(
        request,
        'app/team.html',
    )

def privacy(request):
    return render(
        request,
        'app/privacy.html',
    )


# Account
@login_required
def account(request):
    StudentFormSet.extra = 0
    user = request.user
    account = Account.objects.get(
        user=user,
    )
    parent = getattr(user, 'parent', None)
    teacher = getattr(user, 'teacher', None)
    if request.method == "POST":
        form = AccountForm(
            request.POST,
            instance=account,
            prefix='account',
        )
        formset = StudentFormSet(
            request.POST,
            request.FILES,
            instance=parent,
            prefix='students',
        )
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(
                request,
                "Saved!",
            )
            return redirect('account')
    else:
        form = AccountForm(
            instance=account,
            prefix='account',
        )
        formset = StudentFormSet(
            instance=parent,
            prefix='students',
        )
    return render(
        request,
        'app/account/account.html', {
            'user': user,
            'form': form,
            'formset': formset,
        },
    )

@login_required
def pending(request):
    return render(
        request,
        'app/account/pending.html',
    )

@login_required
def split(request):
    return render(
        request,
        'app/account/split.html',
    )

@login_required
def welcome_teacher(request):
    user = request.user
    teacher, created = Teacher.objects.get_or_create(
        user=user,
    )
    if request.method == "POST":
        form = TeacherForm(
            request.POST,
            instance=teacher,
        )
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Saved!",
            )
            return redirect('share')
    else:
        form = TeacherForm(
            instance=teacher,
        )
    return render(
        request,
        'app/account/welcome_teacher.html',
        context = {
            'form': form,
        }
    )

@login_required
def welcome_parent(request):
    StudentFormSet.extra = 5
    user = request.user
    try:
        success = request.GET.__getitem__('success')
    except:
        success = ''
    if success == 'true':
        user.is_active = True
        user.save()

    parent, created = Parent.objects.get_or_create(
        user=user,
    )
    account = user.account

    if request.method == "POST":
        formset = StudentFormSet(
            request.POST,
            request.FILES,
            instance=parent,
        )
        if formset.is_valid():
            formset.save()
            messages.success(
                request,
                "Saved!",
            )
            return redirect('share')
    else:
        formset = StudentFormSet(
            instance=parent,
        )
    return render(
        request,
        'app/account/welcome_parent.html',
        context = {
            'formset': formset,
        },
    )

@login_required
def share(request):
    return render(
        request,
        'app/account/share.html',
    )

@login_required
def delete(request):
    if request.method == "POST":
        form = DeleteForm(request.POST)
        if form.is_valid():
            user = request.user
            user.delete()
            messages.error(
                request,
                "Account Deleted!",
            )
            return redirect('index')
    else:
        form = DeleteForm()
    return render(
        request,
        'app/account/delete.html',
        {'form': form,},
    )



# Authentication
def login(request):
    redirect_uri = request.build_absolute_uri('callback')
    params = {
        'response_type': 'code',
        'client_id': settings.AUTH0_CLIENT_ID,
        'scope': 'openid profile email',
        'redirect_uri': redirect_uri,
    }
    url = requests.Request(
        'GET',
        'https://{0}/authorize'.format(settings.AUTH0_DOMAIN),
        params=params,
    ).prepare().url
    return redirect(url)

def callback(request):
    code = request.GET.get('code', '')
    if not code:
        return HttpResponse(status=400)
    json_header = {
        'content-type': 'application/json',
    }
    token_url = 'https://{0}/oauth/token'.format(
        settings.AUTH0_DOMAIN,
    )
    redirect_uri = request.build_absolute_uri('callback')
    token_payload = {
        'client_id': settings.AUTH0_CLIENT_ID,
        'client_secret': settings.AUTH0_CLIENT_SECRET,
        'redirect_uri': redirect_uri,
        'code': code,
        'grant_type': 'authorization_code'
    }
    token_info = requests.post(
        token_url,
        data=json.dumps(token_payload),
        headers=json_header
    ).json()
    user_url = 'https://{0}/userinfo?access_token={1}'.format(
        settings.AUTH0_DOMAIN,
        token_info.get('access_token', ''),
    )
    payload = requests.get(user_url).json()
    # format payload key
    payload['username'] = payload.pop('sub')
    request.session['user'] = payload
    user = authenticate(request, **payload)
    if user:
        log_in(request, user)
        return redirect('split')
    return HttpResponse(status=400)

def logout(request):
    log_out(request)
    params = {
        'client_id': settings.AUTH0_CLIENT_ID,
        'return_to': request.build_absolute_uri('index'),
    }
    logout_url = requests.Request(
        'GET',
        'https://{0}/v2/logout'.format(settings.AUTH0_DOMAIN),
        params=params,
    ).prepare().url
    messages.success(
        request,
        "You Have Been Logged Out!",
    )
    return redirect(logout_url)


# Autocomplete
class SchoolAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = School.objects.filter(
        )

        if self.q:
            # qs = qs.filter(slug__icontains=self.q)
            qs = qs.filter(
                Q(name__icontains=self.q)|
                Q(city__icontains=self.q) |
                Q(state__icontains=self.q)
            )

        return qs

# Informed
def informed(request):
    if request.method == "POST":
        form = SubscribeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            mailchimp_subscribe_email.delay(email=email)
            messages.success(
                request,
                'You have been subscribed.',
            )
            return redirect('index')
    else:
        form = SubscribeForm()
    return render(
        request,
        'app/informed/informed.html',
        context = {
            'form': form,
            'app_id': settings.ALGOLIA['APPLICATION_ID'],
            'search_key': settings.ALGOLIA['SEARCH_KEY'],
            'index_name': "School_{0}".format(settings.ALGOLIA['INDEX_SUFFIX']),
        },
    )

# # Admin
# @staff_member_required
# def report(request):
#     report = Affiliation.objects.order_by(
#         'school',
#     ).values(
#         'school',
#     ).annotate(
#         c=Count('id'),
#     )
#     total = Affiliation.objects.aggregate(
#         c=Count('id'),
#     )['c']
#     return render(
#         request,
#         'app/admin/report.html',
#         {'report': report, 'total': total},
#     )



# Involved
# def involved(request):a
#     user = request.user
#     # Account Holder
#     if user.is_authenticated:
#         districts = District.objects.filter(
#             schools__students__user=user,
#         ).distinct()
#         # If they have selected students
#         if districts:
#             return render(
#                 request,
#                 'app/involved/involved.html',
#                 context={
#                     'districts': districts,
#                 },
#             )
#         # Otherwise, pick students
#         else:
#             StudentFormSet.extra = 5
#             if request.method == "POST":
#                 formset = StudentFormSet(
#                     request.POST,
#                     request.FILES,
#                     instance=user,
#                 )
#                 if formset.is_valid():
#                     formset.save()
#                     messages.success(
#                         request,
#                         "Saved!",
#                     )
#                     return redirect('involved')
#             else:
#                 formset = StudentFormSet(
#                     instance=user,
#                 )
#             return render(
#                 request,
#                 'app/involved/involved.html',
#                 context = {
#                     'formset': formset,
#                 },
#             )
#     else:
#         form = SignupForm(request.POST or None)
#         if form.is_valid():
#             # Instantiate Variables
#             name = form.cleaned_data['name']
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             is_public = form.cleaned_data['is_public']
#             is_subscribe = form.cleaned_data['is_subscribe']
#             message = form.cleaned_data['message']

#             # Auth0 Signup
#             auth0_client = Database(settings.AUTH0_DOMAIN)
#             try:
#                 auth0_user = auth0_client.signup(
#                     client_id=settings.AUTH0_CLIENT_ID,
#                     name=name,
#                     email=email,
#                     password=password,
#                     connection='Username-Password-Authentication',
#                 )
#             except Auth0Error as e:
#                 if e.error_code == 'user_exists':
#                     messages.warning(
#                         request,
#                         "That email is in use.  Try to login (upper right corner) or pick a different email.",
#                     )
#                     return redirect('involved')
#             # Create User
#             username = "auth0|{0}".format(auth0_user['_id'])

#             user = authenticate(
#                 request,
#                 username=username,
#                 email=email,
#                 name=name,
#             )
#             user.refresh_from_db()
#             account = user.account
#             account.is_public = is_public
#             account.is_subscribe = is_subscribe
#             account.message = message
#             account.save()
#             log_in(request, user)
#             return redirect('pending')
#         return render(
#             request,
#             'app/involved/involved.html',
#             context={
#                 'form': form,
#             },
#         )

def school(request, slug):
    school = School.objects.get(slug=slug)
    parents = User.objects.filter(students__school=school).distinct()
    for parent in parents:
        parent.grades = ", ".join([x.get_grade_display() for x in parent.students.filter(
        school=school).order_by('grade')])
    reports = Report.objects.filter(
        status=Report.STATUS.approved,
        transmissions__school=school,
    ).order_by('-created')
    contacts = Contact.objects.filter(
        is_active=True,
        entries__school=school,
    ).order_by('role')
    return render(
        request,
        'app/involved/school.html',
        context={
            'school': school,
            'reports': reports,
            'contacts': contacts,
            'parents': parents,
        },
    )

def schools(request):
    user = request.user
    if user.is_authenticated:
        schools = School.objects.filter(
            students__user=user,
        ).order_by(
            'grade',
            'school',
        ).distinct()
    else:
        schools = None
    return render(
        request,
        'app/involved/schools.html',
        context={
            'schools': schools,
            'app_id': settings.ALGOLIA['APPLICATION_ID'],
            'search_key': settings.ALGOLIA['SEARCH_KEY'],
            'index_name': "School_{0}".format(settings.ALGOLIA['INDEX_SUFFIX']),
        },
    )

def district(request, slug):
    district = District.objects.get(slug=slug)
    parents = User.objects.filter(
        students__school__isnull=False,
    ).distinct()
    for parent in parents:
        parent.schools = ", ".join(
            ["{0} {1}".format(x.school.name, x.get_grade_display()) for x in parent.students.filter(
                school__district=district,
            ).order_by('grade')]
        )
    reports = Report.objects.filter(
        district=district,
        status=Report.STATUS.approved,
    ).order_by('-created')
    contacts = Contact.objects.filter(
        is_active=True,
        district=district,
    ).order_by('role')
    return render(
        request,
        'app/involved/district.html',
        context={
            'district': district,
            'reports': reports,
            'contacts': contacts,
            'parents': parents,
        },
    )

def districts(request):
    user = request.user
    if user.is_authenticated:
        districts = District.objects.filter(
            school__students__user=user,
        ).distinct()
    else:
        districts = None
    return render(
        request,
        'app/involved/districts.html',
        context={
            'districts': districts,
            'app_id': settings.ALGOLIA['APPLICATION_ID'],
            'search_key': settings.ALGOLIA['SEARCH_KEY'],
            'index_name': "District_{0}".format(settings.ALGOLIA['INDEX_SUFFIX']),
        },
    )


@login_required
def district_report(request, slug):
    user = request.user
    district = District.objects.get(slug=slug)
    form = ReportForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.district = district
        instance.user = user
        instance.save()
        messages.success(
            request,
            "Report Submitted!",
        )
        return redirect('district', slug)
    return render(
        request,
        'app/involved/report.html',
        {'form': form,},
    )

@login_required
def district_contact(request, slug):
    user = request.user
    district = District.objects.get(slug=slug)
    form = ContactForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.district = district
        instance.save()
        messages.success(
            request,
            "Contact Submitted!",
        )
        return redirect('district', slug)
    return render(
        request,
        'app/involved/contact.html',
        {'form': form,},
    )






def morrow(request):
    return render(
        request,
        'app/informed/morrow.html',
    )

def thomas(request):
    return render(
        request,
        'app/informed/thomas.html',
    )
