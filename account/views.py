from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CreateUserForm, LoginForm
from .models import User
from django.contrib.auth.hashers import make_password, check_password
from commonClasses.resultMessages import ResultMessage

# Create your views here.

def createUser_view(request, *args, **kwargs):
    #session check
    if request.session.get('username') == None:
        return redirect('login')
    else:
        None
    #sessionCheckLog(request)

    form = CreateUserForm(request.POST or None)
    message = None

    if form.is_valid():
        nameForm = request.POST.get('name')
        surnameForm = request.POST.get('surname')
        usernameForm = request.POST.get('username')
        passwordForm = request.POST.get('password')
        isAdminForm = request.POST.get('isAdmin')
        passwordEncyripted = make_password(passwordForm)
        if isAdminForm == None:
            isAdminForm = False
        else:
            isAdminForm = True
        #print (isAdminForm)
        try:
            userFromDatabase = User.objects.get(username = usernameForm)
            message = ResultMessage(False, "An user with this username already exist!")
        except:
            newUser = User(name = nameForm, surname = surnameForm, username = usernameForm, password = passwordEncyripted, isAdmin = isAdminForm)
            newUser.save()
            form = CreateUserForm()
            message = ResultMessage(True, "New user created successfully!")
    context = {
        'form': form,
        'message': message
    }
    return render(request, 'createUser.html', context)

def login_view(request, *args, **kwargs):
    #request.session.flush()
    #session check
    if request.session.get('username') == None:
        None
    else:
        return redirect('home')
    #sessionCheckLog(request)

    form = LoginForm(request.POST or None)
    errorMessage = None
    username = ""
    if form.is_valid():
        usernameForm = request.POST.get('username')
        passwordForm = request.POST.get('password')
        try:
            userFromDatabase = User.objects.get(username = usernameForm)
            if check_password(passwordForm, userFromDatabase.password):
                request.session['username'] = userFromDatabase.username
                request.session['name'] = userFromDatabase.name
                request.session['surname'] = userFromDatabase.surname
                username = request.session.get('name') + request.session.get('surname')
                #print('Correct!')
                return redirect('home')
            #else:
                #print('Wrong!')
        except:
            form =LoginForm(request.POST)
            errorMessage = "User not found"
    context = {
        'form': form,
        'errorMessage': errorMessage,
        'username': username
    }
    return render(request, 'login.html', context)

def sessionLogout_view(request, *args, **kwargs):
    request.session.flush()
    return redirect('login')