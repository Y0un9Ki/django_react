from django.shortcuts import render
from .models import Post, Comment
from .serializer import PostSerializer, CommentSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status, viewsets, mixins, generics
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .permissions import IsOwnerOrReadOnly, IsSuperUser
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from .pagination import PaginationHandlerMixin




# Create your views here.

# 밑에 주석된 코드는 APIView로 작성한 view이다.
# class PostList(APIView, PaginationHandlerMixin):
#     pagination_class = PageNumberPagination
#     serializer_class = PostSerializer
#     permission_classes = (AllowAny,)#(IsAuthenticatedOrReadOnly,)
#     # authentication_classes = [JWTAuthentication]
    
       
#     def get(self, request, format=None):
#         posts = Post.objects.all()[::-1]
#         page = self.paginate_queryset(posts)
#         if page is not None:
#             serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
#         else:
#             serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)
    
#     def post(self, request, format=None):
#         serializer = PostSerializer(data=request.data)
#         print(request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    
# class PostDetail(APIView):
#     # permission_classes = (IsOwnerOrReadOnly,)
#     # authentication_classes = [JWTAuthentication]
    
#     def get_object(self, pk):
#         try:
#             return Post.objects.get(pk=pk)
#         except Post.DoesNotExist:
#             raise Http404
        
#     def get(self, request, pk, format=None):
#         post = self.get_object(pk)
#         serializer = PostSerializer(post)
#         return Response(serializer.data)
    
#     def put(self, request, pk, format=None):
#         post = self.get_object(pk)
#         serializer = PostSerializer(post, data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#     def delete(self, request, pk, format=None):
#         post = self.get_object(pk)
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
    
    
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 3
# 클래스형 view를 만들 때 APIView, Mixin, Generic CBV, ViewSets 방식이 있는데 오른쪽으로 갈수록 그 전에 것을 모두 상속하기에 코드가 간결해진다.
# 밑에 코드는 viewsets으로 작성한 view이다.
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-id') #==> id값을 내림차순으로 주겠다.(id가 큰값부터 넘겨준다.)
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
    pagination_class = StandardResultsSetPagination
#     # setting에 PageNumberPagination을 default로 설정해주면 pagenation이 알아서 적용이 된다!!
#     # 하지만 setting에 default로 설치되어있는 pagenation이 맘에 안든다면, 위와같이 StandardResultsSetPagination이라는
#     # 클래스를 만들어서 PageNumberPagination을 상속한 후, 내가 원하는 view에만 pagination_class를 정의해서 따로 pagenation을 설정을 해줄 수 있다.
#     # 위의 코드를 잘 살펴보자!!
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        

# comment에 대한 권한을 좀 더 세세하게 나누기 위해서 viewset이 아닌 mixins를 사용했다.        
class CommentList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs) # 모든 사람이 작성할 수 있도록 post를 작성했다.
    
class CommentDetail(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    permission_classes = (IsOwnerOrReadOnly, IsAdminUser)
    authentication_classes = [JWTAuthentication]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self,request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        # if not self.request.user.is_staff:
        #     raise PermissionDenied({'message' : '접근권한이 없습니다.'})
        serializer.save(user=self.request.user)
        
def post_comments(request, post_id):
    post_comments = Comment.objects.filter(post_id=post_id)
    print(post_comments)
    comments_data = [{'comment': comment.comment, 'user': comment.user.username} for comment in post_comments]
    # return JsonResponse(comments_data, safe=False)
    return JsonResponse({'data': comments_data}, safe=False, json_dumps_params={'ensure_ascii': False}, status=200)

# 규가 post_id 값을 요청을 보내주면 나는 그걸 가지고 post_id에 대한 post의 딕셔너리를 데이터로 응답으로 보내준다.

def post_dict(request, post_id):
    post_dict = Post.objects.filter(id=post_id)
    print(post_dict)
    post_dict_data = [{'id': post.id, 'user': post.user.username,
                       'title': post.title, 'content': post.content, 'created_at': post.created_at}
                      for post in post_dict]
    return JsonResponse(data=post_dict_data[0], safe=False, json_dumps_params={'ensure_ascii': False}, status=200)
    