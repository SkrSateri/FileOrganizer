from django.shortcuts import render, redirect

# Create your views here.

def home_view(request, *args, **kwargs):
    print(request.session.get('username'))
    if request.session.get('username') == None:
        return redirect('login')
    else:
        None
    context = {
    }
    return render(request, 'home.html', context)
