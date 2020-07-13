# Django
# Standard Library
import json

# Third-Party
import django_rq
import requests
import shortuuid
from auth0.v3.authentication import Database
from auth0.v3.authentication import Logout
from auth0.v3.exceptions import Auth0Error
from dal import autocomplete
from django_rq import job

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
from django.db.models import Sum
from django.dispatch import receiver
from django.forms import formset_factory
from django.forms.models import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.urls import reverse_lazy

# Local
from .forms import AccountForm
from .forms import AffiliationForm
from .forms import DeleteForm
from .forms import RemoveForm
from .forms import SignExistingForm
from .forms import SignForm
from .forms import SignupForm
from .forms import StudentForm
from .forms import SubscribeForm
from .forms import UserCreationForm
from .models import Account
from .models import Affiliation
from .models import Organization
from .models import Student
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
    )

def about(request):
    return render(
        request,
        'app/about.html',
    )

def robots(request):
    return render(
        request,
        'app/robots.txt',
    )


# Involved
def involved(request):
    # New Signup
    form = SignupForm(request.POST or None)
    if form.is_valid():
        # Instantiate Variables
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        is_public = form.cleaned_data['is_public']
        is_subscribe = form.cleaned_data['is_subscribe']
        message = form.cleaned_data['message']

        # Auth0 Signup
        auth0_client = Database(settings.AUTH0_DOMAIN)
        try:
            auth0_user = auth0_client.signup(
                client_id=settings.AUTH0_CLIENT_ID,
                name=name,
                email=email,
                password=password,
                connection='Username-Password-Authentication',
            )
        except Auth0Error as e:
            if e.error_code == 'user_exists':
                messages.warning(
                    request,
                    "That email is in use.  Try to login (upper right corner) or pick a different email.",
                )
                return redirect('involved')
        # Create User
        username = "auth0|{0}".format(auth0_user['_id'])

        user = authenticate(
            request,
            username=username,
            email=email,
            name=name,
        )
        user.refresh_from_db()
        account = user.account
        account.is_public = is_public
        account.is_subscribe = is_subscribe
        account.message = message
        account.save()
        log_in(request, user)
        return redirect('pending')
    return render(
        request,
        'app/involved/involved.html',
        context={
            'form': form,
        },
    )

def organization(request, slug):
    user = request.user
    organization = Organization.objects.get(slug=slug)
    affiliations = organization.affiliations.filter(
        status=Affiliation.STATUS.signed,
    ).order_by('-created')
    try:
        affiliation = organization.affiliations.get(user=user)
    except Exception:
        # Anonymous
        affiliation = None
    except Affiliation.DoesNotExist:
        affiliation = None
    if user.is_authenticated:
        if affiliation:
            form = None
        else:
            if request.method == "POST":
                form = SignExistingForm(request.POST)
                if form.is_valid():
                    form.status = Affiliation.STATUS.signed
                    form.save()
                    messages.success(
                        request,
                        "Your Affiliation has been Saved!",
                    )
                    return redirect('account')
            else:
                form = SignExistingForm(initial={
                    'organization': organization,
                    'user': user,
                })
    else:
        # New Signup
        form = SignupForm(request.POST or None)
        if form.is_valid():
            # Instantiate Variables
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            is_public = form.cleaned_data['is_public']
            is_subscribe = form.cleaned_data['is_subscribe']
            message = form.cleaned_data['message']

            # Auth0 Signup
            auth0_client = Database(settings.AUTH0_DOMAIN)
            try:
                auth0_user = auth0_client.signup(
                    client_id=settings.AUTH0_CLIENT_ID,
                    name=name,
                    email=email,
                    password=password,
                    connection='Username-Password-Authentication',
                )
            except Auth0Error as e:
                if e.error_code == 'user_exists':
                    messages.warning(
                        request,
                        "That email is in use.  Try to login (upper right corner.)",
                    )
                    return render(
                        request,
                        'app/involved/organization.html',
                        context={
                            'organization': organization,
                            'form': form,
                        },
                    )
            # Create User
            username = "auth0|{0}".format(auth0_user['_id'])

            user = authenticate(
                request,
                username=username,
                email=email,
                name=name,
            )
            user.refresh_from_db()
            account = user.account
            account.is_public = is_public
            account.is_subscribe = is_subscribe
            account.save()

            # Create Affiliation
            affiliation = Affiliation.objects.create(
                status=Affiliation.STATUS.signed,
                message=message,
                user=user,
                organization=organization,
            )
            log_in(request, user)
            messages.success(
                request,
                "Your Affiliation has Been Added to the Organization!",
            )
            return redirect('pending')
    affiliations.count = 100
    return render(
        request,
        'app/involved/organization.html',
        context={
            'organization': organization,
            'form': form,
            'affiliation': affiliation,
            'affiliations': affiliations,
        },
    )

@login_required
def affiliation(request, id):
    affiliation = Affiliation.objects.get(
        id=id,
    )
    organization = affiliation.organization
    if request.method == "POST":
        form = AffiliationForm(request.POST, instance=affiliation)
        if form.is_valid():
            affiliation.save()
            messages.success(
                request,
                "Affiliation Saved!",
            )
            return redirect('account')
    else:
        form = AffiliationForm(instance=affiliation)
    return render(
        request,
        'app/involved/affiliation.html',
        context = {
            'organization': organization,
            'affiliation': affiliation,
            'form': form,
        },
    )


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


# Account
@login_required
def account(request):
    user = request.user
    account = Account.objects.get(
        user=user,
    )
    students = user.students.order_by('grade')

    StudentFormSet = inlineformset_factory(
        User,
        Student,
        fields=[
            'grade',
            'organization',
            'user',
        ],
        widgets = {
            'organization': autocomplete.ModelSelect2(
                url='school-search',
                attrs={
                    'data-container-css-class': '',
                    'data-close-on-select': 'false',
                    'data-scroll-after-select': 'true',
                },
            )
        },
        extra=0,
        # max_num=5,
        can_delete=True,
    )

    if request.method == "POST":
        form = AccountForm(
            request.POST,
            instance=account,
            prefix='account',
        )
        formset = StudentFormSet(
            request.POST,
            request.FILES,
            instance=user,
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
            instance=user,
            prefix='students',
        )
    return render(
        request,
        'app/account/account.html', {
            'user': user,
            'form': form,
            'formset': formset,
            'students': students,
        },
    )


@login_required
def pending(request):
    return render(
        request,
        'app/account/pending.html',
    )

class SchoolAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        qs = Organization.objects.filter(kind__gt=500)

        if self.q:
            qs = qs.filter(slug__icontains=self.q)

        return qs

@login_required
def student(request, id):
    student = Student.objects.get(id=id)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Student detail saved!',
            )
            return redirect('account')
    else:
        form = StudentForm(instance=student)
    return render(
        request,
        'app/account/student.html',
        {'form': form,},
    )


@login_required
def student_add(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Student added!',
            )
            return redirect('account')
    else:
        form = StudentForm()
    return render(
        request,
        'app/account/student.html',
        {'form': form,},
    )

@login_required
def student_remove(request, id):
    student = Student.objects.get(id=id)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Student detail saved!',
            )
            return redirect('account')
    else:
        form = StudentForm(instance=student)
    return render(
        request,
        'app/account/student_remove.html',
        {'form': form,},
    )

@login_required
def welcome(request):
    user = request.user
    try:
        success = request.GET.__getitem__('success')
    except:
        success = ''
    if success == 'true':
        user.is_active = True
        user.save()

    StudentFormSet = inlineformset_factory(
        User,
        Student,
        fields=[
            'grade',
            'organization',
            'user',
        ],
        widgets = {
            'organization': autocomplete.ModelSelect2(
                url='school-search',
                attrs={
                    'data-container-css-class': '',
                    'data-close-on-select': 'false',
                    'data-scroll-after-select': 'true',
                },
            )
        },
        # extra=0,
        # max_num=5,
    )
    if request.method == "POST":
        formset = StudentFormSet(
            request.POST,
            request.FILES,
            instance=user,
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
            instance=user,
        )
    return render(
        request,
        'app/account/welcome.html',
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
        return redirect('account')
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

# Admin
@staff_member_required
def report(request):
    report = Affiliation.objects.order_by(
        'organization',
    ).values(
        'organization',
    ).annotate(
        c=Count('id'),
    )
    total = Affiliation.objects.aggregate(
        c=Count('id'),
    )['c']
    return render(
        request,
        'app/admin/report.html',
        {'report': report, 'total': total},
    )
