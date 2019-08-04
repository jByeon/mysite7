from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

'''
views.py : MTV 패턴 중 실질적인 데이터 추출, 연산, HTML 전달 등의 기능이 구현되는 파일
view 기능 구현할 때는 클래스/함수를 정의해서 사용할 수 있음

함수를 정의해 view의 기능을 구현할 때는 첫 번째 매개변수가 필수적으로 있어야 함

request : 웹 클라이언트의 요청정보가 저장된 매개변수
    request 안에는 <form>을 바탕으로 사용자가 입력한 값 혹은 로그인정보, 요청방식 등이 변수형태로 저장되고 있음
'''
##테스트용 view 함수
def test(request):
    #render(request, HTML파일경로, dict)
    #해당 요청을 보낸 웹 클라이언트에게 전송할 HTML파일을
    #dict 데이터로 편집한 뒤 전송하는 함수.
    #view 함수는 반드시 HTML파일 혹은 다른 사이트 주소, 파일 데이터를 return 시켜야 함
    return render(request, 'test.html', {})

#view함수가 템플릿이 HTML을 변경할 수 있도록 변수값 전달
def test_value(request):
    #render함수 인자값으로 사용할 dict형 데이터 생성(key값은 알파벳 문자열만 읽을 수 있음)
    dict = {'a':'홍길동님', 'b':[1,2,3,4,5]}
    return render(request, 'test_value.html', dict)

#view함수가 request 외에 추가 매개변수를 사용할 때
def test_input(request, number):
    print (number)
    return render(request, 'test_input.html', {'a':number})

##메인화면 구성 - DB에 저장된 Question 객체를 바탕으로 HTML을 전달해주는 기능을 함수로 생성

#Question 모델 클래스 import
from vote.models import Question, Choice

def main(request):
    #DB에 저장된 모든 Question 객체를 추출
    q = Question.objects.all()
    print(q)
    '''
    Question.objects : DB에 저장된 Question 객체들에 접근할 때 사용하는 변수.
    객체에 접근할 때는 4가지 함수로 접근할 수 있음
        all() : DB에 저장된 모든 객체를 리스트 형태로 추출
        get(조건) : DB에 저장된 객체 중 조건을 만족하는 객체 1개를 추출
        filter(조건) : DB에 저장된 객체 중 조건을 만족하는 모든 객체를 리스트 형태로 추출
        exclude(조건) : DB에 저장된 객체 중 조건을 만족하지 않는 객체를 리스트 형태로 추출
    '''
    #추출된 Question 객체를 HTML 편집에 사용할 수 있도록 전달
    return render(request, 'vote/main.html', {'q':q})

#웹 클라이언트가 요청한 Question 객체 한개와 연결된 Choice 객체 추출
#q_id : 웹 클라이언트가 요청한 Question 객체의 id 변수값
def detail(request, q_id):
    #Question 객체를 한개 추출. id 변수값이 q_id와 같은 조건
    q = Question.objects.get(id=q_id)
    #추출한 Question 객체와 연동된 Choice 객체들을 추출
    #ForeignKey로 연결된 Question객체가 Choice객체들을 대상으로 추출 함수를 사용하려면 객체.Choice_set.추출함수 명령사용
        #ForeingKey로연결된객체.ForeignKey로연결한모델클래스명(소문자)_set.추출함수(all, get, ...)
    c = q.choice_set.all()
    print(q)
    print(c)
    #HTML코드로 추출한 객체들을 전달
    return render(request, 'vote/detail.html', {'q' : q,'c' : c})

#detail 화면에서 웹 클라이언트가 선택한 Choice 객체 id로 투표 진행
#@login_required : 비 로그인 상태일 때 해당 뷰 함수를 요청하면, settings.py에 지정된 로그인 페이지로 리다이렉트함
@login_required
def vote(request):
    #요청한 방식이 post를 사용했는지 확인하는 조건문
        #request.method : 웹 클라이언트의 요청방식을 저장한 변수
        #'GET' 또는 'POST' 문자열(대문자)을 저장하고 있음
    if request.method == 'POST':
        #post 요청으로 들어온 데이터 중 name == select에 저장된 값을 추출
            #POST 요청으로 들어온 데이터는 request.POST에 dict형으로 저장됨
            #GET 요청으로 들어온 데이터는 request.GET에 dict형으로 저장됨
        #<form>태그에 작성된 사용자입력을 추출할 때는 name속성에 적힌 문자열로 추출할 수 있음
        print(request.POST)
        c_id = request.POST.get('select')
        
        #추출된 값을 활용해 Choice객체(select값을 id변수에 저장한 객체) 한개를 추출
        c = Choice.objects.get(id=c_id)
        
        #추출한 Choice 객체에 votes변수값을 +1 누적
        c.votes += 1

        #변경된 값을 DB에 알려줌
        c.save()
        
        #result view함수의 주소를 웹 클라이언트에게 전송
        #return HttpResponseRedirect('/vote/result/%s/' % c.id)
        #별칭 기반으로 result view함수의 URL을 추출 및 전달
            #url = reverse('result', args=(c.id,))
            #return HttpResponseRedirect(url)
        return HttpResponseRedirect(reverse('result', args=(c.id,)))
        '''
        HttpResponseRedirect(URL문자열) :
            웹 클라이언트에게 HTML이나 파일을 전달하는 것이 아닌 
            다른 view함수의 URL 주소를 넘겨주는 클래스.
            웹 클라이언트가 redirect 주소를 받으면 해당 주소로 웹서버에게 재 요청을 함.
        reverse('별칭', args=()) :
            url.py에서 등록한 별칭으로 url주소를 반환하는 함수.
            등록한 view함수가 매개변수를 요구하면 args를 사용.
        '''
    

#Choice객체의 id를 바탕으로 설문 결과를 출력
def result(request, c_id):
    #c_id기반의 Choice객체 한개 찾기
    c = Choice.objects.get(id=c_id)
    
    #Choice객체와 연동된 Question객체 추출
        # 틀림 >> q = c.choice_set.get(id=c_id)
    q = c.q #혹은 Question.objects.get(id=c.q.id)
    
    print('c.q:', c.q)
    print('q:', q)
    
    #Question객체와 연결된 모든 Choice객체 추출
    c_list = q.choice_set.all() 
    
    #결과 화면 HTML에 Question객체와 Choice객체 리스트 전달
    return render(request, 'vote/result.html', {'q' : q, 'c_list' : c_list})


#Question 객체 추가 함수
    #GET - Question 객체를 생성할 때 사용할 변수값을 입력할 수 있는 input태그와 form태그(POST방식 요청)를 사용자에게 제공
    #POST - 사용자가 입력한 데이터를 바탕으로 Question객체를 생성 및 DB에 저장
from vote.forms import QuestionForm
@login_required
def q_registe(request):
    #사용자 요청이 GET인지 POST인지 구분
    if request.method == 'GET':
        #QuestionForm의 객체를 생성
            #QuestionForm 객체를 생성할 때 입력값이 없는 형태로 생성하면 input태그에 아무런 값도 입력되어있지 않은 상태의 객체가 생성됨
        form = QuestionForm()
        
        #객체를 바탕으로 HTML코드로 변환
            #as_p, as_table, as_ul 함수 : form객체에 입력할 수 있는 공간들을 <input>태그로 변환하면서 <p>, <tr>과 <td>, <li> 태그로 감싸주는 기능이 있는 함수
        rendered = form.as_p()
        print(rendered)
        
        #변환값을 HTML파일에 전달
        return render(request, 'vote/q_registe.html', {'rendered':rendered})
        
    elif request.method == 'POST':
        #QuestionForm 객체를 생성 - 사용자 입력을 바탕으로 생성
        form = QuestionForm(request.POST)
        
        #QuestionForm 객체와 연동된 Question 객체를 생성 및 DB에 저장
            #form.save(commit=False) : 연동된 모델 클래스의 객체로 변환만 하는 함수
            #form.save() : 연동된 모델 클래스의 객체를 생성 및 DB에 저장
        new_q = form.save() 
        print(new_q)
        
        #생성된 Question 객체의 id 값으로 detail뷰의 링크를 전달
        return HttpResponseRedirect(
            reverse('detail', args=(new_q.id,))
        )

#Question 객체 수정 함수
    #q_id : 사용자가 수정할 대상(question)의 id값
@login_required
def q_update(request, q_id):
    #수정할 question 객체 추출
    #get_object_or_404 : 모델 클래스의 객체들 중 id변수값을 이용해 객체 한개를 추출하는 함수.
    #   단, 해당 id값으로 된 객체가 없는 경우 사용자 요청에 잘못이 있는 것으로 판단하여 404에러 페이지를 전달함 
    q = get_object_or_404(Question, id=q_id)
    
    #post인지 get인지 구분
        #get요청시 QestionForm객체 생성 - 수정할 객체를 바탕으로 생성
    if request.method == 'GET':
        #form 클래스 객체 생성 시 instance 매개변수에 연동된 객체를 전달하면, 해당 객체가 가진 값을 input태그에 채운상태로 폼 객체가 생성됨
        form = QuestionForm(instance=q)
        #as.table() : 각 입력 공간과 설명을 <tr>과 <td>로 묶어주는 함수
        result = form.as_table()

        return render(request, 'vote/q_update.html', {'result':result})
        
        #post요청시 QestionForm객체 생성 - 수정할 객체 + 사용자 입력
    elif request.method == 'POST':
        #수정대상 객체와 사용자 입력으로 폼 객체 생성 시, 기존 객체 정보를 사용자 입력으로 수정한 상태의 폼 객체가 생성됨
        form = QuestionForm(request.POST, instance=q)
        #사용자 입력으로 수정한 결과를 DB에 반영
        form.save()

        return HttpResponseRedirect(
            reverse('detail', args=(q_id,))
        )

#Question 객체 삭제 함수
@login_required
def q_delete(request, q_id):
    q = get_object_or_404(Question, id=q_id)
    
    #get - '정말로 지우시겠습니까'가 뜨는 HTML 전달
    if request.method == 'GET':
        return render(
            request, 'vote/q_delete.html', {'q':q}
        )

    #post - DB에서 삭제하는 처리 및 메인 페이지 주소를 전달
    elif request.method == 'POST':
        #추출한 Question 객체를 DB에서 제거
        print('삭제할 대상의 id 변수값:', q.id)
        q.delete() #DB에서 해당 객체 정보를 제거하는 함수
        #삭제하더라도 id 변수값을 제외한 변수들 값은 사용할 수 있음 
        print('삭제된 대상의 id 변수값:', q.id)
        print('삭제된 대상의 다른 변수값:', q.title)
    
        return HttpResponseRedirect(
            reverse('main')
        )



from vote.forms import ChoiceForm

#Choice 객체 추가
@login_required
def c_registe(request):
    #GET - 빈 ChoiceForm 객체 생성 및 html파일 전달
    if request.method == 'GET':
        form = ChoiceForm()
        
        asdf = form.as_p()
        
        return render(request, 'vote/c_registe.html', {'asdf':asdf})
    #POST - 사용자입력 기반의 ChoiceForm객체 생성 및 DB에 객체 저장 + detail 뷰로 이동
    if request.method == 'POST':
        form = ChoiceForm(request.POST)
        
        new_c = form.save()
        
        return HttpResponseRedirect(
            reverse('detail', args=(new_c.q.id,))
        )

    
#Choice 객체 수정
#c_id : 수정할 Choice 객체의 id값
#공통 : 수정할 Choice 객체를 추출
 
@login_required
def c_update(request, c_id):
    c = get_object_or_404(Choice, id=c_id)
    #GET - 추출한 Choice 객체 기반의 ChoiceForm 객체 생성 및 html 전달
    if request.method == 'GET':
        #form = ChoiceForm(instance=c)
        #qwer = form.as_ul()
        qwer = ChoiceForm(instance=c).as_ul()
        detail_url = reverse('detail', args=(c.q.id,))
        
        return render(
            request, 
            'vote/c_update.html', 
            #qwer : form태그 안에 들어갈 input태그 문자열
            #q_id(옵션) : HTML코드에 detail페이지로 이동하기 위한 Question객체의 id값 전달
            #detail_url : 해당 수정페이지와 연관된 detail페이지 주소 전달
            {
                'qwer':qwer,
                'q_id':c.q.id,
                'detail_url': detail_url
            }
        )
    #POST - 추출한 Choice 객체 + 사용자 입력 기반의 ChoiceForm객체 생성 및 수정사항을 DB에 반영 + detail 뷰로 이동
    if request.method == 'POST':
        form = ChoiceForm(request.POST, instance = c)
        form.save()
        return HttpResponseRedirect(
            reverse('detail', args=(c.q.id,))
        )

#Choice 객체 삭제    
#c_id : 삭제할 Choice 객체의 id값
#공통 : 삭제할 Choice객체 추출
@login_required
def c_delete(request, c_id):
    c= get_object_or_404(Choice, id=c_id)
    #DB에서 제거 및 id 변수값 삭제
    c.delete()
    return HttpResponseRedirect(
        reverse('detail', args=(c.q.id,))
    )
    
    
    
#c = get_object_or_404(Choice, c.id)
    