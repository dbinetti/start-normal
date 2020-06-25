# Django
# Third-Party
import django_rq
import shortuuid
from django_rq import job

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetConfirmView
from django.core.mail import EmailMessage
from django.db.models import Count
from django.db.models import Sum
from django.dispatch import receiver
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy

# Local
from .forms import AccountForm
from .forms import CustomSetPasswordForm
from .forms import CustomUserCreationForm
from .forms import DeleteForm
from .forms import RegistrationForm
from .forms import SignatureForm
from .forms import SubscribeForm
from .models import CustomUser
from .models import District
from .models import Faq
from .models import Signature
from .tasks import build_email
from .tasks import mailchimp_subscribe_email
from .tasks import send_email
from .tasks import welcome_email


def district_detail(request, short):
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
        'app/district_detail.html',
        {'district': district, 'contacts': contacts},
    )


def district_list(request):
    districts = District.objects.order_by('name')
    return render(
        request,
        'app/district_list.html',
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
            print('1')
            # Create related user account
            email = form.cleaned_data.get('email')
            password = shortuuid.uuid()
            user = CustomUser(
                email=email,
                password=password,
                is_active=True,
            )
            user = user.save()

            # Relate records and save
            signature.user = user
            signature.save()
            print('2')
            # Notify User through UI
            messages.success(
                request,
                'Your Signature has been added to the Petition.',
            )
            print('3')

            # Execute related tasks
            welcome_email.delay(signature)
            mailchimp_subscribe_email.delay(
                email=signature.email,
                location=signature.location,
            )
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
def account(request):
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
        'app/account.html',
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

def learn(request):
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
        'app/learn.html',
        {'form': form,},
    )

def thanks(request):
    return render(
        request,
        'app/thanks.html',
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
