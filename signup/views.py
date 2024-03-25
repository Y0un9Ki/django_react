from django.shortcuts import render
from .serializer import SignUpSerializer
from .models import User
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.serializer import MyTokenObtainPairSerializer, RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from rest_framework.response import Response

# Create your views here.
User = get_user_model()

# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.user
            token = serializer.validated_data['access']
            refresh = serializer.validated_data['refresh']
            return Response({
                'token': token,
                'refresh': refresh,
                'user': {
                    'username': user.username,
                    'location': user.location
                    # 추가적으로 필요한 정보가 있다면 여기에 추가
                }
            })
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
    
class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
        
            return Response(
                {"message": 200},
                status=status.HTTP_200_OK
            )
        
        '''
        밑에 코드 잘 공부해보기. 만약 HTTP 통신이 와서 view에서 회원가입 api를 보내서 회원가입을 하는데,
        내가 정의해놓은 serializer의 유효성 검증 함수를 통과하지 못했을 때 진행되는 과정이다.
        밑에 코드는 내가 serializer에서 validate함수에 만들어놓은 에러메세지를 상황에 맞게 띄워주는 코드이다.
        '''
        errors = serializer.errors
        return Response(
            errors,
            status=status.HTTP_400_BAD_REQUEST
        )