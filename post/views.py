from django.shortcuts import render
from .models import Post
from .serializer import PostSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets

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
    
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user) 