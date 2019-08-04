'''
Created on 2019. 7. 28.

@author: 405-6
'''
from django.urls.conf import path
from customlogin.views import signup, signin, signout

#하위 urls.py를 정의 및 해당 app의 뷰 함수를 등록
    #등록 시 app_name과 urlpatterns 두 가지를 사용함
        #app_name : 별칭 기반으로 url을 찾을 때 사용하는 그룹 이름
        #urlpatterns : path함수로 뷰함수를 등록 및 관리하는 변수
            # ex) cl 그룹 명에 signup 별칭을 가진 뷰함수를 찾을 경우 url 'cl(그룹명):signup(별칭)'
app_name = 'cl'
urlpatterns = [
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),
    
]