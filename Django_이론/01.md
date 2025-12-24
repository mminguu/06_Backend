# 08. 웹 페이지 만들기

## 개요
Django에서 사용자 요청에 응답하는 페이지를 만드는 방법을 배웁니다.

---

## 08-1. URL 설정하기

### URL 라우팅의 흐름

```
1. 사용자가 브라우저에서 URL 요청
   예: http://127.0.0.1:8000/blog/post/1/

2. Django의 URL 라우터가 요청 URL을 분석

3. urls.py 파일에서 패턴과 매칭

4. 매칭된 뷰 함수/클래스를 실행

5. 응답을 사용자에게 반환
```

### URL 패턴 작성

URL 패턴은 `path()` 또는 `re_path()`로 작성합니다.

#### path() 함수
- 경로 형식의 URL을 간단하게 정의
- Django 2.0 이상에서 권장

```python
from django.urls import path
from . import views

urlpatterns = [
    # 기본 형식: path('경로', 뷰, 이름)
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/create/', views.post_create, name='post_create'),
]
```

#### URL 경로 컨버터

| 컨버터 | 패턴 | 설명 |
|--------|------|------|
| str | [^/]+ | 기본값, 슬래시 제외한 문자열 |
| int | [0-9]+ | 정수 |
| slug | [-a-zA-Z0-9_]+ | 문자, 숫자, 하이픈, 언더스코어 |
| uuid | UUID | UUID 형식 |
| path | [^/]+ | 슬래시 포함한 경로 |

### 프로젝트의 URL 설정

프로젝트의 메인 `urls.py`에서 각 앱의 URL을 포함시킵니다.

```python
# simpleblog/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('pages/', include('pages.urls')),
    path('', include('pages.urls')),  # 루트 경로
]
```

### 앱별 URL 설정

```python
# blog/urls.py

from django.urls import path
from . import views

app_name = 'blog'  # 네임스페이스

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('create/', views.post_create, name='post_create'),
    path('<int:pk>/update/', views.post_update, name='post_update'),
    path('<int:pk>/delete/', views.post_delete, name='post_delete'),
]
```

### URL 역참조 (Reverse)

템플릿이나 뷰에서 URL 주소를 동적으로 생성합니다.

```python
# 뷰에서 사용
from django.urls import reverse

url = reverse('blog:post_list')  # '/blog/'
url = reverse('blog:post_detail', args=[1])  # '/blog/1/'
```

```html
<!-- 템플릿에서 사용 -->
<a href="{% url 'blog:post_list' %}">모든 포스트</a>
<a href="{% url 'blog:post_detail' pk=post.id %}">포스트 보기</a>
```

---

## 08-2. FBV (Function-Based View) 로 페이지 만들기

### FBV란?
뷰를 Python 함수로 작성하는 방식입니다. 간단하고 직관적입니다.

### 기본 구조

```python
# blog/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from .models import Post

# 기본 함수형 뷰
def post_list(request):
    """모든 포스트를 나열하는 뷰"""
    posts = Post.objects.filter(is_published=True)
    context = {'posts': posts}
    return render(request, 'blog/post_list.html', context)


# 디테일 뷰
def post_detail(request, pk):
    """특정 포스트의 상세 내용을 보여주는 뷰"""
    post = get_object_or_404(Post, pk=pk, is_published=True)
    
    # 조회수 증가
    post.views += 1
    post.save()
    
    comments = post.comments.filter(is_approved=True)
    context = {
        'post': post,
        'comments': comments
    }
    return render(request, 'blog/post_detail.html', context)


# HTTP 메서드 제한
@require_http_methods(["GET", "POST"])
def post_create(request):
    """새로운 포스트를 생성하는 뷰"""
    
    if request.method == 'POST':
        # POST 요청 처리
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        post = Post.objects.create(
            title=title,
            content=content,
            author=request.user,
            is_published=True
        )
        
        return redirect('blog:post_detail', pk=post.pk)
    
    # GET 요청 처리
    return render(request, 'blog/post_form.html')


def post_update(request, pk):
    """포스트를 수정하는 뷰"""
    post = get_object_or_404(Post, pk=pk)
    
    # 작성자 확인
    if post.author != request.user:
        return redirect('blog:post_detail', pk=pk)
    
    if request.method == 'POST':
        post.title = request.POST.get('title', post.title)
        post.content = request.POST.get('content', post.content)
        post.save()
        return redirect('blog:post_detail', pk=post.pk)
    
    context = {'post': post}
    return render(request, 'blog/post_form.html', context)


def post_delete(request, pk):
    """포스트를 삭제하는 뷰"""
    post = get_object_or_404(Post, pk=pk)
    
    if post.author != request.user:
        return redirect('blog:post_detail', pk=pk)
    
    if request.method == 'POST':
        post.delete()
        return redirect('blog:post_list')
    
    context = {'post': post}
    return render(request, 'blog/post_confirm_delete.html', context)
```

### FBV의 장점과 단점

**장점:**
- 간단하고 직관적
- 빠르게 작성 가능
- 명시적인 제어 흐름

**단점:**
- 복잡한 로직은 코드가 길어짐
- 재사용성이 낮음
- 중복 코드 작성

---

## 08-3. CBV (Class-Based View) 로 페이지 만들기

### CBV란?
뷰를 Python 클래스로 작성하는 방식입니다. 코드 재사용성이 높고 유지보수하기 좋습니다.

### 기본 구조

```python
# blog/views.py

from django.views import View
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post


class PostListView(ListView):
    """포스트 목록을 보여주는 CBV"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        """발행된 포스트만 필터링"""
        return Post.objects.filter(is_published=True)


class PostDetailView(DetailView):
    """포스트 상세 내용을 보여주는 CBV"""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_queryset(self):
        return Post.objects.filter(is_published=True)
    
    def get_context_data(self, **kwargs):
        """컨텍스트에 댓글 추가"""
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(is_approved=True)
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """포스트 생성 CBV"""
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'excerpt', 'is_published']
    
    def form_valid(self, form):
        """폼 유효성 확인 후 작성자 설정"""
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        """성공 후 이동할 URL"""
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})


class PostUpdateView(LoginRequiredMixin, UpdateView):
    """포스트 수정 CBV"""
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'excerpt', 'is_published']
    
    def get_queryset(self):
        """현재 사용자의 포스트만"""
        return Post.objects.filter(author=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})


class PostDeleteView(LoginRequiredMixin, DeleteView):
    """포스트 삭제 CBV"""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')
    
    def get_queryset(self):
        """현재 사용자의 포스트만"""
        return Post.objects.filter(author=self.request.user)
```

### 주요 Generic CBV

| CBV | 기능 | HTTP 메서드 |
|-----|------|-----------|
| View | 기본 클래스 | GET, POST 등 |
| ListView | 목록 조회 | GET |
| DetailView | 상세 조회 | GET |
| CreateView | 객체 생성 | GET, POST |
| UpdateView | 객체 수정 | GET, POST |
| DeleteView | 객체 삭제 | GET, POST |

### CBV URL 설정

```python
# blog/urls.py

from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('create/', views.PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
]
```

### CBV의 장점과 단점

**장점:**
- 코드 재사용성 높음
- DRY (Don't Repeat Yourself) 원칙 준수
- 인증, 권한 관리 쉬움
- 상속을 통한 확장 용이

**단점:**
- 초기 학습 곡선이 가파름
- 복잡한 커스터마이징이 어려울 수 있음
- 매직이 많음 (내부 동작 이해 필요)

### FBV vs CBV 선택 가이드

| 상황 | 추천 |
|------|------|
| 간단한 뷰 | FBV |
| CRUD 작업 | CBV |
| 복잡한 로직 | FBV |
| 재사용 가능한 뷰 | CBV |
| 빠른 프로토타이핑 | FBV |
| 대규모 프로젝트 | CBV |

---

## 요약

- **08-1**: URL 패턴으로 요청을 뷰에 라우팅
- **08-2**: FBV는 간단하고 명시적
- **08-3**: CBV는 재사용 가능하고 확장성이 좋음
