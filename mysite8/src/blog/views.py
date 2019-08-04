from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from blog.models import Post, PostFile, PostImage
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from blog.forms import PostingForm
from django.http.response import HttpResponseRedirect, HttpResponseNotAllowed
from django.urls.base import reverse



# Create your views here.

#글 목록이 뜨는 페이지
    #제네릭 뷰 : 장고에서 제공하는 여러가지 뷰 기능을 구현한 클래스 모음
        #ListView : 특정 모델 클래스의 객체들을 목록화 할 수 있는 기능이 구현된 뷰
class Main(ListView):
    #사용자에게 전달할 HTML파일의 경로
    template_name = 'blog/main.html'
    #리스트로 뽑을 모델 클래스
            #Post 더블클릭해서 import
    model = Post
    #리스트로 뽑은 객체를 HTML에 전달할 때 사용할 이름
            #render함수(request, {xx:})의 xx에 해당
    context_object_name = 'list'
    #한 페이지에 몇개의 객체가 보여질지 설정
    paginate_by = 3

#글 상세보기 페이지
    #DetailView : 특정 모델 클래스의 특정 객체 한개를 추출할 때 사용하는 뷰
class Detail(DetailView):
    #사용자에게 전달할 HTML파일의 경로
    template_name = 'blog/detail.html'
    #리스트로 뽑을 모델 클래스
    model = Post
    #리스트로 뽑은 객체를 HTML에 전달할 때 사용할 이름
    context_object_name = 'obj'


#글 작성 페이지
    #XXXMixin : 뷰 클래스는 데코레이터(@)를 지정할 수 없기 때문에 login_required와 같은 기능을 뷰에 지정하려면 XXXMixin 클래스를 상속받으면 됨.
    #단, 제네릭 뷰를 먼저 상속받은 다음 Mixin 클래스를 상속받아야 정상적으로 기능이 동작함
    #LoginRequiredMixin : login_required 데코레이터와 동일한 기능.(장고에서 제공하며, customizing 가능함 - docs 참조)
from django.contrib.auth.mixins import LoginRequiredMixin

#FormView : 폼 클래스를 바탕으로 사용자에게 입력받아 처리하는 뷰
    #FormView 더블클릭 import
    #클래스 상속 시 Mixin, 제네릭뷰 순서로 받아야함(ex. class Posting(Mixin, 제네릭뷰))
class Posting(LoginRequiredMixin, FormView):
    #사용자에게 전달할 HTML파일 경로
    template_name = 'blog/posting.html'
    #연동할 폼클래스의 이름
    form_class = PostingForm
    #GET방식으로 요청이 들어오면, 등록된 폼클래스의 객체 생성 후 HTML파일과 함께 전달
    #POST방식으로 요청이 들어오면, 사용자의 입력을 바탕으로 폼클래스 객체 생성 후 유효한값인지 확인한 뒤(is_vaild),
    #True값이 반환되면 폼 객체를 저장하는 함수를 호출
    
    #is_vaild() 이후 호출되는 함수를 오버라이딩하여, 사용자가 업로드한 이미지나 파일을 바탕으로 PostImage, PostFile객체를 생성
        #FormView의 POST방식 요청 시 유효한 값일 때 사용되는 form_vaild 함수 오버라이딩
    def form_valid(self, form):
        #Form 객체를 Post 객체로 변환
            #p : 사용자 입력을 바탕으로 category, title, contents변수가 채워져 있는 새로운 Post객체임
                #model.py에 post에는 category, title, contents, user, pub_date가 있음
                #category, title, contents는 사용자가 입력하고, pub_date는 자동생성됨. 
                #빈칸은 원래 저장되지 않으므로(저장 시 에러), contents처럼 blank함수를 써야하나,
                #user에는 지정하지 않았으므로 앞으로 채워야함.
            #commit=False : post객체를 DB에 저장할 때 user변수에 값이 들어있지 않은 상태기 때문에 에러가 발생함.
                #따라서 DB에 저장하지 않고 연동된 모델 클래스의 객체로 변환만 함
        p = form.save(commit=False)
        
        #user 정보를 클라이언트의 유저정보로 대입
            #self.request : 해당 뷰를 요청한 클라이언트의 요청정보가 저장된 변수
            #self.request.user : 요청한 클라이언트의 User모델크래스 객체 저장 변수
        p.user = self.request.user

        #DB에 Post객체 저장
            #user변수에 값이 들어갔으므로 저장할 수 있게됨
        p.save()
              
        #(post객체에 딸려온) 사용자가 업로드한 파일 데이터를 바탕으로 PostFile 객체 생성
            #self.request.FILES : 사용자가 업로드한 파일을 저장한 변수
            #self.request.FILES.getlist(form.py의 name속성 이름(images , files )) : 해당 입력공간에 업로듣된 파일 데이터들을 추출 
            #사용자가 업로드 한 파일의 갯수만큼 반복
        for f in self.request.FILES.getlist('files'):
            #새로운 PostFile (model.py에 있는) 객체 생성 - DB에 저장 X
            pf = PostFile()
            pf.post = p #새로 만들어진 Post객체와 연동
            pf.file = f #사용자가 업로드한 파일을 FileField에 저장
            
            pf.save()
        
        #사용자가 업로드한 이미지 데이터를 바탕으로 PostImage 객체 생성
            #사용자가 'images'입력공간에 업로드한 파일들을 바탕으로 객체 생성
        for i in self.request.FILES.getlist('images'):
            #새로운 PostFile (model.py에 있는) 객체 생성 - DB에 저장 X
            pi = PostImage()
            pi.post = p
            pi.image = i
            
            pi.save()      
        
        #blog:detail 로 리다이렉트
            #새로 만들어진 Post객체의 id값으로 detail뷰의 주소 전달
        return HttpResponseRedirect(
            reverse('blog:detail', 
                    args = (p.id,)
            )
        )

#글 삭제 기능
def post_delete(request, p_id):
    #post객체 한개 추출 get_object_or_404(어느 모델 클래스를 대상으로 추출할거냐, 찾을 변수값이나 조건)
    p = get_object_or_404(Post, id=p_id)
    
    #추출한 객체의 user정보와, 요청한 클라이언트의 user정보를 비교
    if p.user == request.user:
        #자기가 쓴 글을 지우는 요청인 경우, 추출한 객체를 삭제
        p.delete()
        #메인페이지로 이동
        return HttpResponseRedirect(
            reverse(
                'blog:main'
            )
        )
    #자기가 쓴 글이 아닌데 요청한 경우, 404에러 전달
    else:
        return HttpResponseNotAllowed(['GET']) 
