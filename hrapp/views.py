from django.shortcuts import render, redirect
from hrapp.forms import CompanyForm, DepartamentForm, PositionForm \
    , UserForm, UserLoginForm, PositionChoicesForm, AddDepartament, AddPositionForm, RoleForm, ProfileForm, SearchForm
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
        if worker.vakant:
            worker.position = Position.objects.get(pk=chocesform.data['position'])
            worker.vakant = False
            worker.save()
            position = Position.objects.get(pk=worker.position.pk)
            position.vakant = False
            position.save()
        else:
            oldposition = Position.objects.get(pk=worker.position.pk)
            oldposition.vakant = True
            oldposition.save()
            worker.position = Position.objects.get(pk=chocesform.data['position'])
            worker.vakant = False
            worker.save()
            position = Position.objects.get(pk=worker.position.pk)
            position.vakant = False
            position.save()
        return redirect('worker_detale', pk=pk)
    else:
        worker = Worker.objects.get(pk=pk)
        admin = Worker.objects.get(user=request.user)
        chocesform = PositionChoicesForm(request.POST)
        chocesform.fields['position'] = forms.ModelChoiceField(
            Position.objects.filter(departament__company=admin.position.departament.company).filter(vakant=True)
        )
    return render(request, 'hrapp/worklist/put_on_hold.html', {'worker': worker, 'choicesform': chocesform})


def adddepartament(request):
    form = AddDepartament(request.POST)
    message = ''
    if request.method == "POST":
        if form.is_valid():
            worker = Worker.objects.get(user=request.user)
            company = Company.objects.get(pk=worker.position.departament.company.pk)
            Departament.objects.create(title_dep=form.data['title'], company=company)
            message = 'Отдел добавлен'
            form = AddDepartament()
            return redirect('adddepartament')
    return render(request, 'hrapp/add/adddepartament.html', {'form': form, 'message': message})


def AddPosition(request):
    form = AddPositionForm(request.POST)
    message = ''
    worker = Worker.objects.get(user=request.user)
    form.fields['departament'] = forms.ModelChoiceField(
        Departament.objects.filter(company=worker.position.departament.company, ),
        label='Отдел',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    if request.method == "POST":
        if form.is_valid():
            message = 'Должность добавлена'
            Position.objects.create(
                title_pos=form.data['title'],
                departament=Departament.objects.get(pk=form.data['departament']),
                vakant=True)
            form = AddPositionForm()
            return render(request, 'hrapp/add/addposition.html', {'form': form, 'message': message})
    return render(request, 'hrapp/add/addposition.html', {'form': form, 'message': message})


def rolechoices(request, pk):
    if request.method == "POST":
        formchoices = RoleForm(request.POST)
        worker = Worker.objects.get(pk=pk)
        worker.role = formchoices.data['role']
        worker.save()
        return redirect('worker_detale', pk=pk)
    formchoices = RoleForm(request.POST)
    return render(request, 'hrapp/add/rolechoices.html', {'formchoices': formchoices})


def profile(request, pk):
    user = User.objects.get(pk=pk)
    worker = Worker.objects.get(user=user)
    if request.method == "POST":
        formprofile = ProfileForm(request.POST)
        formprofile.fields['firstname'] = forms.CharField(label=(u'ИМЯ'), max_length=100,
                                                          widget=forms.TextInput(
                                                              attrs={'class': 'form-control',
                                                                     'value': user.first_name}))
        formprofile.fields['soname'] = forms.CharField(label=(u'ФАМИЛИЯ'), max_length=100,
                                                       widget=forms.TextInput(
                                                           attrs={'class': 'form-control', 'value': user.last_name}))
        formprofile.fields['education'] = forms.CharField(label=(u'ОБРАЗОВАНИЕ'), max_length=400,
                                                          widget=forms.TextInput(
                                                              attrs={'class': 'form-control',
                                                                     'value': worker.education}))
        formprofile.fields['about'] = forms.CharField(label=(u'НАВЫКИ И УМЕНИЯ'), max_length=1200,
                                                      widget=forms.Textarea(
                                                          attrs={'class': 'form-control'}), )
        user.first_name = formprofile.data['firstname']
        user.last_name = formprofile.data['soname']
        user.save()
        worker.education = formprofile.data['education']
        worker.about = formprofile.data['about']
        worker.save()
    else:
        formprofile = ProfileForm(initial={'about': worker.about})
        formprofile.fields['firstname'] = forms.CharField(label=(u'ИМЯ'), max_length=100,
                                                          widget=forms.TextInput(
                                                              attrs={'class': 'form-control',
                                                                     'value': user.first_name}))
        formprofile.fields['soname'] = forms.CharField(label=(u'ФАМИЛИЯ'), max_length=100,
                                                       widget=forms.TextInput(
                                                           attrs={'class': 'form-control', 'value': user.last_name}))
        formprofile.fields['education'] = forms.CharField(label=(u'ОБРАЗОВАНИЕ'), max_length=400,
                                                          widget=forms.TextInput(
                                                              attrs={'class': 'form-control',
                                                                     'value': worker.education}))
        formprofile.fields['about'] = forms.CharField(label=(u'НАВЫКИ И УМЕНИЯ'), max_length=1200,
                                                      widget=forms.Textarea(
                                                          attrs={'class': 'form-control'}))

    return render(request, 'hrapp/profile.html', {'formprofile': formprofile})


def search(request):
    searchform = SearchForm(request.POST)
    if request.method == "POST":
        workers = Worker.objects.filter(user__last_name__contains=searchform.data['search']) | Worker.objects.filter(
            user__first_name__contains=searchform.data['search']) | Worker.objects.filter(
            position__title_pos__contains=searchform.data['search']) | Worker.objects.filter(
            user__username__contains=searchform.data['search'])
        return render(request, 'hrapp/search.html', {'searchform': searchform, 'workers': workers})
    return render(request, 'hrapp/search.html', {'searchform': searchform})
