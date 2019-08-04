'''
Created on 2019. 7. 27.

@author: 405-6

HTML에 들어갈 <form>의 <input>을 관리하는 클래스 정의
'''
from django import forms
from vote.models import Question, Choice

#Question 모델 클래스와 연동된 form 클래스 정의
#모델 클래스와 form클래스를 연동시키려면 ModelForm클래스를 상속받아야함
class QuestionForm(forms.ModelForm):
    #ModelForm클래스에서는 meta 클래스를 정의함으로써 어떤 모델클래스와 연동하는지 어떤 변수값을 사용할 것인지를 표현함
    class Meta:
        #model, fields, exclude 변수를 사용함
            #model : 어떤 모델 클래스와 연동했는지 저장
            #fields, exclude 중 한 개의 변수를 통해 사용할 변수를 정의
        model = Question
        fields = ['title'] #Question의 변수 중 title 변수값만 기입할 수 있도록 정의
        #exclude = ['pub_date'] #pub_date를 제외한 나머지 변수들을 기입할 수 있도록 정의
        


#Choice 모델 클래스와 연동된 ChoiceForm 클래스 정의
#q변수와 name변수를 접근할 수 있도록 설정
class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        exclude = ['votes']






        