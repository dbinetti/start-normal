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
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseForbidden
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
from .forms import DeleteForm
from .forms import HomeroomForm
from .forms import InviteForm
from .forms import ParentForm
from .forms import SchoolForm
from .forms import StudentForm
from .forms import StudentFormSet
from .forms import TeacherForm
from .models import Homeroom
from .models import Parent
from .models import School
from .models import Student
from .models import Teacher
from .models import User
from .tasks import mailchimp_subscribe_email


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
        }
    )

@login_required
def invite_classmate(request, homeroom_id):
    homeroom = Homeroom.objects.get(id=homeroom_id)
    schools = School.objects.filter(
        students__classmates__homeroom=homeroom,
    ).exclude(
    )
    students = Student.objects.filter(
        school__in=schools,
        classmates__isnull=True,
    ).exclude(
    ).order_by('grade')
    if request.method == 'POST':
        form = InviteForm(request.POST)
        if form.is_valid():
            invite = form.save(commit=False)
            invite.homeroom = homeroom
            invite.inviter = request.user
            invite.save()
            messages.success(
                request,
                "Classmate invited",
            )
            return redirect('homeroom', homeroom.id)
        else:
            print(form.errors)
    form = InviteForm()
    # invite_link = f'http://localhost:8000/invite/{homeroom_id}'
    invite_link = request.build_absolute_uri(reverse('invite', args=[homeroom_id]))
    return render(
        request,
        'app/invite_classmate.html',
        context={
            'form': form,
            'homeroom': homeroom,
            'students': students,
            'invite_link': invite_link,
        }
    )


def invite(request, homeroom_id):
    homeroom = Homeroom.objects.get(id=homeroom_id)
    parent = homeroom.parent.user.name
    classmates = homeroom.classmates.order_by(
        'student__school',
        'student__grade',
    )
    return render(
        request,
        'app/invite.html',
        context={
            'homeroom': homeroom,
            'parent': parent,
            'classmates': classmates,
        }
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
def create_homeroom(request, student_id):
    parent = request.user.parent
    homeroom = Homeroom.objects.create(
        parent=parent,
    )
    student = Student.objects.get(id=student_id)
    student.homeroom = homeroom
    student.save
    messages.success(
        request,
        "Homeroom Created!",
    )
    return redirect('homeroom', homeroom.id)


@login_required
def create_invite(request, homeroom_id):
    return


@login_required
def create_classmate(request, homeroom_id):
    homeroom = get_object_or_404(Homeroom, pk=homeroom_id)
    schools = School.objects.filter(
        students__classmates__homeroom=homeroom,
    )
    students = Student.objects.filter(
        school__in=schools,

    ).order_by('grade')
    if request.method == 'POST':

        form = InviteForm(request.POST)
        if form.is_valid():
            invite = form.save(commit=False)
            invite.homeroom = homeroom
            invite.save()
    return render(
        request,
        'app/create_classmate.html',
        context={
            'students': students,
            'form': form,
        },
    )


@login_required
def delete_student(request, student_id):
    parent = request.user.parent
    student = Student.objects.get(
        id=student_id,
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
def delete_classmate(request, classmate_id):
    return


@login_required
def parent(request):
    StudentFormSet.extra = 5
    parent, created = Parent.objects.get_or_create(
        user=request.user,
    )
    if request.method == "POST":
        formset = StudentFormSet(
            request.POST,
            request.FILES,
            instance=parent,
            prefix='students',
        )
        form = ParentForm(
            request.POST,
            instance=parent,
            prefix='parent',
        )
        if formset.is_valid() and form.is_valid():
            formset.save()
            form.save()
            messages.success(
                request,
                "Saved!",
            )
            return redirect('dashboard')
    formset = StudentFormSet(
        instance=parent,
        prefix='students',
    )
    form = ParentForm(
        instance=parent,
        prefix='parent',
    )
    return render(
        request,
        'app/parent.html',
        context={
            'formset': formset,
            'form': form,
        }
    )



@login_required
def accept(request, homeroom_id):
    user = request.user
    homeroom = Homeroom.objects.get(id=homeroom_id)

    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            parent, created = Parent.objects.get_or_create(
                user=user,
            )
            name = form.cleaned_data['name']
            school = form.cleaned_data['school']
            grade = form.cleaned_data['grade']
            student = Student.objects.create(
                name=name,
                school=school,
                grade=grade,
                parent=parent,
            )
            homeroom.classmates.create(student=student)
            messages.success(
                request,
                "Student added to homeroom!",
            )
            return redirect('dashboard')

    else:
        form = StudentForm()

    return render(
        request,
        'app/accept.html',
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

@login_required
def homeroom(request, homeroom_id):
    homeroom = get_object_or_404(Homeroom, pk=homeroom_id)
    schools = School.objects.filter(
        students__homeroom=homeroom,
    )
    students = homeroom.students.all()
    schoolmates = Student.objects.filter(
        school__in=schools,
        homeroom__isnull=True,
    ).order_by('grade')
    invites = homeroom.invites.all()
    return render(
        request,
        'app/homeroom.html', {
            'homeroom': homeroom,
            'students': students,
            'schoolmates': schoolmates,
            'invites': invites,
        },
    )


@login_required
def classmate(request, classmate_id):
    return

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
def add_classmate_from_student(request, homeroom_id, student_id):
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
    if kind not in ['dashboard', 'teacher', 'parent']:
        homeroom_id = kind
        kind = 'accept'

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
        if kind == 'accept':
            return redirect('accept', homeroom_id)
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


def school(request, slug):
    school = School.objects.get(slug=slug)
    parents = User.objects.filter(
        parent__students__school=school,
    ).distinct()
    for parent in parents:
        parent.grades = ", ".join([x.get_grade_display() for x in parent.parent.students.filter(
        school=school).order_by('grade')])
    students = school.students.select_related(
        'parent'
    ).filter(
        classmates__isnull=True,
    ).order_by(
        'grade',
        'name',
    )
    homerooms = Homeroom.objects.filter(
        classmates__student__school=school,
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
