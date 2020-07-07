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
from auth0.v3.authentication import Database
from auth0.v3.authentication import Logout
from django_rq import job

# Local
from .forms import AccountForm
from .forms import DeleteForm
from .forms import RemoveForm
from .forms import SignatureForm
from .forms import SignupForm
from .forms import SubscribeForm
from .forms import UserCreationForm
from .models import Account
from .models import District
from .models import Faq
from .models import Petition
from .models import Signature
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

def robots(request):
    return render(
        request,
        'app/robots.txt',
    )


# Involved
def district(request, slug):
    district = District.objects.get(
        slug__iexact=slug,
    )
    contacts = district.contacts.filter(
        is_active=True,
    ).order_by(
        'role',
    )
    petitions = district.petitions.all(
    ).order_by(
        'created',
    )
    return render(
        request,
        'app/involved/district.html', {
            'district': district,
            'contacts': contacts,
            'petitions': petitions,
        },
    )

def involved(request):
    ALGOLIA_APPLICATION_ID = settings.ALGOLIA['APPLICATION_ID']
    ALGOLIA_SEARCH_KEY = settings.ALGOLIA['SEARCH_KEY']
    index = "District" if settings.ALGOLIA['INDEX_SUFFIX'] else "District_".format(
        settings.ALGOLIA['INDEX_SUFFIX'],
    )
    return render(
        request,
        'app/involved/involved.html', {
            'ALGOLIA_APPLICATION_ID': ALGOLIA_APPLICATION_ID,
            'ALGOLIA_SEARCH_KEY': ALGOLIA_SEARCH_KEY,
            'index': index,
        },
    )

# def petition(request, id):
#     petition = Petition.objects.get(id=id)
#     try:
#         account = request.user.account
#     except AttributeError:
#         account = None
#     try:
#         signature = petition.signatures.get(account=account)
#     except Signature.DoesNotExist:
#         signature = None

#     if account:
#         if signature:
#             if request.method == "POST":
#                 form = SignatureForm(request.POST, instance=signature)
#                 if form.is_valid():
#                     form.save()
#                     messages.success(
#                         request,
#                         "Your Signature has been Saved!",
#                     )
#                     return redirect('account')
#             else:
#                 form = SignatureForm(instance=signature)
#         else:
#             if request.method == "POST":
#                 form = SignatureForm(request.POST)
#                 if form.is_valid():
#                     form.status = Signature.STATUS.signed
#                     form.save()
#                     messages.success(
#                         request,
#                         "Your Signature has been Saved!",
#                     )
#                     return redirect('account')
#             else:
#                 form = SignatureForm(initial={
#                     'petition': petition,
#                     'account': account,
#                     'name': account.name,
#                     'is_public': True,
#                 })
#     else:
#         # New Signup
#         form = SignupForm(request.POST or None)
#         if form.is_valid():
#             # Instantiate Variables
#             name = form.cleaned_data['name']
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             is_public = form.cleaned_data['is_public']
#             message = form.cleaned_data['message']

#             # Auth0 Signup
#             auth0_client = Database(settings.AUTH0_DOMAIN)
#             auth0_user = auth0_client.signup(
#                 client_id=settings.AUTH0_CLIENT_ID,
#                 email=email,
#                 password=password,
#                 connection='Username-Password-Authentication',
#                 username='noop', # TODO https://github.com/auth0/auth0-python/issues/228
#                 user_metadata={
#                     'name': name,
#                 }
#             )

#             # Create User
#             username = "auth0|{0}".format(auth0_user['_id'])

#             user = authenticate(
#                 request,
#                 username=username,
#                 email=email,
#             )
#             user.refresh_from_db()
#             account = user.account
#             account.name = name
#             account.save()

#             # Create Signature
#             signature = Signature.objects.create(
#                 status=Signature.STATUS.signed,
#                 name=name,
#                 is_public=is_public,
#                 message=message,
#                 account=account,
#                 petition=petition,
#             )
#             log_in(request, user)
#             messages.success(
#                 request,
#                 "Your Signature has Been Added to the Petition!",
#             )
#             return redirect('account')

#     return render(
#         request,
#         'public/petition.html',
#         {'petition': petition, 'form': form},
#     )


@login_required
def signature(request, id):
    signature = Signature.objects.get(
        id=id,
    )
    return render(
        request,
        'app/involved/signature.html',
        {'signature': signature},
    )

@login_required
def signature_add(request, id):
    signature = Signature.objects.get(
        id=id,
    )
    return render(
        request,
        'app/involved/signature_add.html',
        {'signature': signature},
    )

@login_required
def signature_remove(request, id):
    signature = Signature.objects.get(
        id=id,
    )
    if request.method == "POST":
        form = RemoveForm(request.POST)
        if form.is_valid():
            signature.status = signature.STATUS.removed
            signature.save()
            messages.error(
                request,
                "Signature Removed!",
            )
            return redirect('account')
    else:
        form = RemoveForm()
    return render(
        request,
        'app/involved/signature_remove.html',
        {'form': form,},
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
    signatures = account.signatures.order_by('created')
    return render(
        request,
        'app/account/account.html', {
            'form': form,
            'signatures': signatures,
        },
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
    report = Signature.objects.order_by(
        'petition',
    ).values(
        'petition',
    ).annotate(
        c=Count('id'),
    )
    total = Signature.objects.aggregate(
        c=Count('id'),
    )['c']
    return render(
        request,
        'app/admin/report.html',
        {'report': report, 'total': total},
    )
