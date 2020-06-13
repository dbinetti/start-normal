# Django
# Third-Party
import django_rq
import shortuuid
from django_rq import job

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import (
    authenticate,
    login,
    logout,
)
from django.core.mail import EmailMessage
from django.db.models import (
    Count,
    Sum,
)
from django.dispatch import receiver
from django.shortcuts import (
    redirect,
    render,
)

# Local
from .forms import (
    CustomUserCreationForm,
    SignatureForm,
)
from .models import (
    CustomUser,
    Signature,
)
from .tasks import build_email


@job
def queue_email(email):
    return email.send()


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
                    email.bcc = ['dbinetti@gmail.com']
                queue_email.delay(email)
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


def process_login(request):
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
        redirect('index')
    return render(
        request,
        'app/login.html',
        {'form': form},
    )

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("index")


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
