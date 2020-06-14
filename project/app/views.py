# Django
# First-Party
import django_rq
import shortuuid
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetConfirmView
from django.core.mail import EmailMessage
from django.db.models import Count, Sum
from django.dispatch import receiver
from django.shortcuts import redirect, render
from django_rq import job

# Local
from .forms import (AccountForm, CustomSetPasswordForm, CustomUserCreationForm,
                    DeleteForm, SignatureForm, SubscribeForm)
from .models import CustomUser, Signature
from .tasks import build_email, send_email, subscribe_email


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name='app/claim.html'
    form_class = CustomSetPasswordForm

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
    return render(
        request,
        'app/account.html',
        {'form': form,},
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
            messages.danger(
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
    if request.method == "POST":
        form = SignatureForm(request.POST)
        if form.is_valid():
            signature = form.save()

            email = form.cleaned_data.get('email')
            password = shortuuid.uuid()
            user = CustomUser(
                email=email,
                password=password,
            )
            user.save()
            user.refresh_from_db()
            signature.user = user
            signature.save()

            messages.success(
                request,
                'Your name has been added to the Letter.',
            )
            context = form.cleaned_data
            if email:
                email = build_email(
                    subject='Start Normal - Thank You!',
                    template='emails/thank_you.txt',
                    context=context,
                    to=[email],
                )
                if context['notes']:
                    email.bcc = ['dbinetti@startnormal.com']
                send_email.delay(email)
            return redirect('thanks')
    else:
        form = SignatureForm()
    return render(
        request,
        'app/letter.html',
        {'form': form,},
    )

def learn(request):
    if request.method == "POST":
        form = SubscribeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            subscribe_email.delay(email=email)
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
    return redirect("https://fast.wistia.net/embed/channel/uutb20lwv5")



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
    ).order_by('id')
    return render(
        request,
        'app/notes.html',
        {'signatures': signatures},
    )
