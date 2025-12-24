from django.urls import path, include
from . import views
app_name = 'blog'
urlpatterns = [
    path('',views.post_list, name = 'post_list' ),  # FBV  단순한 뷰 (로직)
    path('<int:pk>/',views.post_detail, name = 'post_detail' ),
    # CBV  crud처럼 반복패턴이 많은 뷰는
    # 폼 처리, 유효성 검사, 성공후 리다이렉트, 에러처리 를 미리 구현해둔 상태
    path('create/',views.PostCreateView.as_view(), name = 'post_create' ),  
    path('<int:pk>/edit',views.PostUpdateView.as_view(), name = 'post_edit' ),
    path('<int:pk>/delete',views.PostDeleteView.as_view(), name = 'post_delete' ),

    # 댓글
    path('<int:pk>/comment',views.add_comment, name = 'add_comment' ),

    # 좋아요, 북마크
    path('<int:pk>/like',views.toggle_like, name = 'toggle_like' ),
    path('<int:pk>/bookmark',views.toggle_bookmark, name = 'toggle_bookmark'),

    # 카테고리 , 검색
    path('<int:pk>/cartegory',views.category_posts, name = 'category_posts'),
    path('search/',views.search, name = 'search'),

    # 대시보드
    path('dashboard/',views.dashboard, name = 'dashboard'),
]
