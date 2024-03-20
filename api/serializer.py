from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User

User = get_user_model()

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Frontend에서 더 필요한 정보가 있다면 여기에 추가적으로 작성하면 됩니다. token["is_superuser"] = user.is_superuser 이런식으로요.
        token['username'] = user.username
        token['location'] = user.location
        return token

class RegisterSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(required=True)
    # password = serializers.CharField(
    #     write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    # location = serializers.CharField(required=True)
    # RegisterSerializer에서 ModelSerializer를 상속받았기에 model에서 가지고 있는 속성들을 알아서 가지고 온다. 
    # 그렇기에 굳이 username, password, location을 정의를 안해줘도 되지만 헷갈리기에 그냥 정의하자!!!
    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'location')
        # fields의 내가 model의 User의 password2를 정의해놓지 않았지만 RegisterSerializer에서 정의를 했기에 fields에 넣어주어야 한다.

    def validate(self, attrs): # ==> 여기서 attrs는 User의 저장된 username, password, location 키값에 들어가있는 value들을 딕셔너리 형태로 들고오는 것!!!
        if attrs['password'] != attrs['password2']: # ==> attrs['password']는 User의 password의 해당되는 value값 즉, 실제 비밀번호이다.  
            raise serializers.ValidationError(
                {"password": 'not matched password1, password2'})
        
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError(
                {"username": 'already username exist'})

        return attrs

    def create(self, validated_data):
        location = validated_data.pop('location', None) # None이 의미하는 것은 만약 location이 없으면 None값을 줘라라는 의미
        user = User.objects.create(
            username=validated_data['username'],
        )

        user.set_password(validated_data['password'])
        if location:
            user.location = location
        user.save()
        
        return user