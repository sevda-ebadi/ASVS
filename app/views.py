import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from app.forms import EmployeeSignUpForm, EmployeeSignInForm, CompanySignInForm, CompanySignUpForm, \
    ResumeConfirmationForm, EditCompanyInfoForm, CreateResumeForm, EditEmployeeInfoForm
from .models import JobOpportunity, Employee, Employer, Company, Resume, OpportunityComment

logger = logging.getLogger(__name__)


def index(request):
    context = {}
    jobs = JobOpportunity.objects.all().order_by('created_at')
    context['jobs'] = jobs
    if request.user.is_authenticated:
        try:
            employee = Employee.objects.get(user=request.user)
            context['employee'] = employee
            return render(request, 'main.html', context)
        except:
            logger.error("some error happend")
        try:
            employer = Employer.objects.get(user=request.user)
            context['employer'] = employer
        except:
            logger.error("some error happend")
    return render(request, 'main.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


@csrf_protect
def employee_login(request):
    c = {}
    if request.method == "POST":
        submit = request.POST.get("submit", None)
        redirect_to = request.POST.get("redirect_to", None)
        if submit == "signin":
            form = EmployeeSignInForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username', None)
                password = form.cleaned_data.get('password', None)
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    print(redirect_to)
                    print(type(redirect_to))
                    url = redirect_to if redirect_to is not None else '/employee/panel'
                    return HttpResponseRedirect(url)
        elif submit == "signup":
            form = EmployeeSignUpForm(request.POST)
            if form.is_valid():
                firstname = form.cleaned_data.get('firstname', None)
                lastname = form.cleaned_data.get('lastname', None)
                email = form.cleaned_data.get('email', None)
                phone = form.cleaned_data.get('phone', None)
                degree = form.cleaned_data.get('degree', None)
                password = form.cleaned_data.get('password', None)
                try:
                    user = User(first_name=firstname, last_name=lastname, email=email, username=email)
                    user.set_password(password)
                    user.save()
                    employee = Employee(user=user, phone=phone, degree=degree)
                    employee.save()
                    auth = authenticate(request, username=email, password=password)
                    login(request, auth)
                    return HttpResponseRedirect('/employee/panel')
                except Exception as e:
                    c['message'] = str(e)
                    logger.error(e.message())
            else:
                c['message'] = form.errors
        return render(request, 'signin_signup_karjoo.html', c)
    else:
        redirect_to = request.GET.get("redirect_to", None)
        if redirect_to:
            c['redirect_to'] = redirect_to
        return render(request, 'signin_signup_karjoo.html', c)


@csrf_protect
def employee_panel(request):
    context = {}
    if request.method == "POST":
        form = EditEmployeeInfoForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data.get("phone", None)
            firstname = form.cleaned_data.get("firstname", None)
            lastname = form.cleaned_data.get("lastname", None)
            user = User.objects.get(id=request.user.id)
            user.first_name = firstname
            user.last_name = lastname
            user.save()
            employee = Employee.objects.get(user=user)
            employee.phone = phone
            employee.save()
        else:
            print(form.errors)
        return HttpResponseRedirect('/employee/panel')
    employee = Employee.objects.get(user=request.user)
    context['employee'] = employee
    return render(request, 'karjoo_panel.html', context)


@csrf_protect
def employee_panel_resume(request):
    context = {}
    employee = Employee.objects.get(user=request.user)
    resumes = Resume.objects.filter(employee=employee)
    context['resumes'] = resumes
    return render(request, 'send_resume.html', context)


@csrf_protect
def company_login(request):
    c = {}
    if request.method == "POST":
        submit = request.POST.get("submit", None)
        if submit == "signin":
            form = CompanySignInForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username', None)
                password = form.cleaned_data.get('password', None)
                user = authenticate(request, username=username, password=password)
                print(username)
                print(password)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect('/company/panel')
            else:
                print(form.errors)
        elif submit == "signup":
            form = CompanySignUpForm(request.POST, request.FILES)
            if form.is_valid():
                name = form.cleaned_data.get('company_name', None)
                email = form.cleaned_data.get('email', None)
                phone = form.cleaned_data.get('phone', None)
                password = form.cleaned_data.get('password', None)
                description = form.cleaned_data.get('description', None)
                logo = form.cleaned_data.get("file", None)
                try:
                    user = User(email=email, username=email)
                    user.set_password(password)
                    user.save()
                    company = Company(name=name, description=description, phone=phone)
                    company.logo = logo
                    company.save()
                    employee = Employer(user=user, company=company)
                    employee.save()
                    auth = authenticate(request, username=email, password=password)
                    login(request, auth)
                    return HttpResponseRedirect('/company/panel')
                except Exception as e:
                    c['message'] = str(e)
                    print(c)
            else:
                c['message'] = form.errors
                print(c)
        else:
            pass
        return render(request, 'signin_signup_company.html', c)
    else:
        return render(request, 'signin_signup_company.html', c)


@csrf_protect
def company_panel(request):
    context = {}
    employer = Employer.objects.get(user=request.user)
    if request.method == "POST":
        form = EditCompanyInfoForm(request.POST)
        if form.is_valid():
            company = Company.objects.get(employer=employer)
            company_name = form.cleaned_data.get("company_name", None)
            phone = form.cleaned_data.get("phone", None)
            description = form.cleaned_data.get("description", None)
            company.name = company_name
            company.phone = phone
            company.description = description
            company.save()
            print(company.description)
        else:
            print(form.errors.as_data())
        return HttpResponseRedirect('/company/panel')
    elif request.method == "GET":
        context['employer'] = employer
    return render(request, 'karfarma_panel.html', context)


@csrf_protect
def company_panel_resume(request):
    context = {}
    if request.method == "POST":
        form = ResumeConfirmationForm(request.POST)
        if form.is_valid():
            status = form.cleaned_data.get("status", None)
            resume_id = form.cleaned_data.get("resume_id", None)
            resume = Resume.objects.get(id=resume_id)
            resume.status = status
            resume.save()
            return HttpResponseRedirect('/company/panel/resume')
    elif request.method == "GET":
        company = Company.objects.get(employer__user=request.user)
        resumes = Resume.objects.filter(opportunity__company=company)
        context['resumes'] = resumes
    return render(request, 'recieve_resume.html', context)


@csrf_protect
def company_panel_job(request):
    context = {}
    if request.method == "POST":
        form = CreateJobOpportunityForm(request.POST)
        if form.is_valid():
            pass
        return HttpResponseRedirect('/')
    return render(request, 'create_job_op.html', context)


def info(request, opportunity_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/employee?redirect_to=/opportunity/' + opportunity_id)
    try:
        resume = Resume.objects.get(employee__user=request.user, opportunity_id=opportunity_id)
    except Resume.DoesNotExist:
        resume = None
    if request.method == "POST":
        if not resume:
            form = CreateResumeForm(request.POST, request.FILES)
            if form.is_valid():
                opportunity = JobOpportunity.objects.get(id=opportunity_id)
                employee = Employee.objects.get(user=request.user)
                resume = Resume(opportunity=opportunity, employee=employee)
                file = form.cleaned_data.get("file", None)
                salary = form.cleaned_data.get("salary", None)
                resume.resume = file
                resume.salary = salary
                resume.save()
                return HttpResponseRedirect('/opportunity/' + opportunity_id)
        return HttpResponseRedirect('/opportunity/' + opportunity_id)
    else:
        context = {}
        employee = Employee.objects.get(user=request.user)
        job = JobOpportunity.objects.get(id=opportunity_id)
        comments = OpportunityComment.objects.filter(opportunity_id=opportunity_id)
        context['job'] = job
        context['employee'] = employee
        context['opportunity_id'] = opportunity_id
        context['resume'] = resume
        context['comments'] = comments
    return render(request, 'info_job.html', context)


invalid_characters = {
    " ": "&nbsp",
    "\"": "&quot",
    '>': "&gt",
    '<': "&lt",
    "'": "&apos"
}


def xss(string):
    out = str()
    for character in string:
        token = invalid_characters.get(character, None)
        if token:
            out += token
        else:
            out += character
    return out


def info_comment(request, opportunity_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/employee?redirect_to=/opportunity/' + opportunity_id)
    if request.method == "POST":
        text = request.POST.get("text", None)
        text = xss(text)
        if text is not None:
            opportunity = JobOpportunity.objects.get(id=opportunity_id)
            employee = Employee.objects.get(user=request.user)
            comment = OpportunityComment(user=employee, opportunity=opportunity, text=text)
            comment.save()
    return HttpResponseRedirect('/opportunity/' + opportunity_id)


def search(request):
    context = {}
    page = request.GET.get('page')
    q = request.GET.get('q', None)
    if not q:
        jobs_list = JobOpportunity.objects.all()
    else:
        jobs_list = JobOpportunity.objects.filter(Q(title__contains=q) | Q(description__contains=q))
    paginator = Paginator(jobs_list, 5)
    try:
        jobs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        jobs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        jobs = paginator.page(paginator.num_pages)
    context['jobs'] = jobs
    if q:
        context['q'] = q

    if request.user.is_authenticated:
        try:
            employee = Employee.objects.get(user=request.user)
            context['employee'] = employee
            return render(request, 'search_page.html', context)
        except:
            pass
        try:
            employer = Employer.objects.get(user=request.user)
            context['employer'] = employer
        except:
            pass
    return render(request, 'search_page.html', context)
