from django.contrib import admin
# 추가할 모델 클래스가 있는 파이썬 파일 import
    #vote/models.py에 있는 Question 클래스를 접근할 수 있도록 import함
from vote.models import Question, Choice

# Register your models here.
'''
admin.py : 완성된 모델 클래스를 관리자 사이트에서 조회/삽입/삭제/수정/검색 작업을 수행하기 위해 모델 클래스를 등록하는 파이썬 파일
내부적 코드로 공개하지 않고 작업하고 싶으면 작성X

admin.site.register(모델 클래스) : 해당 모델 클래스를 관리자 사이트에서 접근할 수 있도록 허용하는 함수
'''

admin.site.register(Question)
admin.site.register(Choice)