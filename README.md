# pjt_book_review_board

읽은 책들을 올리고 리뷰를 올릴수 있는 게시판





## [04.03] 1일차  

### 계획

장고를 이용해서 책 리뷰를 올릴수있는 게시판을 만든다.

리뷰에는 좋아요를 할수있고, 댓글 역시 달을수있다.

책이 종류가 많은 만큼 카테고리를 지정해서 올릴수있도록하고 탭을 통해서 분류를 할수있게 한다.



- 계획한 index 페이지



![image-20210403202721241](README.assets/image-20210403202721241.png)



- 상세페이지



![image-20210403201436344](README.assets/image-20210403201436344.png)





### 무엇을 구현할지

- 부트스트랩을 적극적으로 이용할것 ( nav bar 와 책을 나타내는걸 카드로 나타낸다.)

- 책

  :책사진, 책이름, 저자, 간단한 소개내용으로 정보가 이루어져있다.

- 좋아요

  : 로그인 했다면 좋아요, 싫어요를 고를 수있고 그 수를 집계해서 index에 표현해준다.

- 회원가입

  :닉네임, 비밀번호 입력으로 끝낸다.

- 댓글

  : 로그아웃이되도 리뷰는 볼수있되, 댓글은 달지 못하도록한다.

  : 댓글을 달을때 별점을 매길수있다. 5점 만점으로 제한을 두고

  : 댓글들의 값을 평균을 내서 인덱스와 상세 페이지에 나타낼수있게함

  : 그러면 댓글에 필요한 요소는 유저, 댓글내용, 별점

- 검색

  : 책이름으로 url이 이동할수잇게 하고 없으면 404 에러뜨게 만든다.

- 카테고리

  : 책마다 종류가 다양하므로 카테고리를 만들어서 탭모양으로 바뀔수있게 만든다.



### 고민

- 회원가입하는 것이 의미가 있을까?

  : 회원가입을 만든이유는 무분별한 별점테러같은것이 없도록 번거로운 과정을 추가해서 막으려고 한것인데 그외 추가적인 기능없이 ''그것''만을 위해 있는것이 맞는가?

  - 추가적인 기능 생성: 프로필을 만들고 좋아요 리스트를 만들어서 추가기능 구현 

  - 회원가입삭제 : 익명의 닉네임으로 댓글을 달고 별점을 달수있게 만들기



## [04.05] 2일차



### 기본적인 틀을 제작

![image-20210405221106268](README.assets/image-20210405221106268.png)



- book_review_site 로 프로젝트를 시작하였고

- 추가적인 앱을 책의 리뷰를 쓰는 reivews와 사용자의 정보를 넣을 수있는 accounts를 생성했다.
- book_review_site에는 index.html을 만들어 부트스트랩의 starter templates 만 넣어주었다.
- book_review_site의 urls.py에서 리뷰와 어카운트의 url로 진행할수있게 include 해주었다.



### 모델 설정

- 기본적인 유저 커스터마이징
- accounts/model.py

```python
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    pass
```

- accounts/forms.py

```python
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = '__all__'
```



- 리뷰와 유저의 모델 설정
- review/model.py

```python
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT) 
    # 올린사람의 정보
    title = models.TextField() # 책제목
    author = models.TextField() # 저자이름
    content = models.TextField() # 책내용
    created_at = models.DateTimeField(auto_now_add=True) # 리뷰 생성날짜
    like_user = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='like_book')
    # 좋아요하는 사람
    
    def __str__(self):
        return self.title #어드민에서는 책제목으로 보이게

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 댓글단 유저의 정보
    Review = models.ForeignKey(Review, on_delete=models.CASCADE) #댓글달은 리뷰의 정보
    content = models.TextField() # 댓글내용
    rank = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)])# 댓글에 점수를 매길수있는데 1점부터 5점까지 매길수있다.
    created_at = models.DateTimeField(auto_now_add=True) # 댓글 생성날짜

    def __str__(self):
        return self.content # 어드민에서 댓글내용으로 파악
```

- reviews/forms.py

```python
from django import forms
from .models import Review, Comment


class Review_Form(forms.ModelForm):

    class Meta:
        model = Review
        fields = '__all__'
    
class Comment_Form(forms.ModelForm):

    class Meta:
        model = Comment
        fields = '__all__'
```

- 고민인 것이 원래는 관리자가 책을 올려주고 거기에대해서 리뷰를 다는 방식으로 하려고 했다. 하지만 관리자가 24시간 책을 찾아서 올리는 것이 아니기 때문에 사용자도 올릴수있도록 하였다.
  - 단 여기서 같은 이름의 책은 올릴수가 없다. (중복을 판별하는것은 책이름과 저자이름) 
- 좀더 제한을 모델에서 줄수있을거라 생각한다. 좀더 찾아보기로 한다.
- 댓글작성시 점수를 줘서 그평균을 리뷰에도 나타나게 해서 리뷰에 랭크를 외래키로 등록해야하는데 에러가생긴다. (그런데 굳이 외래키로 줘야할 이유가 있을까?) 



### migrate

![image-20210405222347186](README.assets/image-20210405222347186.png)



- 일단 migrate가 되는지 확인해 보았고 다음 진행작업에 model 을 한번더 생각해보고 다시 migrate 하겠다.



## [04.09, 04.11] 3, 4일차



### migrate

![image-20210409221041175](README.assets/image-20210409221041175.png)

- 저번 rank에 대한 생각으로 한번 외래키로 넣어서 시도했으나 Review에서 이미 선언되지 않은 Comment의 키를 받아오는 것이 안되는 것같다.
- 그래서 rank의 외래키는 넣어두지않고 Comment의 rank로 표현할수있을거라 생각하기 때문에 외래키는 접어두고 migrate 했다.



### CRUD 구현

모델을 만들었으니 책리뷰글을 **생성**, **읽기**, **업데이트**, **삭제** 하는 기능을 넣어주려고 한다.

- 구현하면서 review 보다는 책에 대한 것이 중점이라고 생각해서 reviews가 아닌 books 로변경했다. 
- accounts 를 구현하게 되면 login-required 같은 인증또한 넣을 예정이다.





- urls.py

![1](README.assets/1.png)



- books/views.py

![2](README.assets/2.png)



### html 구현

views.py 까지 작성하고 나서 html를 작성하려는데 문제가 발생!

html에서 base.html 확장시키려는데 `block`이 먹질 않는다.

버전도 Django html로 되있고 다 정상인데 안될이유가 없는데... 스택오버플로우에서도 답을 찾지 못해서 따로 질문올리고서 다음날 다시 시도했다.

그런데 뭔일있었냐는듯 다음날 그대로 해결되었다. :angry:   뭔가 문제엿던거니..



![image-20210412213041114](README.assets/image-20210412213041114.png)



- html 은 일단 서버에 제대로 나타는지 확인하기 위해서 값을 받고 추후에 꾸밈같은 걸 해줄 예정



- create.html

![3](README.assets/3.png)





- detail.html

![4](README.assets/4.png)



- index.html

![5](README.assets/5.png)



- update.html

![6](README.assets/6.png)



### 생성된 페이지

- index 페이지

![image-20210412004040315](README.assets/image-20210412004040315.png)

- 생성 페이지

![image-20210412004107916](README.assets/image-20210412004107916.png)



### 다음 계획

- 디테일 페이지는 오류가 생긴다. Book_from.pk 가 존재하지 않는다는데 다음 작업때 살펴봐야할 부분이다.
- CRUD 를 마무리 시키고 가능하면 comment 기능도 할수있다면 최대한 할것이다. comment에서 별점을 매겨서 book의 평점을 나타내야하기 때문에 이부분은 고민을 많이 하게 될것같다.



-----------

### [04.26] 5일차



### 문제 해결

Book_from.pk 가 존재하지 않는다 라는 문제를 겪었었는데 book의 pk를 'pk'로 공통적으로 바꿔준 결과 해결되어 detail 페이지를 정상적으로 확인할 수 있었다. 



### index 페이지 개선 (+navbar)

- 기존의 인덱스 페이지가 무엇을 나타내는지 알기 힘들었고 웹페이지상에서 무질서해 보였다.

- 이를 부트스랩의 카드를 가지고 이용해 웹사이트의 책 리뷰들을 그리드 시스템을 통해서 반응형으로 될수있도록 깔끔하게 나타냈다.

  - https://getbootstrap.com/docs/5.0/components/card

- 리뷰 생성의 경우 버튼을 통해서 생성할수있도록 설계했다.

- nav bar의 경우 필요한기능인 index 로 이동하는 'Home' 과 리뷰생성하는 'Create' 을 넣었고

  회원가입과 로그인, 로그아웃은 아직 기능이없지만 추후 구현할 예정이다.

- 카드안의 내용이 넘처서 이부분을 css를 이용해 일정 문장 이상 넘어가면 생략될수있도록 했다.

  - 참고 : https://dheldh77.tistory.com/entry/Django-%EC%9D%B4%EB%AF%B8%EC%A7%80-%EC%97%85%EB%A1%9C%EB%93%9C

    

![image-20210426230942816](README.assets/image-20210426230942816.png)

```html
{% extends 'base.html' %}

{% block content %}
  <div class = "d-grid gap-2 col-4 mx-auto" style= 'margin:20px; height:50px;'>
    <button type="button" class="btn btn-primary"><a href="{% url 'books:create'%}" class="btn" style="color: white;">Create Review</a></button>

  </div> 
  <hr>
  <div class="container">
    <div class="row justify-content-start">
    {% for book in books %}
      <div class='col-4'>
        <div class="card mb-3" style="max-width: 540px; height: 18rem;">
          <div class="row g-0">
            <div class="col-md-4">
              {% if article.image %}
                <img src="{{ book.image.url }}" alt="{{ book.image.url }}">
              {% endif %}
            </div>
            <div class="col-md-8">
              <div class="card-body">
                <h4 class="card-title"><a href="{% url 'books:detail' book.pk %}">{{ book.title }}</a></h4>
                <h6 class="card-text">{{ book.author }}</h6>
                <p class="card-text" 
                style=" height: 10rem; line-height: 1.5;overflow: hidden;display: -webkit-box;-webkit-line-clamp: 7;-webkit-box-orient: vertical;">{{ book.content }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>  
    {% endfor %}
    </div>
  </div>
{% endblock %}
```



### Detail 페이지 개선

- 디테일 페이지에서 제목,저자, 작성시간을 나타낼수있게 하였다.
- 추가적으로 구현하지 못했던 update와 delete 또한 html에 넣어 디테일 페이지에 버튼으로 작동할수있게 하였다.
- index 페이지로 갈수있는 back 버튼을 만들었다.

![image-20210426231004966](README.assets/image-20210426231004966.png)

```html
{% extends 'base.html' %}
{% block content %}
  <hr>
  {% if article.image %}
    <img src="{{ book.image }}" alt="{{ book.image }}">
  {% endif %}
  <p>제목 : {{ book.title }}</p>
  <p>저자 : {{ book.author }}</p>
  <p>내용 : {{ book.content }}</p>
  <p>작성시각 : {{ book.created_at }}</p>
  <hr>
  <a href="{% url 'books:update' book.pk %}" class="btn">UPDATE</a>
  <form action="{% url 'books:delete' book.pk %}" method="POST">
    {% csrf_token %}
    <button class="btn">DELETE</button>
  </form>
  <a href="{% url 'books:index' %}"  class="btn">Back</a>
  <hr>
{% endblock content %}
```



### 문제 - 이미지 업로드

- 이미지를 인덱스의 카드에 보이게 하고 디테일에서 보이게 하려고했으나 에러가 일어난다.

![image-20210426232122511](README.assets/image-20210426232122511.png)

- 이미지파일을 찾지 못하는것 같은데 이부분 다음 프로젝트 진행 시간에 해결해보려한다.



### 다음할일

- 이미지 문제를 해결하면 그다음으로 로그인 로그아웃 회원가입을 구현한다.



-----------



### 필요 링크

- 페이지네이션

  https://getbootstrap.com/docs/5.0/components/pagination/

- 좋아요, 싫어요 폰트

  https://fontawesome.com/icons?d=gallery&p=2&q=thumb

- heroku
- pythonanywhere
- lightsail

