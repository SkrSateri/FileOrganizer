from django.shortcuts import render, redirect

# Create your views here.

def home_view(request, *args, **kwargs):
    #print(request.session.get('username'))
    #session check
    if request.session.get('username') == None:
        return redirect('login')
    else:
        None
    #session check end

    username = "Hello " + request.session.get('name') + " " +request.session.get('surname')
    context = {
        'username': username,
    }
    return render(request, 'home.html', context)
