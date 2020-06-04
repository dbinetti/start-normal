# Django
from django.contrib import messages
from django.shortcuts import (
    redirect,
    render,
)

# Local
from .forms import SignatureForm
from .models import Signature


def index(request):
    if request.method == "POST":
        form = SignatureForm(request.POST)
        if form.is_valid():
            signature = form.save()
            messages.success(
                request,
                'Your name has been added to the Petition.',
            )
            return redirect('thanks')
    else:
        form = SignatureForm()
    signatures = Signature.objects.filter(
        is_approved=True,
    ).order_by('timestamp')
    return render(
        request,
        'app/index.html',
        {'form': form,
        'signatures': signatures},
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


def letter(request):
    return render(
        request,
        'app/letter.html',
    )
