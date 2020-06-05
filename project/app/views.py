# Django
from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render

# Local
from .forms import SignatureForm
from .models import Signature


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
            to = form.cleaned_data['email']
            if to:
                mail = EmailMessage(
                    subject='Thank you for supporting our children',
                    body='Thank you for supporting our kids and wanting to Start Normal.  Things are moving incredibly quickly but I will do my best to keep you updated as much as I can.  Feel free to reach out to me with questions, comments, or ideas.  You can also call me at 415.713.2126.  Best, Dave',
                    from_email='David Binetti <dbinetti@gmail.com>',
                    to=[to],
                    bcc=['dbinetti@gmail.com'],
                )
                mail.send()
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
