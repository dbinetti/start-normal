# Standard Library
import json
import logging

# Third-Party
import requests
from dal import autocomplete

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

# Local
from .forms import DeleteForm
from .forms import HomeroomForm
from .forms import InviteForm
from .forms import ParentForm
from .forms import SchoolForm
from .forms import StudentForm
from .forms import StudentFormSet
from .forms import TeacherForm
from .models import Ask
from .models import Homeroom
from .models import Invite
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
            qs = qs.filter(search_vector=self.q)
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
def homeroom_invite(request, homeroom_id):
    homeroom = Homeroom.objects.get(id=homeroom_id)
    # schools = School.objects.filter(
    #     students__homeroom=homeroom,
    # ).exclude(
    # )
    # schoolmates = Student.objects.filter(
    #     school__in=schools,
    #     homeroom__isnull=True,
    # ).exclude(
    # ).order_by('grade')
    form = InviteForm(request.POST or None)
    if form.is_valid():
        invite = form.save(commit=False)
        invite.homeroom = homeroom
        invite.inviter = request.user
        invite.save()
        messages.success(
            request,
            "Classmate Added!",
        )
        return redirect('homeroom', homeroom.id)
    homeroom_link = request.build_absolute_uri(reverse('homeroom', args=[homeroom_id]))
    return render(
        request,
        'app/homeroom_invite.html',
        context={
            'form': form,
            'homeroom': homeroom,
            # 'schoolmates': schoolmates,
            'homeroom_link': homeroom_link,
        }
    )


def invite(request, invite_id):
    invite = get_object_or_404(Invite, pk=invite_id)
    students = invite.homeroom.students.order_by(
        'school',
        'grade',
    )
    return render(
        request,
        'app/invite.html',
        context={
            'invite': invite,
            'students': students,
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
    student = Student.objects.get(id=student_id)
    initial = {
        'schedule': parent.schedule,
        'frequency': parent.frequency,
        'safety': parent.safety,
    }
    form = HomeroomForm(request.POST or None, initial=initial)
    if form.is_valid():
        homeroom = form.save(commit=False)
        homeroom.parent = parent
        homeroom.save()
        student.homeroom = homeroom
        student.save()
        messages.success(
            request,
            "Homeroom Created!",
        )
        return redirect('parent-homeroom-intro')
    return render(
        request,
        'app/create_homeroom.html',
        context={
            'form': form,
            'student': student,
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
    return redirect('homerooms')



@login_required
def homerooms(request):
    parent = request.user.parent
    homerooms = parent.homerooms.all()
    return render(
        request,
        'app/homerooms.html',
        context={
            'homerooms': homerooms,
        }
    )



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
def remove_homeroom_student(request, homeroom_id, student_id):
    homeroom = get_object_or_404(Homeroom, pk=homeroom_id)
    student = get_object_or_404(Student, pk=student_id)
    student.homeroom = None
    student.save()
    messages.success(
        request,
        "Student Removed!",
    )
    return redirect('homeroom', homeroom.id)



@login_required
def parent(request):
    parent = getattr(request.user, 'parent', None)
    if request.method == "POST":
        parent, _ = Parent.objects.get_or_create(
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
                "Saved!",
            )
            return redirect('parent-two')
    else:
        form = ParentForm(
            instance=parent,
        )
    return render(
        request,
        'app/parent.html',
        context={
            'form': form,
        }
    )


@login_required
def parent_two(request):
    StudentFormSet.extra = 1
    parent = request.user.parent
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
    else:
        formset = StudentFormSet(
            instance=parent,
        )
    return render(
        request,
        'app/parent_two.html',
        context={
            'formset': formset,
        }
    )



@login_required
def add_student_parent(request):
    parent = request.user.parent
    is_more = bool(parent.students.count())
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
        }
    )


@login_required
def parent_homeroom_intro(request):
    parent = request.user.parent
    students = parent.students.order_by(
        'grade',
    )
    return render(
        request,
        'app/parent_homeroom_intro.html',
        context={
            'students': students,
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

def homeroom(request, homeroom_id):
    homeroom = get_object_or_404(Homeroom, pk=homeroom_id)
    invites = homeroom.invites.all()
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
    students = homeroom.students.values_list(
        'name',
        'parent__user__name',
        'parent__user__email',
    )
    invites = homeroom.invites.values_list(
        'student_name',
        'parent_name',
        'parent_email',
    )
    classmates = []
    for student in students:
        classmates.append({
            'student_name': student[0],
            'parent_name':student[1],
            'parent_email':student[2],
        })
    for invite in invites:
        classmates.append({
            'student_name': invite[0],
            'parent_name':invite[1],
            'parent_email':invite[2],
        })
    return render(
        request,
        'app/homeroom.html', {
            'form': form,
            'homeroom': homeroom,
            'invites': invites,
            'homeroom_link': homeroom_link,
            'classmates': classmates,
        }
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
def add_homeroom_student(request, homeroom_id, student_id):
    homeroom = get_object_or_404(Homeroom, pk=homeroom_id)
    student = get_object_or_404(Student, pk=student_id)
    student.homeroom = homeroom
    student.save()
    messages.success(
        request,
        "Student Addded!",
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
        return redirect(kind)
    return HttpResponse(status=400)

@login_required
def ask_form(request, homeroom_id):
    homeroom = get_object_or_404(Homeroom, id=homeroom_id)
    parent, created = Parent.objects.get_or_create(
        user=request.user,
    )
    if created:
        parent.schedule = homeroom.schedule
        parent.frequency = homeroom.frequency
        parent.safety = homeroom.safety
        parent.save()
    form = StudentForm(request.POST or None)
    if form.is_valid():
        student = form.save(commit=False)
        student.parent = parent
        student.save()
        Ask.objects.create(
            homeroom=homeroom,
            student=student,
        )
        messages.success(
            request,
            "Request Sent!",
        )
        return redirect('dashboard')
    return render(
        request,
        'app/ask_form.html',
        context={
            'form': form,
        }
    )


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
