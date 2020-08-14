# Standard Library
import json
import logging

# Django
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as log_in
from django.contrib.auth import logout as log_out
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.crypto import get_random_string

# First-Party
import requests
from dal import autocomplete

# Local
from .forms import AddAskForm
from .forms import AskForm
from .forms import DeleteForm
from .forms import HomeroomForm
from .forms import ParentForm
from .forms import SchoolForm
from .forms import StudentForm
from .forms import StudentFormSet
from .forms import TeacherForm
from .forms import UserAskForm
from .models import Ask
from .models import Homeroom
from .models import Parent
from .models import School
from .models import Student
from .models import Teacher
from .models import User
from .tasks import mailchimp_subscribe_email


# Root
def index(request):
    return render(
        request,
        'app/index.html',
        context={
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
        'robots.txt',
    )
    return HttpResponse(
        rendered,
        content_type="text/plain",
    )

def sitemap(request):
    slugs = School.objects.values_list('slug', flat=True)
    rendered = render_to_string(
        'sitemap.txt',
        context={
            'slugs': slugs,
        }
    )
    return HttpResponse(
        rendered,
        content_type="text/plain",
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
    if kind not in ['dashboard', 'teacher', 'parent']:
        homeroom_id = kind
        kind = 'ask'

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
    user = authenticate(request, **payload)
    if user:
        log_in(request, user)
        if kind == 'ask':
            return redirect('ask-form', homeroom_id)
        if kind == 'parent':
            kind = 'create-parent'
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


# Account
@login_required
def dashboard(request):
    user = request.user
    parent = getattr(user, 'parent', None)
    teacher = getattr(user, 'teacher', None)
    students = Student.objects.filter(
        parent=parent,
    )
    homerooms = Homeroom.objects.filter(
        parent=parent,
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
def delete_user(request):
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


# Student
@login_required
def create_student(request):
    parent = request.user.parent
    form = StudentForm(request.POST or None)
    if form.is_valid():
        student = form.save(commit=False)
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
        context={
            'form': form,
        }
    )

@login_required
def student(request, student_id):
    user = request.user
    student = Student.objects.get(
        id=student_id,
        parent=user.parent,
    )
    form = StudentForm(request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        messages.success(
            request,
            "Saved!",
        )
        return redirect('dashboard')
    return render(
        request,
        'app/student.html',
        context={
            'form': form,
            'student': student,
        },
    )

@login_required
def delete_student(request, student_id):
    parent = request.user.parent
    student = Student.objects.get(
        id=student_id,
    )
    if student.parent != parent:
        return HttpResponse(status=400)
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


# Teacher
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
        context={
            'form': form,
        }
    )


# Parent Onboarding
@login_required
def create_parent(request):
    parent = getattr(request.user, 'parent', None)
    if parent:
        return redirect('parent', parent.id)
    if request.method == "POST":
        parent = Parent.objects.create(
            user=request.user,
        )
        form = ParentForm(
            request.POST,
            instance=parent,
        )
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Parent Preferences Saved!",
            )
            return redirect('add-student-parent')
    else:
        form = ParentForm(
            instance=parent,
            initial={
                'name': request.user.name,
                'email': request.user.email,
            }
        )
    return render(
        request,
        'app/parent_create.html',
        context={
            'form': form,
        },
    )

@login_required
def parent(request, parent_id):
    parent = get_object_or_404(Parent, parent_id)
    if parent.id != request.user.parent.id:
        return HttpResponse(status=400)
    form = ParentForm(
        request.POST or None,
        instance=parent,
    )
    if form.is_valid():
        form.save()
        messages.success(
            request,
            "Saved!",
        )
        return redirect('dashboard')
    return render(
        request,
        'app/parent.html',
        context={
            'form': form,
        }
    )

@login_required
def add_student_parent(request):
    parent = request.user.parent
    is_more = bool(parent.students.count())
    students = parent.students.order_by('created')
    form = StudentForm(request.POST or None)
    if form.is_valid():
        student = form.save(commit=False)
        student.parent = parent
        student.save()
        messages.success(
            request,
            "Student Added!",
        )
        return redirect('add-student-parent')
    return render(
        request,
        'app/add_student_parent.html',
        context={
            'form': form,
            'is_more': is_more,
            'students': students,
        }
    )

@login_required
def create_homerooms(request):
    parent = request.user.parent
    students = parent.students.all()
    for student in students:
        homeroom = Homeroom.objects.create(
            parent=parent,
            frequency=parent.frequency,
            schedule=parent.schedule,
            safety=parent.safety,
        )
        student.homeroom = homeroom
        student.save()
    parent.is_welcomed = True
    parent.save()
    return redirect('homerooms')


@login_required
def add_ask(request, homeroom_id):
    homeroom = get_object_or_404(Homeroom, id=homeroom_id)
    form = AddAskForm(request.POST or None)
    if form.is_valid():
        ask = form.save(commit=False)
        ask.status = ask.STATUS.invited
        ask.homeroom = homeroom
        ask.save()
        messages.success(
            request,
            "Student Added!",
        )
        return redirect('homeroom', homeroom.id)
    return render(
        request,
        'app/add_ask.html',
        context={
            'form': form,
        }
    )

@login_required
def ask(request, homeroom_id, student_id):
    student = get_object_or_404(Student, id=student_id)
    homeroom = get_object_or_404(Homeroom, id=homeroom_id)
    Ask.objects.create(
        student=student,
        homeroom=homeroom,
    )
    messages.success(
        request,
        "Request sent!",
    )
    return redirect('dashboard')

@login_required
def ask_form(request, homeroom_id):
    homeroom = get_object_or_404(Homeroom, id=homeroom_id)
    parent, created = Parent.objects.get_or_create(
        user=request.user,
    )
    if created:
        parent.name = request.user.name
        parent.email = request.user.email
        parent.schedule = homeroom.schedule
        parent.frequency = homeroom.frequency
        parent.safety = homeroom.safety
        parent.save()
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            ask = form.save(commit=False)
            student = Student.objects.create(
                name=ask.student_name,
                gender=ask.gender,
                school=ask.school,
                grade=ask.grade,
                parent=parent,
            )
            ask.student = student
            ask.parent_name = parent.name
            ask.parent_email = parent.email
            ask.homeroom = homeroom
            ask.save()
            messages.success(
                request,
                "Request Sent!",
            )
            return redirect('dashboard')
    else:
        form = AskForm()
    return render(
        request,
        'app/ask_form.html',
        context={
            'form': form,
        }
    )

@login_required
def ask_user(request, homeroom_id):
    homeroom = get_object_or_404(Homeroom, id=homeroom_id)
    parent = request.user.parent
    if request.method == 'POST':
        form = UserAskForm(parent, request.POST)
        if form.is_valid():
            ask = form.save(commit=False)
            ask.student_name = ask.student.name
            ask.parent_name = ask.student.parent.name
            ask.parent_email = ask.student.parent.email
            ask.homeroom = homeroom
            ask.save()
            messages.success(
                request,
                "Request Sent!",
            )
            return redirect('dashboard')
    else:
        form = UserAskForm(parent)
    return render(
        request,
        'app/ask_user.html',
        context={
            'form': form,
            'homeroom': homeroom,
        }
    )

@login_required
def homerooms(request):
    parent = request.user.parent
    students = parent.students.all()
    for student in students:
        student.homeroom.homeroom_link = request.build_absolute_uri(
            reverse('homeroom', args=[student.homeroom.id])
        )
    return render(
        request,
        'app/homerooms.html',
        context={
            'students': students,
        }
    )

@login_required
def homeroom_search(request):
    return render(
        request,
        'app/homeroom_search.html',
        context={
            'app_id': settings.ALGOLIA['APPLICATION_ID'],
            'search_key': settings.ALGOLIA['SEARCH_KEY'],
            'index_name': "Homeroom_{0}".format(settings.ALGOLIA['INDEX_SUFFIX']),
        }
    )


# Homeroom
def homeroom(request, homeroom_id):
    homeroom = get_object_or_404(Homeroom, pk=homeroom_id)
    form = HomeroomForm(
        request.POST or None,
        instance=homeroom,
    )
    if form.is_valid():
        form.save()
        messages.success(
            request,
            'Saved!',
        )
        return redirect('homeroom', homeroom.id)
    homeroom_link = request.build_absolute_uri(
        reverse('homeroom', args=[homeroom_id])
    )
    students = homeroom.students.all()
    asks = homeroom.asks.all()
    return render(
        request,
        'app/homeroom.html', {
            'form': form,
            'homeroom': homeroom,
            'homeroom_link': homeroom_link,
            'students': students,
            'asks': asks,
        }
    )

@login_required
def delete_homeroom(request, homeroom_id):
    parent = request.user.parent
    homeroom = get_object_or_404(Homeroom, id=homeroom_id)
    if homeroom.parent != parent:
        return HttpResponse(status=400)
    if request.method == "POST":
        form = DeleteForm(request.POST)
        if form.is_valid():
            homeroom.delete()
            messages.error(
                request,
                "Homeroom Deleted!",
            )
            return redirect('dashboard')
    else:
        form = DeleteForm()
    return render(
        request,
        'app/delete_homeroom.html',
        {'form': form,},
    )

@login_required
def connect_homeroom(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    homerooms = Homeroom.objects.filter(
        students__school=student.school,
        students__grade=student.grade,
    ).distinct()
    students = Student.objects.filter(
        school=student.school,
        homeroom__isnull=True,
    ).order_by('grade')
    return render(
        request,
        'app/connect_homeroom.html',
        context={
            'student': student,
            'homerooms': homerooms,
            'students': students,
            'app_id': settings.ALGOLIA['APPLICATION_ID'],
            'search_key': settings.ALGOLIA['SEARCH_KEY'],
            'index_name': "Homeroom_{0}".format(settings.ALGOLIA['INDEX_SUFFIX']),
        }
    )

@login_required
def create_homeroom(request):
    parent = request.user.parent
    initial = {
        'schedule': parent.schedule,
        'frequency': parent.frequency,
        'safety': parent.safety,
    }
    form = HomeroomForm(request.POST or None, initial=initial)
    if form.is_valid():
        form.save()
        messages.success(
            request,
            "Homeroom Created!",
        )
        return redirect('dashboard')
    return render(
        request,
        'app/create_homeroom.html',
        context={
            'form': form,
        }
    )


# Schools
def search_schools(request):
    return render(
        request,
        'app/search_schools.html',
        context={
            'app_id': settings.ALGOLIA['APPLICATION_ID'],
            'search_key': settings.ALGOLIA['SEARCH_KEY'],
            'index_name': "School_{0}".format(settings.ALGOLIA['INDEX_SUFFIX']),
        },
    )

def school(request, slug):
    school = get_object_or_404(School, slug=slug)
    parents = User.objects.filter(
        parent__students__school=school,
    ).distinct()
    for parent in parents:
        parent.grades = ", ".join([x.get_grade_display() for x in parent.parent.students.filter(
        school=school).order_by('grade')])
    students = school.students.select_related(
        'parent'
    ).filter(
        homeroom__isnull=True,
    ).order_by(
        'grade',
        'name',
    )
    homerooms = Homeroom.objects.filter(
        students__school=school,
    ).distinct()

    return render(
        request,
        'app/school.html',
        context={
            'school': school,
            'parents': parents,
            'students': students,
            'homerooms': homerooms,
        },
    )

class SchoolAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = School.objects.filter(
        )

        if self.q:
            qs = qs.filter(search_vector=self.q)
        return qs
