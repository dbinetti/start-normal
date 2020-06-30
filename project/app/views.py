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
from .models import District
from .models import Faq
from .models import Signature
from .models import User
from .tasks import build_email
from .tasks import mailchimp_subscribe_email
from .tasks import mailchimp_subscribe_signature
from .tasks import send_email
from .tasks import welcome_email


def login(request):
    redirect_uri = '{0}://{1}/callback'.format(
        request.scheme,
        request.get_host(),
    )
    print(redirect_uri)
    params = {
        'response_type': 'code',
        'client_id': settings.AUTH0_CLIENT_ID,
        'scope': 'openid',
        'redirect_uri': redirect_uri,
        'connection': 'Username-Password-Authentication',
    }
    url = requests.Request(
        'GET',
        'https://{0}/authorize'.format(settings.AUTH0_DOMAIN),
        params=params,
    ).prepare().url
    return redirect(url)


def callback(request):
    code = request.GET.get('code', '')
    json_header = {
        'content-type': 'application/json',
    }
    token_url = 'https://{0}/oauth/token'.format(
        settings.AUTH0_DOMAIN,
    )
    redirect_uri = '{0}://{1}/callback'.format(
        request.scheme,
        request.get_host(),
    )
    print(redirect_uri)
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
    logout_url = 'https://{0}/v2/logout'.format(settings.AUTH0_DOMAIN)
    return redirect(logout_url)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('account')
    else:
        form = UserCreationForm()
    return render(
        request,
        'registration/signup.html',
        {'form': form},
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
        'app/district.html',
        {'district': district, 'contacts': contacts},
    )

def account(request):
    return render(
        request,
        'app/account.html',
    )


def districts(request):
    districts = District.objects.order_by('name')
    return render(
        request,
        'app/districts.html',
        {'districts': districts},
    )


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
            user = user.save()

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
        'app/sign.html',
        {'form': form, 'signatures': signatures, 'progress': progress},
    )

def petition(request):
    signatures = Signature.objects.filter(
        is_approved=True,
    )
    progress = (signatures.count() / 5000) * 100
    return render(
        request,
        'app/petition.html',
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
        'app/signatures.html',
        {'signatures': signatures, 'progress': progress},
    )

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name='app/claim.html'
    form_class = CustomSetPasswordForm
    post_reset_login = True
    success_url = reverse_lazy('account')

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
        'app/signature.html',
        {'form': form, 'progress': progress, 'signatures': signatures},
    )

@login_required
def faq(request):
    faqs = Faq.objects.filter(
        is_active=True,
    ).order_by(
        'num',
        'created',
    )
    return render(
        request,
        'app/faq.html',
        {'faqs': faqs},
    )

@login_required
def delete(request):
    if request.method == "POST":
        form = DeleteForm(request.POST)
        if form.is_valid():
            user = request.user
            signature = user.signature
            signature.delete()
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
        'app/delete.html',
        {'form': form,},
    )

def index(request):
    return render(
        request,
        'app/index.html',
    )

def letter(request):
    return redirect('sign')

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
        'app/subscribe.html',
        {'form': form,},
    )

def thanks(request):
    return render(
        request,
        'app/thanks.html',
    )

def morrow(request):
    return render(
        request,
        'app/morrow.html',
    )

def about(request):
    return render(
        request,
        'app/about.html',
    )

def videos(request):
    return render(
        request,
        'app/videos.html',
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
        'app/thomas.html',
        {'form': form,},
    )

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
        'app/report.html',
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
        'app/notes.html',
        {'signatures': signatures},
    )
