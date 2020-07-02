# Django
# Standard Library
import json

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
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.urls import reverse_lazy

# First-Party
import django_rq
import requests
import shortuuid
from django_rq import job

# Local
from .forms import AccountForm
from .forms import CustomSetPasswordForm
from .forms import DeleteForm
from .forms import RegistrationForm
from .forms import SignatureForm
from .forms import SubscribeForm
from .forms import UserCreationForm
from .models import Account
from .models import District
from .models import Faq
from .models import Signature
from .models import User
from .tasks import build_email
from .tasks import mailchimp_subscribe_email
from .tasks import mailchimp_subscribe_signature
from .tasks import send_email
from .tasks import welcome_email


# Public
def index(request):
    return render(
        request,
        'public/index.html',
    )

def morrow(request):
    return render(
        request,
        'public/morrow.html',
    )

def about(request):
    return render(
        request,
        'public/about.html',
    )

def videos(request):
    return render(
        request,
        'public/videos.html',
    )

def thomas(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save()
            # email = form.cleaned_data.get('email')
            messages.success(
                request,
                'You have registered for the Q&A with Thomas Albeck!',
            )
            # registration_email.delay(signature)
    else:
        form = RegistrationForm()
    return render(
        request,
        'public/thomas.html',
        {'form': form,},
    )

def district(request, short):
    district = District.objects.get(
        short__iexact=short,
    )
    contacts = district.contacts.filter(
        is_active=True,
    ).order_by(
        'role',
    )
    return render(
        request,
        'public/district.html',
        {'district': district, 'contacts': contacts},
    )

def districts(request):
    districts = District.objects.order_by('name')
    return render(
        request,
        'public/districts.html',
        {'districts': districts},
    )

def petition(request):
    signatures = Signature.objects.filter(
        is_approved=True,
    )
    progress = (signatures.count() / 5000) * 100
    return render(
        request,
        'public/petition.html',
        {'signatures': signatures, 'progress': progress},
    )

def signatures(request):
    signatures = Signature.objects.filter(
        is_approved=True,
    ).order_by(
        '-is_public',
        'location',
        'created',
    )
    progress = (signatures.count() / 5000) * 100
    return render(
        request,
        'public/signatures.html',
        {'signatures': signatures, 'progress': progress},
    )

def subscribe(request):
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
        'public/subscribe.html',
        {'form': form,},
    )

def faq(request):
    faqs = Faq.objects.filter(
        is_active=True,
    ).order_by(
        'num',
        'created',
    )
    return render(
        request,
        'public/faq.html',
        {'faqs': faqs},
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
        'client_secret': settings.AUTH0_SECRET,
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
    user_info = requests.get(user_url).json()
    username = user_info['sub']

    user = authenticate(username=username)
    if user:
        log_in(request, user)
        return redirect('index')
    return HttpResponse(status=400)

def logout(request):
    log_out(request)
    params = {
        'client_id': settings.AUTH0_CLIENT_ID,
        'return_to': request.build_absolute_uri('goodbye'),
    }
    logout_url = requests.Request(
        'GET',
        'https://{0}/v2/logout'.format(settings.AUTH0_DOMAIN),
        params=params,
    ).prepare().url
    return redirect(logout_url)

def goodbye(request):
    return render(
        request,
        'private/goodbye.html',
    )

# Private
def sign(request):
    if request.user.is_authenticated:
        return redirect('account')
    if request.method == "POST":
        form = SignatureForm(request.POST)
        if form.is_valid():
            # Instantiate Signature object
            signature = form.save(commit=False)
            # Create related user account
            email = form.cleaned_data.get('email')
            password = shortuuid.uuid()
            user = User(
                email=email,
                password=password,
                is_active=True,
            )
            user.save()
            user.refresh_from_db()
            # Relate records and save
            signature.user = user
            signature.save()
            # Notify User through UI
            messages.success(
                request,
                'Your Signature has been added to the Petition.',
            )
            # Execute related tasks
            welcome_email.delay(signature)
            mailchimp_subscribe_signature.delay(signature)
            # Forward to share page
            return redirect('thanks')
    else:
        form = SignatureForm()
    signatures = Signature.objects.filter(
        is_approved=True,
    ).order_by(
        '-is_public',
        'location',
        'created',
    )
    progress = (signatures.count() / 5000) * 100
    return render(
        request,
        'public/sign.html',
        {'form': form, 'signatures': signatures, 'progress': progress},
    )

@login_required
def account(request):
    user = request.user
    account = Account.objects.get(
        user=user,
    )
    if request.method == "POST":
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Saved!",
            )
    else:
        form = AccountForm(instance=account)
    return render(
        request,
        'private/account.html', {
            'form': form,
        },
    )

@login_required
def signature(request):
    user = request.user
    signature = Signature.objects.get(
        user=user,
    )
    if request.method == "POST":
        form = AccountForm(request.POST, instance=signature)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Saved!",
            )
    else:
        form = AccountForm(instance=signature)
    signatures = Signature.objects.filter(
        is_approved=True,
    )
    progress = (signatures.count() / 5000) * 100
    return render(
        request,
        'private/signature.html',
        {'form': form, 'progress': progress, 'signatures': signatures},
    )

@login_required
def delete(request):
    if request.method == "POST":
        form = DeleteForm(request.POST)
        if form.is_valid():
            user = request.user
            user.is_active = False
            user.save()
            messages.error(
                request,
                "Account Deleted!",
            )
            return redirect('index')
    else:
        form = DeleteForm()
    return render(
        request,
        'private/delete.html',
        {'form': form,},
    )

@login_required
def thanks(request):
    return render(
        request,
        'private/thanks.html',
    )

# Admin
@staff_member_required
def report(request):
    report = Signature.objects.order_by(
        'location',
    ).values(
        'location',
    ).annotate(
        c=Count('id'),
    )
    total = Signature.objects.aggregate(
        c=Count('id'),
    )['c']
    return render(
        request,
        'staff/report.html',
        {'report': report, 'total': total},
    )

@staff_member_required
def notes(request):
    signatures = Signature.objects.exclude(
        notes="",
    ).exclude(
        notes=None,
    ).order_by('-id')
    return render(
        request,
        'staff/notes.html',
        {'signatures': signatures},
    )
