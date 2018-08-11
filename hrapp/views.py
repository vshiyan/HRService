from django.shortcuts import render, redirect
from hrapp.forms import CompanyForm, DepartamentForm, PositionForm, UserForm, UserLoginForm, PositionChoicesForm
from hrapp.models import Position, User, Worker, Departament, Company
from django.contrib.auth import authenticate, login, logout
from django import forms


# Create your views here.
def home(request):
    """Rendering home page"""
    return render(request, 'hrapp/home.html', {})


def signup_company(request):
    """Rendering page sign up for company"""
    if request.method == "POST":
        form_com = CompanyForm(request.POST)
        form_dep = DepartamentForm(request.POST)
        form_pos = PositionForm(request.POST)
        form_user = UserForm(request.POST)
        if form_com.is_valid() and form_dep.is_valid() and form_pos.is_valid() and form_user.is_valid():
            company = form_com.save(commit=False)
            company.save()
            print(company.title_com)
            departament = form_dep.save(commit=False)
            departament.company = Company.objects.get(pk=company.pk)
            departament.save()
            position = form_pos.save(commit=False)
            position.departament = Departament.objects.get(pk=departament.pk)
            position.vakant = False
            position.save()
            form_user.save()
            user = User.objects.get(username=form_user.data['username'])
            Worker.objects.create(user=user, role='admin', position=position, vakant=False)
            print('Доходит')
            # user = authenticate(username=form.data['username'], password=form.data['password1'])
            # login(request, user)
            return redirect('home')
    else:
        form_com = CompanyForm()
        form_dep = DepartamentForm()
        form_pos = PositionForm()
        form_user = UserForm()
    return render(request, 'hrapp/signup/signupcompany.html',
                  {'formCom': form_com, 'formDep': form_dep, 'formPos': form_pos, 'formWork': form_user})


def signup_worker(request):
    if request.method == "POST":
        form_user = UserForm(request.POST)
        if form_user.is_valid():
            form_user.save()
            user = User.objects.get(username=form_user.data['username'])
            Worker.objects.create(user=user, role='worker', vakant=True)
            print('Доходит')
            # user = authenticate(username=form.data['username'], password=form.data['password1'])
            # login(request, user)
            return redirect('home')
    else:
        form_user = UserForm()
    return render(request, 'hrapp/signup/signupworker.html', {'formWork': form_user})


def sign_in(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.data['username'], password=form.data['password'])
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form = UserLoginForm
                return render(request, 'hrapp/signup/sign_in.html', {'form': form})
    form = UserLoginForm
    return render(request, 'hrapp/signup/sign_in.html', {'form': form})


def sign_out(request):
    logout(request)
    return redirect('home')


def freelist(request):
    worker = Worker.objects.get(user=request.user)
    freeworkerlist = Worker.objects.filter(vakant=True)
    return render(request, 'hrapp/worklist/freelist.html', {'worker': worker, 'fwl': freeworkerlist})


def workerdetale(request, pk):
    worker = Worker.objects.get(pk=pk)
    return render(request, 'hrapp/worklist/workerdetale.html', {'worker': worker})


def companylist(request):
    worker = Worker.objects.get(user=request.user)
    workercompanylist = Worker.objects.filter(
        position__departament__company=worker.position.departament.company)
    return render(request, 'hrapp/worklist/companylist.html', {"companylist": workercompanylist})


def departamentlist(request):
    worker = Worker.objects.get(user=request.user)
    departamentlist = Departament.objects.filter(company=worker.position.departament.company)
    return render(request, 'hrapp/worklist/departamentlist.html', {'departamentlist': departamentlist})


def departamentdetale(request, pk):
    departament = Departament.objects.get(pk=pk)
    positionlist = Position.objects.filter(departament=departament)
    return render(request, 'hrapp/worklist/departamentdetale.html', {'positionlist': positionlist})


def positiondetale(request, pk):
    position = Position.objects.get(pk=pk)
    if position.vakant == False:
        worker = Worker.objects.get(position=position)
        return render(request, 'hrapp/worklist/positiondetale.html', {'worker': worker, 'position': position})
    return render(request, 'hrapp/worklist/positiondetale.html', {'position': position})


def lay_off(requerst, pk):
    worker = Worker.objects.get(pk=pk)
    worker.lay_off()
    return render(requerst, 'hrapp/lay_off.html', {})


def put_on_hold(request, pk):
    if request.method == "POST":
        worker = Worker.objects.get(pk=pk)
        admin = Worker.objects.get(user=request.user)
        chocesform = PositionChoicesForm(request.POST)
        chocesform.fields['position'] = forms.ModelChoiceField(
            Position.objects.filter(departament__company=admin.position.departament.company).filter(vakant=True)
        )
        worker.position = Position.objects.get(pk=chocesform.data['position'])
        worker.vakant = False
        worker.save()
        position = Position.objects.get(pk=worker.position.pk)
        position.vakant=False
        position.save()
        message = 'Сотруднику присвоена новая должность'
        return redirect(home)
    else:
        worker = Worker.objects.get(pk=pk)
        admin = Worker.objects.get(user=request.user)
        chocesform = PositionChoicesForm(request.POST)
        chocesform.fields['position'] = forms.ModelChoiceField(
            Position.objects.filter(departament__company=admin.position.departament.company).filter(vakant=True)
        )
    return render(request, 'hrapp/worklist/put_on_hold.html', {'worker': worker, 'choicesform': chocesform})
