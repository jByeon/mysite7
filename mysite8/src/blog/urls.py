'''
Created on 2019. 8. 3.

@author: 405-6
'''
from django.urls.conf import path
from blog.views import Main, Detail, Posting, post_delete


app_name = 'blog'

urlpatterns = [
    #뷰클래스를 url에 등록할 때는 뷰클래스.as_view()로 등록
    #함수 등록할때는 다른 url.py 참고
        #127.0.0.1:8000/blog
    path('', Main.as_view(), name='main'),
    #DetailView는 특정 모델클래스의 특정 객체를 추출하기 위해 pk(primary key)라는 매개변수를 사용함
        #127.0.0.1:8000/blog/숫자
    path('<int:pk>/', Detail.as_view(), name='detail'),
    
    path('posting/', Posting.as_view(), name='posting'),
    
    path('delete/<int:p_id>', post_delete, name='delete'),
    
    ]

