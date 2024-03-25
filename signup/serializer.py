from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from rest_framework.response import Response
from rest_framework import status

user = get_user_model()

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Frontend에서 더 필요한 정보가 있다면 여기에 추가적으로 작성하면 됩니다. token["is_superuser"] = user.is_superuser 이런식으로요.
        token['username'] = user.username
        token['location'] = user.location
        # token['is_admin'] = user.is_admin
        return token
# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer

# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = TokenObtainPairSerializer

    # def post(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)

    #     if serializer.is_valid():
    #         user = serializer.validated_data.get('user')
    #         token = serializer.validated_data.get('access')
    #         refresh = serializer.validated_data.get('refresh')
    #         return Response({
    #             'token': token,
    #             'refresh': refresh,
    #             'username': user.username,
    #             'location': user.location
    #         })
    #     return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
    
class SignUpSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length=100,required=True, write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'location']
        
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']: # ==> attrs['password']는 User의 password의 해당되는 value값 즉, 실제 비밀번호이다.  
            raise serializers.ValidationError(
                {"message": '비밀번호가 맞지 않습니다.'})
        if len(attrs.get('username', ''))<2:
            raise serializers.ValidationError(
                {'message' : '이름을 2글자 이상으로 해주세요'}
            )
        if len(attrs.get('location', ''))<2:
            raise serializers.ValidationError(
                {'message' : '사는곳의 구를 입력해주세요(2글자 이상)'}
            )
        username=attrs.get('username', '')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {'message' : '이름이 이미 존재합니다.'}
            )
        return attrs
    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            location = validated_data['location'],
        )
        user.set_password(validated_data['password'])
        user.save()
        
        return user