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




# Create your views here.

# 밑에 주석된 코드는 APIView로 작성한 view이다.
# class PostList(APIView):
#     def get(self, request, format=None):
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)
    
#     def post(self, request, format=None):
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
# class PostDetail(APIView):
#     def get_object(self, pk):
#         try:
#             return Post.objects.get(pk=pk)
#         except Post.DoesNotExist:
#             raise Http404
        
#     def get(self, request, pk, format=None):
#         post = self.get_object(pk)
#         serializer = PostSerializer(post)
#         return Response(serializer.data)
    
#    def put(self, request, pk, format=None):
#       post = self.get_object(pk)
#       serializer = PostSerializer(post, data=request.data)
#       if serializer.is_valid():
#           serializer.save()
#           return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, pk, format=None):
#         post = self.get_object(pk)
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# 클래스형 view를 만들 때 APIView, Mixin, Generic CBV, ViewSets 방식이 있는데 오른쪽으로 갈수록 그 전에 것을 모두 상속하기에 코드가 간결해진다.
# 밑에 코드는 viewsets으로 작성한 view이다.
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
# class CommentViewSet(viewsets.ModelViewSet):
#     authentication_classes = [BasicAuthentication, SessionAuthentication]
#     permission_classes = (IsAuthenticatedOrReadOnly,)
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
    
#     # perform_create는 현재 요청을 하는 user를 전달해주기 위해 만들어진 메서드이다.
#     # 이 저장된 user로 이제 권한을 정해주게 되는데 
#     # 객체를 생성한 유저와 요청을 한 유저가 같으며 그에 해당하는 권한을 주고,
#     # 만약 객체를 생성한 유저와 요청을 한 유저가 다르면 그냥 읽을 수 있게만 해주도록 나는 설정을 했다.
#     # 이것을 판단하기 위한 함수를 만들어준것이다.
#     def perform_create(self, serializer):
#         serializer.save(user = self.request.user)


# comment에 대한 권한을 좀 더 세세하게 나누기 위해서 viewset이 아닌 mixins를 사용했다.        
class CommentList(mixins.ListModelMixin,
                  generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
class CommentDetail(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    permission_classes = (AllowAny,)#(IsAdminUser,IsAuthenticatedOrReadOnly)
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
        if not self.request.user.is_staff:
            raise PermissionDenied({'message' : '접근권한이 없습니다.'})
        serializer.save(user=self.request.user)
        
def post_comments(request, post_id):
    post_comments = Comment.objects.filter(post_id=post_id)
    print(post_comments)
    comments_data = [{'comment': comment.comment, 'user': comment.user.username} for comment in post_comments]
    # return JsonResponse(comments_data, safe=False)
    return JsonResponse({'data': comments_data}, safe=False, json_dumps_params={'ensure_ascii': False}, status=200)
