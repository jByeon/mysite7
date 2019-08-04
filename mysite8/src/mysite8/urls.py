"""mysite8 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
'''
urls.py : 웹 프로젝트가 실행될 때 웹 클라이언트가 요청을 한 인터넷 주소에 해당하는 view클래스/함수를 호출하기 위한 등록 파일

view 클래스/함수를 등록할 때는 urlpatterns 변수의 요소로 추가하면 됨.
    요소로 추가할 때는 path 함수를 사용
    path(웹 클라이언트가 요청할 url주소(문자열), 호출될 view클래스/함수 이름)
'''

from django.contrib import admin
#include : 다른 URLConf파일을 등록할 때 사용하는 함수
#path(시작문자열, include(urls.py가 있는 위치)) : 시작문자열로 요청하는 모든 인터넷주소는 include안에 있는 urls.py가 처라할 수 있도록 등록함
    # ex) path('test/', include(vote.urls')) -> 127.0.0.1:8000/test/로 시작하는 모든 요청들을 vote폴더의 urls.py에서 처리할 수 있도록 등록
from django.urls import path, include
#등록할 view함수 import
#vote/views.py에 존재하는 test함수를 import
from vote.views import test, test_value, test_input, main, detail, vote, result, q_registe, q_update, q_delete, c_registe, c_update, c_delete

urlpatterns = [
    path('a1/', admin.site.urls),
    path('', test),
    path('value/', test_value),
    #127.0.0.1:8000/숫자(int)/로 요청하는 처리는 test_input 함수를 호출함
        #호출할 때, 이용자가 입력한 숫자(int)값을 number 변수의 인자값으로 사용 <타입(ex. int):변수명>
    path('<int:number>/', test_input),
    #path 함수의 name 매개변수 : 등록된 view의 별칭을 지정하는 매개변수
        #템플릿 : {% url '별칭의 이름(문자열)'  매개변수%}
        #view : reverse 함수로 별칭 기반의 사이트주소 추출 가능
    path('vote/', main, name = 'main'),
    #127.0.0.1:8000/vote/숫자/
    path('vote/<int:q_id>/', detail, name = 'detail'),
    path('vote/vote/', vote, name = 'vote'),
    #127.0.0.1:8000/vote/result/Choice객체의 id숫자/
    path('vote/result/<int:c_id>/', result, name = 'result'),
    path('vote/qr/', q_registe, name = 'qr'), 
    path('vote/qu/<int:q_id>/', q_update, name='qu'),
    path('vote/qd/<int:q_id>/', q_delete, name='qd'),
    path('vote/cr/', c_registe, name = 'cr'),
    path('vote/cu/<int:c_id>/', c_update, name='cu'),
    path('vote/cd/<int:c_id>/', c_delete, name='cd'),
    
    #127.0.0.1:8000/cl/로 시작하는 요청들은 customlogin/urls.py에서 처리
    path('cl/', include('customlogin.urls')),
    
    #127.0.0.1:8000/auth/로 시작하는 요청들을 social_django app의 urls.py에서 처리
        #include함수의 namespace : 해당 urls.py에 지정된 app_name 값을 사용하지 않고 새로운 그룹명(별칭)을 지정
    path('auth/', include('social_django.urls', namespace = 'social')),
    
    #127.0.0.1:8000/blog/로 시작하는 요청들을 blog/urls.py에서 처리
    path('blog/', include('blog.urls'))
    
]

#setting.py 변수값을 사용할 수 있도록 import
from django.conf import settings
#MEDIA_URL과 MEDIA_ROOT를 연결하기 위한 함수 import
from django.conf.urls.static import static
#'/files/'로 시작하는 모든 요청은 파일 업로드/다운로드 처리로 설정
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
