from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CommentList, CommentDetail, post_comments, post_dict,  PostViewSet # PostList, PostDetail, , #,   # 
from rest_framework.routers import DefaultRouter

# 밑에는 class view를 기반으로 할 때, 만들어줘야 하는 url방식이다.
'''
urlpatterns = [
    path('posts/', views.PostList.as_view()),
    path('posts/<int:pk>/', views.PostDetail.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
'''
# pagination = PostPaginationViewSet.as_view({
#     'get' : 'list',
#     'Post' : 'create',
# })



# router방식 사용

router = DefaultRouter()
router.register('post', PostViewSet, basename='Post')

urlpatterns =[
    path('', include(router.urls)),
    # path('post/', PostList.as_view()),
    # path('post/<int:pk>/', PostDetail.as_view()),
    path('comment/', CommentList.as_view()),
    path('comment/<int:pk>/', CommentDetail.as_view()),
    path('comments/<int:post_id>/', post_comments),
    path('posts/<int:post_id>/', post_dict),
]
    # path('pagination/', pagination)
# 위에는 router를 사용했을 때이며, 밑에는 router를 사용하지 않을 때 만들어줘야 하는 코드이다. 매우 편한것을 볼 수 있다.

'''
post_list = PostViewSet.as_view({
    'get' : 'list',
    'post' : 'create'
})

post_detail = PostViewSet.as_view({
    'get' : 'retrieve',
    'put' : 'update',
    'delete' : 'destroy'
})

urlpatterns =[
    path('posts/', post_list),
    path('posts/<int:pk>/', post_detail),
]
'''
