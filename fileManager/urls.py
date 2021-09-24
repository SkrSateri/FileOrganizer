"""fileManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from account.views import createUser_view, login_view, sessionLogout_view
from home.views import home_view
from search.views import searchFile_view, uploadFile_view, downloadFile_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('createUser/', createUser_view, name = 'createUser'),
    path('home/', home_view, name = 'home'),
    path('login/', login_view, name = 'login'),
    path('searchFile/', searchFile_view, name = 'searchFile'),
    path('uploadFile/', uploadFile_view, name = 'uploadFile'),
    path('logout/', sessionLogout_view, name = 'logout'),
    path('<int:oid>', downloadFile_view, name = 'downloadFile'),
]
