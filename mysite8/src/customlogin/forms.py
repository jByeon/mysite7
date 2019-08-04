'''
Created on 2019. 7. 28.

@author: 405-6
'''
#Django에서 기본적으로 제공해주는 회원관리app에서 User 모델 클래스를 연동하여, 회원관리 및 로그인 폼을 정의함
    #django.contrib.auth : Django에서 회원관리를 하는 app 경로
from django.contrib.auth.models import User
from django import forms


#회원가입 form 정의
class SignupForm(forms.ModelForm):
    #모델 클래스 변수 외에 비밀번호 확인란을 추가
        #forms.XXXField : 폼 클래스에 사용자 입력공간을 정의할 때 사용.
            #모델 클래스에서 사용한 models.XXXField와 기능과 이름이 유사함.
        #label 매개변수 : 해당 입력공간의 설명란을 정의하는 매개변수.
            #기본값은 변수명으로 설정됨.
        #위젯 : 데이터 저장 형식 외에 사용자의 입력타입을 변환하는 것
            #비밀번호 작성란은 텍스트값을 입력받기 때문에 type=text로 되어있지만 비밀번호 타입으로 바꿔주는 작업은 위젯을 통해 할 수 있음
            #forms.XXXInput
    password_check = forms.CharField(max_length=100, 
                                     label='비밀번호 확인',
                                     widget = forms.PasswordInput())
    
    #입력란의 순서를 저장하는 변수
    field_order = ['username', 'password', 'password_check', 'last_name', 'first_name', 'email']
    
    class Meta:
        model = User
        fields = ['username', 'password', 'last_name', 'first_name', 'email']
        #모델 클래스에 정의된 변수를 대상으로 위젯 적용할 때 사용하는 변수
        widgets = {
            #'변수이름':적용할 위젯(XXXInput클래스 객체)
            'password':forms.PasswordInput()
        }
        
#로그인 form 정의
class SigninForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password':forms.PasswordInput()
        }
        
        