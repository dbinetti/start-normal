# Django
# Standard Library
import json
import logging

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
from django.db.models import Q
from django.db.models import Sum
from django.dispatch import receiver
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string

# First-Party
import django_rq
import requests
from auth0.v3.authentication import Database
from auth0.v3.authentication import Logout
from auth0.v3.exceptions import Auth0Error
from dal import autocomplete
from django_rq import job

# Local
from .forms import AccountForm
from .forms import ClassmateForm
from .forms import ContactForm
from .forms import DeleteForm
from .forms import HomeroomForm
from .forms import InviteForm
from .forms import InviteFormSet
from .forms import ReportForm
from .forms import SchoolForm
from .forms import SignupForm
from .forms import StudentForm
from .forms import StudentFormSet
from .forms import SubscribeForm
from .forms import TeacherForm
from .forms import UserCreationForm
from .models import Account
from .models import Classmate
from .models import Contact
from .models import District
from .models import Entry
from .models import Homeroom
from .models import Parent
from .models import Report
from .models import School
from .models import Student
from .models import Teacher
from .models import Transmission
from .models import User
from .tasks import build_email
from .tasks import mailchimp_create_or_update_from_user
from .tasks import mailchimp_subscribe_email
from .tasks import send_email


# Root
def index(request):
    return render(
        request,
        'app/index.html',
        context = {
            'app_id': settings.ALGOLIA['APPLICATION_ID'],
            'search_key': settings.ALGOLIA['SEARCH_KEY'],
            'index_name': "School_{0}".format(settings.ALGOLIA['INDEX_SUFFIX']),
        }
    )

def about(request):
    return render(
        request,
        'app/about.html',
    )

def faq(request):
    return render(
        request,
        'app/faq.html',
    )

def team(request):
    return render(
        request,
        'app/team.html',
    )

def privacy(request):
    return render(
        request,
        'app/privacy.html',
    )

def robots(request):
    rendered = render_to_string(
        'app/robots.txt',
    )
    return HttpResponse(
        rendered,
        content_type="text/plain",
    )


def sitemap(request):
    slugs = School.objects.values_list('slug', flat=True)
    rendered = render_to_string(
        'app/sitemap.txt',
        context = {
            'slugs': slugs,
        }
    )
    return HttpResponse(
        rendered,
        content_type="text/plain",
    )


# Account
@login_required
def dashboard(request):
    user = request.user

    if not user.account.is_welcomed:
        return redirect('share')
    parent = getattr(user, 'parent', None)
    teacher = getattr(user, 'teacher', None)
    students = Student.objects.filter(
        parent=parent,
    )
    homerooms = Homeroom.objects.filter(
        students__in=students,
    )
    return render(
        request,
        'app/dashboard.html',
        context={
            'user': user,
            'parent': parent,
            'teacher': teacher,
            'students': students,
            'homerooms': homerooms,
        }
    )


@login_required
def account(request):
    StudentFormSet.extra = 0
    user = request.user
    account = Account.objects.get(
        user=user,
    )
    parent = getattr(user, 'parent', None)
    teacher = getattr(user, 'teacher', None)
    valid = False
    if request.method == "POST":
        form = AccountForm(
            request.POST,
            instance=account,
            prefix='account',
        )
        if form.is_valid():
            form.save()
        else:
            valid = False
        if teacher:
            teacher_form = TeacherForm(
                request.POST,
                instance=teacher,
                prefix='teacher',
            )
            if teacher_form.is_valid():
                teacher_form.save(commit=False)
                teacher_form.user = user
                teacher_form.save()
            else:
                valid = False
        if parent:
            formset = StudentFormSet(
                request.POST,
                request.FILES,
                instance=parent,
                prefix='students',
            )
            if formset.is_valid():
                formset.save()
            else:
                valid = False
        if valid:
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
        if teacher:
            teacher_form = TeacherForm(
                instance=teacher,
                prefix='teacher',
            )
        else:
            teacher_form = None
        if parent:
            formset = StudentFormSet(
                instance=parent,
                prefix='students',
            )
        else:
            formset = None
    return render(
        request,
        'app/account.html', {
            'user': user,
            'form': form,
            'teacher_form': teacher_form,
            'formset': formset,
        },
    )

@login_required
def pending(request):
    return render(
        request,
        'app/pending.html',
    )

@login_required
def teacher(request):
    user = request.user
    teacher, created = Teacher.objects.get_or_create(
        user=user,
    )
    if request.method == "POST":
        form = TeacherForm(
            request.POST,
            instance=teacher,
        )
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Saved!",
            )
            return redirect('dashboard')
    else:
        form = TeacherForm(
            instance=teacher,
        )
    return render(
        request,
        'app/teacher.html',
        context = {
            'form': form,
        }
    )

@login_required
def invite(request, student_id):
    student = Student.objects.get(id=student_id)
    parent = request.user.parent
    if request.method == 'POST':
        form = InviteForm(request.POST)
        if form.is_valid():
            homeroom = form.cleaned_data['homeroom']
            classmate, created = Classmate.objects.get_or_create(
                homeroom=homeroom,
                student=student,
            )
            classmate.status = classmate.STATUS.accepted
            classmate.save()
            messages.success(
                request,
                "Classmate Added!",
            )
            return redirect('school', student.school.slug)
    form = InviteForm()
    form.fields['homeroom'].queryset = Homeroom.objects.filter(
        parent=parent,
    )
    return render(
        request,
        'app/invite.html',
        context = {
            'form': form,
        }
    )

@login_required
def create_teacher(request):
    user = request.user
    teacher, created = Teacher.objects.get_or_create(
        user=user,
    )
    return redirect('account')

@login_required
def create_parent(request):
    user = request.user
    parent, created = Parent.objects.get_or_create(
        user=user,
    )
    return redirect('account')

@login_required
def create_student(request):
    parent = request.user.parent
    form = StudentForm(request.POST or None)
    if form.is_valid():
        school = form.cleaned_data['school']
        grade = form.cleaned_data['grade']
        homeroom = Homeroom.objects.get(
            school=school,
            grade=grade,
        )
        student = form.save(commit=False)
        student.homeroom = homeroom
        student.parent = parent
        student.save()
        messages.success(
            request,
            'Added!',
        )
        return redirect('dashboard')
    return render(
        request,
        'app/create_student.html',
        context = {
            'form': form,
        }
    )

@login_required
def join_homeroom(request):
    return render(
        request,
        'app/join_homeroom.html',
        # {'form': form,},
    )

@login_required
def delete_student(request, id):
    parent = request.user.parent
    student = Student.objects.get(
        id=id,
    )
    if request.method == "POST":
        form = DeleteForm(request.POST)
        if form.is_valid():
            student.delete()
            messages.error(
                request,
                "Student Deleted!",
            )
            return redirect('dashboard')
    else:
        form = DeleteForm()
    return render(
        request,
        'app/delete_student.html',
        {'form': form,},
    )


@login_required
def parent(request):
    user = request.user
    StudentFormSet.extra = 5
    parent, created = Parent.objects.get_or_create(
        user=user,
    )
    if request.method == "POST":
        formset = StudentFormSet(
            request.POST,
            request.FILES,
            instance=parent,
        )
        if formset.is_valid():
            formset.save()
            messages.success(
                request,
                "Saved!",
            )
            return redirect('dashboard')
    formset = StudentFormSet(
        instance=parent,
    )
    return render(
        request,
        'app/parent.html',
        context = {
            'formset': formset,
        }
    )


@login_required
def join(request, id):
    homeroom = Homeroom.objects.get(id=id)
    user = request.user
    parent, created = Parent.objects.get_or_create(
        user=user,
    )
    student = Student.objects.create(
        grade=homeroom.grade,
        school=homeroom.school,
        parent=parent,
        # homeroom=homeroom,
    )
    if request.method == 'POST':
        form = StudentForm(
            request.POST,
            instance=student,
        )
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Added to Homeroom!",
            )
            return redirect('dashboard')
    form = StudentForm(
        instance=student,
    )
    return render(
        request,
        'app/join.html',
        context = {
            'form': form,
            'homeroom': homeroom,
        }
    )


@login_required
def addme(request, homeroom_id):
    homeroom = Homeroom.objects.get(id=homeroom_id)
    user = request.user
    parent, created = Parent.objects.get_or_create(
        user=user,
    )
    student = Student.objects.create(
        grade=homeroom.grade,
        school=homeroom.school,
        parent=parent,
        # homeroom=homeroom,
    )
    if request.method == 'POST':
        form = StudentForm(
            request.POST,
            instance=student,
        )
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Added to Homeroom!",
            )
            return redirect('dashboard')
    form = StudentForm(
        instance=student,
    )
    return render(
        request,
        'app/invite.html',
        context = {
            'form': form,
        }
    )


@login_required
def student(request, id):
    user = request.user
    student = Student.objects.get(
        id=id,
        parent=user.parent,
    )
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Saved!",
            )
            return redirect('dashboard')
    else:
        form = StudentForm(instance=student)

    return render(
        request,
        'app/student.html',
        context = {
            'form': form,
            'student': student,
        },
    )

# @login_required
def homeroom(request, id):
    homeroom = get_object_or_404(Homeroom, pk=id)
    classmates = homeroom.classmates.all()
    return render(
        request,
        'app/homeroom.html', {
            'homeroom': homeroom,
            'classmates': classmates,
        },
    )


@login_required
def add_student(request, homeroom_id):
    homeroom = get_object_or_404(Homeroom, pk=homeroom_id)
    students = Student.objects.filter(
        school__students__homeroom=homeroom,
    ).distinct('school__students')
    return render(
        request,
        'app/add_student.html', {
            'students': students,
            'homeroom': homeroom,
        },
    )


@login_required
def add_classmate(request, homeroom_id, student_id):
    homeroom = get_object_or_404(Homeroom, pk=homeroom_id)
    student = get_object_or_404(Student, pk=student_id)
    classmate, created = Classmate.objects.get_or_create(
        homeroom=homeroom,
        student=student,
    )
    if created:
        messages.success(
            request,
            "Classmate Addded!",
        )
    return redirect('homeroom', homeroom.id)


@login_required
def share(request):
    account = request.user.account
    account.is_welcomed = True
    account.save()
    return render(
        request,
        'app/share.html',
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
        'app/delete.html',
        {'form': form,},
    )



# Authentication
def login(request):
    redirect_uri = request.build_absolute_uri(reverse('callback'))
    state = "{0}|{1}".format(
        'dashboard',
        get_random_string(),
    )
    request.session['state'] = state
    params = {
        'response_type': 'code',
        'client_id': settings.AUTH0_CLIENT_ID,
        'scope': 'openid profile email',
        'redirect_uri': redirect_uri,
        'state': state,
    }
    url = requests.Request(
        'GET',
        'https://{0}/authorize'.format(settings.AUTH0_DOMAIN),
        params=params,
    ).prepare().url
    return redirect(url)

def signup(request, kind):
    redirect_uri = request.build_absolute_uri(reverse('callback'))
    state = "{0}|{1}".format(
        kind,
        get_random_string(),
    )
    request.session['state'] = state
    params = {
        'response_type': 'code',
        'client_id': settings.AUTH0_CLIENT_ID,
        'scope': 'openid profile email',
        'redirect_uri': redirect_uri,
        'state': state,
        'action': 'signup',
    }
    url = requests.Request(
        'GET',
        'https://{0}/authorize'.format(settings.AUTH0_DOMAIN),
        params=params,
    ).prepare().url
    return redirect(url)

def callback(request):
    # Reject if state doesn't match
    browser_state = request.session.get('state', None)
    server_state = request.GET.get('state', None)
    if browser_state != server_state:
        return HttpResponse(status=400)

    # Parse referrer
    kind = server_state.partition("|")[0]
    if kind not in ['dashboard', 'parent', 'teacher',]:
        try:
            homeroom = Homeroom.objects.get(id=kind)
        except Homeroom.DoesNotExist:
            homeroom = None
            kind = 'parent'
    else:
        homeroom = None
    # Get Auth0 Code
    code = request.GET.get('code', None)
    if not code:
        return HttpResponse(status=400)
    token_url = 'https://{0}/oauth/token'.format(
        settings.AUTH0_DOMAIN,
    )
    redirect_uri = request.build_absolute_uri(reverse('callback'))
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
        headers={
            'content-type': 'application/json',
        }
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
        if homeroom:
            return redirect('join', homeroom.id)
        return redirect(kind)
    return HttpResponse(status=400)

def logout(request):
    log_out(request)
    params = {
        'client_id': settings.AUTH0_CLIENT_ID,
        'return_to': request.build_absolute_uri(reverse('index')),
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


# Autocomplete
class SchoolAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = School.objects.filter(
        )

        if self.q:
            # qs = qs.filter(slug__icontains=self.q)
            qs = qs.filter(
                Q(name__icontains=self.q)|
                Q(city__icontains=self.q) |
                Q(state__icontains=self.q)
            )

        return qs

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
        'app/informed.html',
        context = {
            'form': form,
            'app_id': settings.ALGOLIA['APPLICATION_ID'],
            'search_key': settings.ALGOLIA['SEARCH_KEY'],
            'index_name': "School_{0}".format(settings.ALGOLIA['INDEX_SUFFIX']),
        },
    )

def school(request, slug):
    user = request.user
    school = School.objects.get(slug=slug)
    parents = User.objects.filter(
        parent__students__school=school,
    ).distinct()
    for parent in parents:
        parent.grades = ", ".join([x.get_grade_display() for x in parent.parent.students.filter(
        school=school).order_by('grade')])
    if request.user.is_authenticated:
        user_reports = Report.objects.filter(
            status=Report.STATUS.new,
            transmissions__school=school,
            user=request.user,
        ).order_by('-created')
    else:
        user_reports = None
    reports = Report.objects.filter(
        status=Report.STATUS.approved,
        transmissions__school=school,
    ).order_by('-created')
    contacts = Contact.objects.filter(
        is_active=True,
        entries__school=school,
    ).order_by('role')
    # homerooms = school.homerooms.order_by('grade')
    students = school.students.select_related('parent').order_by('grade', 'name')
    return render(
        request,
        'app/school.html',
        context={
            'school': school,
            'user_reports': user_reports,
            'reports': reports,
            'contacts': contacts,
            'parents': parents,
            # 'homerooms': homerooms,
            'students': students,
        },
    )

def search(request):
    return render(
        request,
        'app/search.html',
        context={
            'app_id': settings.ALGOLIA['APPLICATION_ID'],
            'search_key': settings.ALGOLIA['SEARCH_KEY'],
            'index_name': "School_{0}".format(settings.ALGOLIA['INDEX_SUFFIX']),
        },
    )



@login_required
def add_school(request):
    user = request.user
    form = SchoolForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(
            request,
            "School Submitted!",
        )
        return redirect('parent')
    return render(
        request,
        'app/add_school.html',
        context = {
            'form': form,
        },
    )

@login_required
def add_report(request, slug):
    user = request.user
    school = School.objects.get(slug=slug)
    form = ReportForm(request.POST or None)
    if form.is_valid():
        report = form.save(commit=False)
        report.user = user
        report.save()
        transmission = Transmission.objects.create(
            school=school,
            report=report,
        )
        messages.success(
            request,
            "Report Submitted!",
        )
        return redirect('school', slug)
    return render(
        request,
        'app/report.html',
        {'form': form,},
    )

@login_required
def add_contact(request, slug):
    user = request.user
    school = School.objects.get(slug=slug)
    form = ContactForm(request.POST or None)
    if form.is_valid():
        contact = form.save(commit=False)
        contact.user = user
        contact = form.save()
        entry = Entry.objects.create(
            school=school,
            contact=contact,
        )
        messages.success(
            request,
            "Contact Submitted!",
        )
        return redirect('school', slug)
    return render(
        request,
        'app/contact.html',
        {'form': form,},
    )




def morrow(request):
    return render(
        request,
        'app/morrow.html',
    )

def thomas(request):
    return render(
        request,
        'app/thomas.html',
    )
