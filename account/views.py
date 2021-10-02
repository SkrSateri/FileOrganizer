from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CreateUserForm, LoginForm, searchUserForm
from .models import User
from django.contrib.auth.hashers import make_password, check_password
from commonClasses.resultMessages import ResultMessage

# Create your views here.

def deleteUser_view(request, uid):
    #sessionCheck
    if request.session.get('username') == None:
        return redirect('login')
    if request.session.get('isAdmin') == False:
        return render(request,'notAdmin.html')
    else:
        None
    #session check end

    errorValue = False

    #get the user from database and delete it
    try:
        userToDelete = User.objects.get(id = uid)
        userToDelete.delete()
    except:
        errorValue = True

    #--------
    if errorValue:
        return redirect('searchUser')
    else:
        None
    return redirect('searchUser')

def searchUser_view(request, *args, **kwargs):
    #sessionCheck
    if request.session.get('username') == None:
        return redirect('login')
    if request.session.get('isAdmin') == False:
        return render(request,'notAdmin.html')
    else:
        None
    #session check end

    #declaring form to render
    form = searchUserForm(request.POST or None, use_required_attribute = False)

    #getting values from form and assigning them to the variables
    usernameForm = request.POST.get('username')
    nameForm = request.POST.get('name')
    surnameForm = request.POST.get('surname')
    print(str(nameForm))

    #message decleration
    resultMessage = ResultMessage(None,"resultMessage  somehow not Working")

    #request check
    isRequestExist = False
    if request.POST:
        isRequestExist = True
    else:
        isRequestExist = False

    #trying to find user from database
    if str(nameForm) == "" and str(surnameForm) == "":
        print('username')
        try:
            userQuery = User.objects.filter(username = usernameForm).values('id', 'name', 'surname', 'username', 'isAdmin').order_by('name')
        except:
            userQuery = None
    elif str(usernameForm) == "" and str(surnameForm) == "":
        print('name')
        try:
            userQuery = User.objects.filter(name = nameForm).values('id', 'name', 'surname', 'username', 'isAdmin').order_by('name')
        except:
            userQuery = None
    elif str(usernameForm) == "" and str(nameForm) == "":
        print('surname')
        try:
            userQuery = User.objects.filter(surname = surnameForm).values('id', 'name', 'surname', 'username', 'isAdmin')
        except:
            userQuery = None
    elif str(surnameForm) == "":
        print('username and name')
        try:
            userQuery = User.objects.filter(username = usernameForm, name = nameForm).values('id', 'name', 'surname', 'username', 'isAdmin')
        except:
            userQuery = None
    elif str(nameForm) == "":
        print('username and surname')
        try:
            userQuery = User.objects.filter(username = usernameForm, surname = surnameForm).values('id', 'name', 'surname', 'username', 'isAdmin')
        except:
            userQuery = None
    elif str(usernameForm) == "":
        print('name and surname')
        try:
            userQuery = User.objects.filter(name = nameForm, surname = surnameForm).values('id', 'name', 'surname', 'username', 'isAdmin')
        except:
            userQuery = None
    else:
        print('username, name and surname')
        try:
            userQuery = User.objects.filter(name = nameForm, surname = surnameForm, username = usernameForm).values('id', 'name', 'surname', 'username', 'isAdmin')
        except:
            userQuery = None

    if not userQuery:
        resultMessage = ResultMessage(False, 'There is no user with that name')

    context = {
        'form': form,
        'userQuery': userQuery,
        'resultMessage': resultMessage
    }

    if isRequestExist:
        return render(request, 'manageUsersResult.html', context)
    else:
        None

    return render(request, 'manageUsers.html', context)
        



def createUser_view(request, *args, **kwargs):
    #session check
    if request.session.get('username') == None:
        return redirect('login')
    elif request.session.get('isAdmin') == False:
        return render(request, 'notAdmin.html')
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
                request.session['isAdmin'] = userFromDatabase.isAdmin
                request.session['id'] = userFromDatabase.id
                username = request.session.get('name') + request.session.get('surname')
                print(userFromDatabase.isActive)
                userFromDatabase.isActive = True
                print(userFromDatabase.isActive)
                userFromDatabase.save()
                return redirect('home')
            #else:
                #print('Wrong!')
        except:
            form =LoginForm(request.POST)
            errorMessage = "Password is wrong or user is not exist"
    context = {
        'form': form,
        'errorMessage': errorMessage,
        'username': username
    }
    return render(request, 'login.html', context)

def sessionLogout_view(request, *args, **kwargs):
    try:
        userId = request.session['id']
        userFromDatabase = User.objects.get(id = userId )
        userFromDatabase.isActive = False
        print(userFromDatabase)
        userFromDatabase.save()
    except:
        None
    request.session.flush()
    return redirect('login')