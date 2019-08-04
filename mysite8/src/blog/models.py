from django.db import models
#django에서 제공하는 회원모델 클래스
    #한명의 User가 여러개의 글을 작성할 수 있도록 foreignKey 설정하기 위해 import
from django.contrib.auth.models import User

# Create your models here.

#글 카테고리 저장 공간(모델 클래스)
class Category(models.Model):
    #카테고리 명 저장 공간
    name = models.CharField('카테고리', max_length=10)
    #객체 출력함수 오버라이딩
    def __str__(self):
        return self.name

#글 내용 저장 공간
class Post(models.Model):
    #Category 모델 클래스 외래키 설정
        #Post가 n Category 가 1인 관계
        #models.PROTECT : Category 모델 객체가 삭제될 때, 연결된 Post 객체가 존재하면, 삭제되지 않도록 막아주는 기능
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    
    #User 모델 클래스 외래키 설정
        #models.CASCADE : User 모델 객체가 삭제될 때 연결된 Post 객체들도 같이 삭제되는 기능
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    #제목
    title = models.CharField('제목', max_length=100)
    
    #글 내용
        #TextField : 글자 수 제한이 없는 문자열 저장공간
        #blank, null : XXXField 생성자의 공통 매개변수
            #blank : form 태그에서 필수로 입력하지 않아도 영역을 설정(default는 False)
            #null : DB에 저장할 때 값이 없어도 저장되도록 설정(default는 False)
    contents = models.TextField('내용', blank=True, null=True)
    
    #생성일
        #auto_now_add = True : 객체 생성 시 서버의 시간을 자동으로 입력
    pub_date = models.DateField('작성일', auto_now_add = True)

    def __str__(self):
        return self.title
    
    #Meta 클래스를 정의해서 정렬 순서를 지정
    class Meta:
        #정렬순서 지정
            #정렬에 사용할 변수들을 list형태로 지정
            #변수 이름 앞에 -를 붙이면 내림차순으로 정렬
        ordering = ['-pub_date']

#글에 포함된 이미지 저장 공간
class PostImage(models.Model):
    #어떤 글의 객체인지 연결
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    #이미지 파일 저장 공간
        #ImageField : 이미지를 저장할 때 사용하는 저장공간
        #upload_to : 클라이언트가 업로드한 파일을 저장 및 접근할 때, 사용할 이미지가 저장된 서버의 하드디스크 경로
            #%y : 서버시간 기준의 년
            #%m : 월
            #%d : 일
    #클라이언트가 이미지를 업로드하면 images를 서버시간의년/월/일 폴더에 저장함
    image = models.ImageField('이미지', upload_to='images/%y/%m/%d')
    
#글에 포함된 파일 저장 공간
class PostFile(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    #클라이언트가 업로드한 파일들은 서버의 files/년/월/일 폴더에 저장됨
    file = models.FileField('파일', upload_to='files/%y/%m/%d')
    
    