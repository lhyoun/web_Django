"""pyboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from board import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # localhost/admin을 요청하면 admin.site.urls가 실행되는데
    # 이는 내장된 admin에 해당하는 view를 return해주는 역할을 할거임 아마도
    
    path('movie_save',views.movie_save),
    path('map',views.cctv_map),
    path('main',views.main),
        
    path('insert', views.insert),   # C
    path('write', views.write),     # C
    path("reply_insert", views.reply_insert),   # C
    
    path('detail',views.detail),    # R
    
    path('', views.list),           # R
    # localhost/ 로 요청하면 views.list를 실행
    # view.list는 views.py안에 있고 그 함수를 실행해서 그에 해당하는 view를 return받음
    path("download", views.download),   # R
    
    
    path('update', views.update),   # U
    
    path('wordcloud', views.wordcloud),
    
    path('delete', views.delete),   # D
    
    path('chart', views.chart),
    
]
