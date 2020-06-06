# Django
from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import (
    redirect,
    render,
)

# First-Party
import django_rq
from django_rq import job

# Local
from .forms import SignatureForm
from .models import Signature


@job
def queue_email(subject, body, to):
    mail = EmailMessage(
        subject=subject,
        body=body,
        from_email='David Binetti <dbinetti@gmail.com>',
        to=to,
        # bcc=['dbinetti@gmail.com'],
    )
    return mail.send()


def index(request):
    return render(
        request,
        'app/index.html',
    )

def letter(request):
    if request.method == "POST":
        form = SignatureForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Your name has been added to the Letter.',
            )
            email = form.cleaned_data['email']
            if email:
                subject = 'Thank you for supporting our children'
                body = 'Thank you for supporting our kids and wanting to Start Normal.  Apologies for the auto-responding message but response to this has been extraordinary and it\'s the only way I can keep up.  Feel free to reach out to me with questions, comments, or ideas.  You can also call me at 415.713.2126.  Best, Dave'
                from_email = 'David Binetti <dbinetti@gmail.com>'
                to=[email]
                queue_email.delay(
                    subject=subject,
                    body=body,
                    to=to,
                )
            return redirect('thanks')
    else:
        form = SignatureForm()
    return render(
        request,
        'app/letter.html',
        {'form': form,},
    )

def thanks(request):
    return render(
        request,
        'app/thanks.html',
    )

def framework(request):
    return render(
        request,
        'app/framework.html',
    )
def about(request):
    return render(
        request,
        'app/about.html',
    )

def data(request):
    return render(
        request,
        'app/data.html',
    )

def unsustainable(request):
    return render(
        request,
        'app/unsustainable.html',
    )

def unrealistic(request):
    return render(
        request,
        'app/unrealistic.html',
    )

def morrow(request):
    return render(
        request,
        'app/morrow.html',
    )

def harm(request):
    return render(
        request,
        'app/harm.html',
    )

def transcript(request):
    return render(
        request,
        'app/transcript.html',
    )
