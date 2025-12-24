from django.db import models
from django.contrib.auth.models import User
# ORM  - 쿼리대신 DB를 사용하는 방법
# 카테고리 모델 
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['-created_at']
    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    # 다대일 관계  Many-to-One
    # related_name='posts'  역참조 할때 사용하는 이름  User -> Post 목록에 접근할때 사용하는 이름
    # 설정안하면.. user.post_set.all()
    # 설정하면 .. user.posts.all()
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='posts')
    # category.posts.all()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True,
                                blank=True,related_name='posts')   
    # 다대다
    tags = models.ManyToManyField(Tag, blank=True,related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간 딱 한번만
    updated_at = models.DateTimeField(auto_now=True) # 수정 시간  자동갱신
    published = models.BooleanField(default=False)
    views = models.IntegerField(default=0)  # 조회수
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='comments')
    content = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return f"{self.author.username}'s comment"
class Bookmark(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='bookmarks')
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='bookmarks')
    created_at = models.DateField(auto_now_add=True)
    class Meta:  # 같은 유저는 같은 포스트를 한번만 북마크 할수 있다
        unique_together = ('post', 'user')  # 여러필드를 묶어서 하나의 유니크 제약조건
    def __str__(self):
        return f"{self.user.username}- {self.post.title}"
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='likes')
    created_at = models.DateField(auto_now_add=True)
    class Meta:  
        unique_together = ('post', 'user')  # 여러필드를 묶어서 하나의 유니크 제약조건
    def __str__(self):
        return f"{self.user.username} - {self.post.title}"
    