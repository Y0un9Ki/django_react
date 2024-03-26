from .models import User
from rest_framework import serializers
from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length=100,required=True, write_only=True)
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'password2',
            'location',
        ]
        
    def validate(self, attrs):
        if attrs['password']!=attrs['password2']:
            raise serializers.ValidationError(
                {'message': '비밀번호가 맞지 않습니다.'}
            )
        if len(attrs.get('username', ''))<2:
            raise serializers.ValidationError(
                {'message': '이름을 2글자 이상으로 해주세요'}
            )
        if len(attrs.get('location', ''))<2:
            raise serializers.ValidationError(
                {'message': '사는곳의 구를 입력해주세요(서울로 한정)'}
            )
        if len(attrs.get('location', ''))>5:
            raise serializers.ValidationError(
                {'message': '서울시 구를 입력해주세요(5글자를 넘기지 않아요)'}
            )
            
        username=attrs.get('username', '')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {'message' : '이름이 이미 존재합니다.'}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2', '')
        auth_user = User.objects.create_user(**validated_data)
        return auth_user
    
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=10)
    password = serializers.CharField(max_length=15, write_only=True)
    # passoword2 = serializers.CharField(read_only = True) # 비밀번호 확인을 위해 이것을 추가함
    location = serializers.CharField(read_only = True) # 이것을 추가함
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)

    def create(self, validated_date):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError({'message': "회원가입을 해주세요"})

        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)

            update_last_login(None, user)

            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'username': user.username,
                'role': user.role,
                'location' : user.location
            }

            return validation
        except User.DoesNotExist:
            raise serializers.ValidationError({'message' :"회원가입을 해주세요"})
        
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'role',
            'location'
        )